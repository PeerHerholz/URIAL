def rdm_compare(rdms, models, comp=None, plot=None):
    '''function to compare target and model rmds'''

    import pandas as pd
    from scipy.spatial import distance
    from nilearn.connectome import sym_matrix_to_vec, vec_to_sym_matrix
    from scipy.stats import rankdata, spearmanr, kendalltau, pearsonr, mstats
    import numpy as np
    from itertools import combinations
    import pickle
    import seaborn as sns
    import matplotlib.pyplot as plt
    import copy

    if isinstance(rdms, str) is True:
        with open(rdms, 'rb') as f:
            dict_rdms = pickle.load(f)
        target_rdms = copy.deepcopy(dict_rdms['rdm'])
        target_conds = target_rdms[0].keys()
    else:
        target_rdms = rdms
        target_conds = rdms[0].keys()

    if isinstance(models, str) is True:
        with open(models, 'rb') as f:
            dict_models = pickle.load(f)
            models = dict_models['rdm']
            model_ids = dict_models['id']
    else:
        models = models

    for rdm in dict_models['rdm']:
        if 'Unnamed: 0' in rdm:
            del rdm['Unnamed: 0']

    for index, rdm in enumerate(target_rdms):
        target_rdms[index] = target_rdms[index].as_matrix()

    list_cor_rdm = list(range(0, len(target_rdms)))
    list_p = list(range(0, len(target_rdms)))
    target_rdms_trans = list(range(0, len(target_rdms)))

    if comp is None or comp == 'spearman':
        for index, rdm in enumerate(target_rdms):
            target_rdms_trans[index] = vec_to_sym_matrix(rankdata(sym_matrix_to_vec(rdm)))
            rdm_avg = pd.DataFrame(np.mean(target_rdms_trans, axis=0), columns=target_conds)

        for index, part_rdm in enumerate(target_rdms_trans):
            list_cor_rdm[index], list_p[index] = spearmanr(part_rdm.flatten(), rdm_avg.as_matrix().flatten())

        list_cor_sub = list()
        list_cor_rdm_sub = list()
        list_p_sub = list()

        for index, part in enumerate(target_rdms_trans):
            tmp_rdms = target_rdms_trans.copy()
            tmp_part = target_rdms_trans[index]
            tmp_rdms.pop(index)
            tmp_rdm_avg = np.mean(tmp_rdms, axis=0)
            list_cor_sub.append(spearmanr(tmp_part.flatten(), tmp_rdm_avg.flatten()))

        for i, cor in enumerate(list_cor_sub):
            list_cor_rdm_sub.append(cor.correlation)
            list_p_sub.append(cor.pvalue)

    elif comp == 'kendalltaua':
        for index, rdm in enumerate(target_rdms):
            target_rdms_trans[index] = vec_to_sym_matrix(rankdata(sym_matrix_to_vec(rdm)))
            rdm_avg = pd.DataFrame(np.mean(target_rdms, axis=0), columns=target_conds)

        for index, part_rdm in enumerate(target_rdms):
            list_cor_rdm[index], list_p[index] = kendalltau(part_rdm.flatten(), rdm_avg.as_matrix().flatten())

        list_cor_sub = list()
        list_cor_rdm_sub = list()
        list_p_sub = list()

        for index, part in enumerate(target_rdms):
            tmp_rdms = target_rdms.copy()
            tmp_part = target_rdms[index]
            tmp_rdms.pop(index)
            tmp_rdm_avg = np.mean(tmp_rdms, axis=0)
            list_cor_sub.append(kendalltau(tmp_part.flatten(), tmp_rdm_avg.flatten()))

        for i, cor in enumerate(list_cor_sub):
            list_cor_rdm_sub.append(cor.correlation)
            list_p_sub.append(cor.pvalue)

    elif comp == 'pearson':
        for index, rdm in enumerate(target_rdms):
            target_rdms_trans[index] = vec_to_sym_matrix(mstats.zscore(sym_matrix_to_vec(rdm)))
            rdm_avg = pd.DataFrame(np.mean(target_rdms_trans, axis=0), columns=target_conds)

        for index, part_rdm in enumerate(target_rdms_trans):
            list_cor_rdm[index], list_p[index] = pearsonr(part_rdm.flatten(), rdm_avg.as_matrix().flatten())

        list_cor_sub = list()
        list_cor_rdm_sub = list()
        list_p_sub = list()

        for index, part in enumerate(target_rdms_trans):
            tmp_rdms = target_rdms_trans.copy()
            tmp_part = target_rdms_trans[index]
            tmp_rdms.pop(index)
            tmp_rdm_avg = np.mean(tmp_rdms, axis=0)
            list_cor_sub.append(pearsonr(tmp_part.flatten(), tmp_rdm_avg.flatten()))

        for i, cor in enumerate(list_cor_sub):
            list_cor_rdm_sub.append(cor[0])
            list_p_sub.append(cor[1])

    upper_noise_ceiling = np.mean(list_cor_rdm)
    lower_noise_ceiling = np.mean(list_cor_rdm_sub)

    model_comp = pd.DataFrame(columns=['participant', 'models', 'cor'],
                              index=np.arange(len(dict_models['id']) * len(dict_rdms['id'])))
    model_comp['participant'] = dict_rdms['id'] * len(dict_models['id'])
    model_comp['models'] = sorted(dict_models['id'] * len(dict_rdms['id']))

    list_cor_models = list()

    snd_rdms = list()
    snd_rdms.append(rdm_avg.as_matrix())
    for mod_rdm in models:
        snd_rdms.append(mod_rdm.as_matrix())

    ids_rdms = list()
    ids_rdms.append('group average')
    for mod_ids in model_ids:
        ids_rdms.append(mod_ids)

    if comp is None or comp == 'spearman':
        for index, model_rdm in enumerate(dict_models['rdm']):
            for i, sub_rdm in enumerate(target_rdms_trans):
                list_cor_models.append(spearmanr(sub_rdm.flatten(), model_rdm.as_matrix().flatten()).correlation)
                rdms_dist = [spearmanr(x.flatten(), y.flatten()).correlation for x, y in combinations(snd_rdms, 2)]
                rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids_rdms)
    elif comp == 'kendalltaua':
        for index, model_rdm in enumerate(dict_models['rdm']):
            for i, sub_rdm in enumerate(target_rdms):
                list_cor_models.append(kendalltau(sub_rdm.flatten(), model_rdm.as_matrix().flatten()).correlation)
                rdms_dist = [kendalltau(x.flatten(), y.flatten()).correlation for x, y in combinations(snd_rdms, 2)]
                rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids_rdms)
    elif comp == 'pearson':
        for index, model_rdm in enumerate(dict_models['rdm']):
            for i, sub_rdm in enumerate(target_rdms_trans):
                list_cor_models.append(pearsonr(sub_rdm.flatten(), model_rdm.as_matrix().flatten())[0])
                rdms_dist = [pearsonr(x.flatten(), y.flatten())[0] for x, y in combinations(snd_rdms, 2)]
                rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids_rdms)

    model_comp['cor'] = list_cor_models

    if plot is None:
        print('results will not be plotted')
    elif plot == 'bar':
        ax = sns.barplot(x=model_comp['models'], y=model_comp['cor'], data=model_comp)
        plt.plot(np.linspace(-20, 120, 1000), [upper_noise_ceiling] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(-20, 120, 1000), [lower_noise_ceiling] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, lower_noise_ceiling), 10000, (upper_noise_ceiling - lower_noise_ceiling), color='r',
                             alpha=0.5)
        ax.set_xticklabels(labels=list(dict_models['id']))
        if comp is None or comp == 'spearman':
            ax.set(ylabel='spearman correlation with target RDM')
        if comp == 'pearson':
            ax.set(ylabel='pearson correlation with target RDM')
        if comp == 'kendalltaua':
            ax.set(ylabel='kendall tau a correlation with target RDM')
        ax.add_patch(rect)
        plt.tight_layout()
    elif plot == 'violin':
        ax = sns.violinplot(x=model_comp['models'], y=model_comp['cor'], data=model_comp)
        plt.plot(np.linspace(-20, 120, 1000), [upper_noise_ceiling] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(-20, 120, 1000), [lower_noise_ceiling] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, lower_noise_ceiling), 10000, (upper_noise_ceiling - lower_noise_ceiling), color='r',
                             alpha=0.5)
        ax.set_xticklabels(labels=list(dict_models['id']))
        if comp is None or comp == 'spearman':
            ax.set(ylabel='spearman correlation with target RDM')
        if comp == 'pearson':
            ax.set(ylabel='pearson correlation with target RDM')
        if comp == 'kendalltaua':
            ax.set(ylabel='kendall tau a correlation with target RDM')
        ax.add_patch(rect)
        plt.tight_layout()

    return rdm_avg, model_comp, rdms_dist