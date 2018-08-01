def rdm_compare(rdms, models, comp=None, plot=None):
    '''function to compare target and model
        rmds'''

    global dict_rdms
    global DefaultListOrderedDict

    from glob import glob
    import pandas as pd
    from collections import OrderedDict
    from scipy.spatial import distance
    from scipy.stats import rankdata, spearmanr, kendalltau, pearsonr, mstats
    import numpy as np
    from itertools import combinations

    if isinstance(rdms, str) is True:
        with open(rdms, 'rb') as f:
            dict_rdms = pickle.load(f)

        rdms = dict_rdms['rdm']
        conds = rdms[0].keys()
    else:
        rdms = rdms
        conds = rdms[0].keys()

    if isinstance(models, str) is True:
        with open(models, 'rb') as f:
            dict_models = pickle.load(f)
            models = dict_models['rdm']
    else:
        models = models

    for rdm in dict_models['rdm']:
        if 'Unnamed: 0' in rdm:
            del rdm['Unnamed: 0']


    for index, rdm in enumerate(rdms):
        rdms[index] = rdms[index].as_matrix()


    global rdm_avg

    rdm_avg = pd.DataFrame(np.mean(rdms, axis=0), columns=conds)

    list_cor_rdm=list(range(0,len(rdms)))
    list_p=list(range(0,len(rdms)))

    if comp is None or 'spearman':
        for index, rdm in enumerate(rdms):
        rdms[index]=rankdata(rdm)
    elif comp=='pearson':
        for index, rdm in enumerate(rdms):
        rdms[index]=mstats.zscore(rdm)

    for index, part_rdm in enumerate(rdms):
        list_cor_rdm[index], list_p[index] = spearmanr(part_rdm.flatten() , rdm_avg.as_matrix().flatten())

    upper_noise_ceiling = np.mean(list_cor_rdm)

    list_cor_sub=list()
    list_cor_rdm_sub=list()
    list_p_sub=list()

    for index, part in enumerate(rdms):
        tmp_rdms=rdms.copy()
        tmp_part=rdms[index]
        tmp_rdms.pop(index)
        tmp_rdm_avg=np.mean(tmp_rdms, axis=0)
        list_cor_sub.append(spearmanr(tmp_part.flatten(), tmp_rdm_avg.flatten()))

        #for i, p in enumerate(rdms):
        #    list_cor_sub.append(spearmanr(p.flatten(), tmp_rdm_avg.flatten()))

    for i,cor in enumerate(list_cor_sub):
        list_cor_rdm_sub.append(cor.correlation)
        list_p_sub.append(cor.pvalue)

    lower_noise_ceiling=np.mean(list_cor_rdm_sub)

    model_comp = pd.DataFrame(columns=['participant', 'models', 'cor'], index=np.arange(len(dict_models['id'])*len(dict_rdms['id'])))
    model_comp['participant']=dict_rdms['id']*len(dict_models['id'])
    model_comp['models']=sorted(dict_models['id']*len(dict_rdms['id']))

    list_cor_models=list()

    if comp is None or 'spearman':
        for index, model_rdm in enumerate(dict_models['rdm']):
            for i, sub_rdm in enumerate(dict_rdms['rdm']):
                list_cor_models.append(spearmanr(sub_rdm.flatten(), model_rdm.as_matrix().flatten()).correlation)
    elif comp == 'pearson':
        for index, model_rdm in enumerate(dict_models['rdm']):
            for i, sub_rdm in enumerate(dict_rdms['rdm']):
                list_cor_models.append(pearsonr(sub_rdm.flatten(), model_rdm.as_matrix().flatten())[0])
    elif comp == 'kendalltau':
        for index, model_rdm in enumerate(dict_models['rdm']):
            for i, sub_rdm in enumerate(dict_rdms['rdm']):
            list_cor_models.append(kendalltau(sub_rdm.flatten(), model_rdm.as_matrix().flatten()).correlation)


    model_comp['cor']=list_cor_models

    if plot is None:
        print('results will no be plotted')
    elif plot == 'bar':
        ax=sns.barplot(x=model_comp['models'], y=model_comp['cor'], data=model_comp)
        plt.plot(np.linspace(-20, 120, 1000), [upper_noise_ceiling] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(-20, 120, 1000), [lower_noise_ceiling] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, lower_noise_ceiling), 10000, (upper_noise_ceiling - lower_noise_ceiling), color='r',
                             alpha=0.5)
        ax.set_xticklabels(labels=list(dict_models['id']))
        if comp is None or 'spearman':
            ax.set(ylabel='spearman correlation with target RDM')
        if comp == 'pearson':
            ax.set(ylabel='pearson correlation with target RDM')
        if comp == 'kendalltau':
            ax.set(ylabel='kendall tau a correlation with target RDM')
        ax.add_patch(rect)
        plt.tight_layout()
    elif plot == 'violin':
        ax=sns.violinplot(x=model_comp['models'], y=model_comp['cor'], data=model_comp)
        plt.plot(np.linspace(-20, 120, 1000), [upper_noise_ceiling] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(-20, 120, 1000), [lower_noise_ceiling] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, lower_noise_ceiling), 10000, (upper_noise_ceiling - lower_noise_ceiling), color='r',
                             alpha=0.5)
        ax.set_xticklabels(labels=list(dict_models['id']))
        if comp is None or 'spearman':
            ax.set(ylabel='spearman correlation with target RDM')
        if comp == 'pearson':
            ax.set(ylabel='pearson correlation with target RDM')
        if comp == 'kendalltau':
            ax.set(ylabel='kendall tau a correlation with target RDM')
        ax.add_patch(rect)
        plt.tight_layout()



    return model_comp