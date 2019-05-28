def plot_rdm(rdm, mat=False, model=False, level=None, comp=None, cmap="Spectral_r"):
    '''
    function to visualize RDM based rank transformed and scaled similarity values
    (only for plotting, raw/initial values remain unchanged)
    '''

    from scipy.io.matlab import loadmat
    from scipy.stats import rankdata
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import minmax_scale
    import pandas as pd
    import seaborn as sns
    from nilearn.connectome import sym_matrix_to_vec, vec_to_sym_matrix

    if mat is True:
        matfile = loadmat(rdm)
        rdm = matfile['rdm'][0][0]

    if isinstance(rdm, str) is True:
        rdm = pd.read_csv(rdm, sep=',')
        if 'Unnamed: 0' in rdm:
            del rdm['Unnamed: 0']
    else:
        rdm=rdm

    categories = list(rdm.columns)
    y_categories = list(categories)

    if model is False and level == '2nd':

        ax = sns.heatmap(rdm, xticklabels=categories, yticklabels=y_categories, cmap=cmap, vmin=-1, vmax=1)
        ax.set_yticklabels(y_categories, rotation=0)
        ax.xaxis.tick_top()
        ax.set_xticklabels(categories, rotation=90)
        if comp is None:
            ax.collections[0].colorbar.set_label("correlations between RDMs")
        if comp == 'kendalltaua':
            ax.collections[0].colorbar.set_label("correlations between RDMs [kendall tau]")
        if comp == 'spearman':
            ax.collections[0].colorbar.set_label("correlations between RDMs [spearman]")
        if comp == 'pearson':
            ax.collections[0].colorbar.set_label("correlations between RDMs [pearson]")
        plt.tight_layout()



    if model is False and level is None:

        rdm = rdm.to_numpy()

        rdm_vec = sym_matrix_to_vec(rdm)
        rdm_vec = rankdata(rdm_vec)

        rdm_array = rdm_vec.reshape(-1, 1)
        rdm_array = minmax_scale(rdm_array, (0, 1))
        rdm_array = rdm_array.flatten()
        rdm_rank_scale = vec_to_sym_matrix(rdm_array)

        ax = sns.heatmap(rdm_rank_scale, xticklabels=categories, yticklabels=y_categories, cmap=cmap)
        ax.set_yticklabels(y_categories, rotation=0)
        ax.xaxis.tick_top()
        ax.set_xticklabels(categories, rotation=90)
        ax.collections[0].colorbar.set_label("pairwise similarities, rank transformed & scaled [0,1]")
        plt.tight_layout()

    if model is True:

        rdm = rdm.to_numpy()

        rdm_vec = sym_matrix_to_vec(rdm)

        rdm_array = rdm_vec.reshape(-1, 1)
        rdm_array = minmax_scale(rdm_array, (0, 1))
        rdm_array = rdm_array.flatten()
        rdm_scale = vec_to_sym_matrix(rdm_array)

        ax = sns.heatmap(rdm_scale, xticklabels=categories, yticklabels=y_categories, cmap=cmap)
        ax.set_yticklabels(y_categories, rotation=0)
        ax.xaxis.tick_top()
        ax.set_xticklabels(categories, rotation=90)
        ax.collections[0].colorbar.set_label("pairwise similarities, scaled [0,1]")
        plt.tight_layout()




def plot_mds(rdm, level=None):
    '''function to visualize RDM via multidimensional scaling'''

    # big kudos to Jona Sassenhagen for doing an amazing job
    # adding condition names and colors to the mds plot

    # import modules and functions
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import manifold
    from sklearn.decomposition import PCA
    from matplotlib.collections import LineCollection

    ## computation/transformation section

    # read in the rdm in .csv format, creating a data frame
    if isinstance(rdm, str) is True:
        df = pd.read_csv(rdm)
        if 'Unnamed: 0' in rdm:
            del rdm['Unnamed: 0']
    else:
        df=rdm

    df.index = df.columns  # set data frame index based on columns

    if level == '2nd':
        df= df.mask(df.values > -1.05, 1 - df.values)

    # set seed for mds
    seed = 0

    # create mds object
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                       dissimilarity="precomputed", n_jobs=1)
    # apply mds to data frame
    rdm_mds = mds.fit(df.values).embedding_

    # create new data frame from mds
    df_mds = pd.DataFrame(rdm_mds, index=df.index, columns=["dim1", "dim2"])
    df_mds["cond"] = df_mds.index # create condition column based on index

    # create pca object
    clf = PCA(n_components=2)

    # set rdm data frame based on data frame values
    rdm = pd.DataFrame(df.values)

    # scale data
    rdm = rdm.max() / rdm * 100
    rdm[np.isinf(rdm)] = 0

    # convert rdm data frame to array
    rdm = rdm.to_numpy()

    # apply pca to mds
    rdm_mds_pca = clf.fit_transform(rdm_mds)

    ## plotting section

    sns.set_style("white") # set seaborn style to white
    # create lmplot from the mds data frame
    g = sns.lmplot("dim1", "dim2", hue="cond", data=df_mds, fit_reg=False, legend=False)
    ax = g.ax # set axes
    sns.despine(ax=ax, trim=True, left=True, bottom=True) # despine graphic
    ax.axes.get_xaxis().set_visible(False) # remove x axis
    ax.axes.get_yaxis().set_visible(False) # remove y axis
    ax.grid(False) # remove gird

    # add condition names to plot
    for dim1, dim2, name in df_mds.values:
        ax.text(dim1 * 1.05, dim2 * 1.05, name)

    # create segments
    segments = [[rdm_mds[i, :], rdm_mds[j, :]]
                for i in range(len(rdm_mds_pca)) for j in range(len(rdm_mds_pca))]
    values = np.abs(rdm)

    # set line collection
    lc = LineCollection(segments,
                        zorder=0, cmap=plt.cm.Greys,
                        norm=plt.Normalize(0, values.max()))
    lc.set_array(rdm.flatten())
    lc.set_linewidths(0.5 * np.ones(len(segments)))
    ax.add_collection(lc) # add line collection to plot

    plt.tight_layout()
    plt.show()


def plot_dendrogram(rdm, co_th=None):
    '''function to visualize RDM as dendrogram'''

    import pandas as pd
    from scipy.cluster.hierarchy import dendrogram, linkage

    # read in the rdm in .csv format, creating a data frame
    if isinstance(rdm, str) is True:
        df = pd.read_csv(rdm)
        if 'Unnamed: 0' in rdm:
            del rdm['Unnamed: 0']
    else:
        rdm = rdm

    data_den = linkage(rdm, 'ward')

    if co_th is not None:
        co_th = co_th
    elif co_th is None:
        co_th = 'default'

    # Make the dendro
    dendrogram(data_den, labels=rdm.columns, leaf_rotation=0, orientation="left", color_threshold=co_th,
               above_threshold_color='grey')


def plot_model_fit(model_comp, plot=None, comp=None):
    '''function to visualize RDM model fit'''

    # read in the rdm in .csv format, creating a data frame
    if isinstance(model_comp, str) is True:
        df = pd.read_csv(model_comp)
        if 'Unnamed: 0' in rdm:
            del rdm['Unnamed: 0']
    else:
        model_comp = model_comp

    sns.set_style('darkgrid')
    sns.set_context('paper')

    #sns.set_palette("hls", len(model_comp['models'].unique()))
    sns.set_palette(rdm_col)

    # set plot parameter
    if plot is None or plot=='bar':
        ax = sns.barplot(x=model_comp['models'], y=model_comp['cor'], data=model_comp)
        plt.plot(np.linspace(0, 1, 1000), [model_comp['upper_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(0, 1, 1000), [model_comp['lower_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, model_comp['lower_noise_ceiling'][0]), 10000, (model_comp['upper_noise_ceiling'][0] - model_comp['lower_noise_ceiling'][0]), color='firebrick',
                             alpha=0.5)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        if comp is None or comp == 'spearman':
            ax.set(ylabel='spearman correlation with target RDM')
        if comp == 'pearson':
            ax.set(ylabel='pearson correlation with target RDM')
        if comp == 'kendalltaua':
            ax.set_xlabel("models", fontsize=12)
            ax.set_ylabel("kendall tau a correlation with target RDM", fontsize=12)
            sns.set(font_scale=0.7)
        ax.add_patch(rect)
        plt.tight_layout()
    elif plot == 'violin':
        ax = sns.violinplot(x=model_comp['models'], y=model_comp['cor'], data=model_comp)
        plt.plot(np.linspace(0, 1, 1000), [model_comp['upper_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(0, 1, 1000), [model_comp['lower_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, model_comp['lower_noise_ceiling'][0]), 10000, (model_comp['upper_noise_ceiling'][0] - model_comp['lower_noise_ceiling'][0]), color='r',
                             alpha=0.5)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        if comp is None or comp == 'spearman':
            ax.set(ylabel='spearman correlation with target RDM')
        if comp == 'pearson':
            ax.set(ylabel='pearson correlation with target RDM')
        if comp == 'kendalltaua':
            ax.set(ylabel='kendall tau a correlation with target RDM')
        ax.add_patch(rect)
        plt.tight_layout()


# # # model_rdms = ['behavior', 'main genre', 'sub genre', 'random', 'spectrum', 'pitch', 'chroma', 'timbre', 'dynamic tempo','tempogram']
# model_rdms = ['main genre', 'random', 'sub genre', 'chroma', 'dynamic tempo', 'pitch', 'timbre', 'spectrum','tempogram']
# #
# models = []
# #
#  for model in model_rdms:
#      models.append([model]*10)
# #
# models = models[0] + models[1] + models[2] + models[3] + models[4] + models[5] + models[6] + models[7] + models[8] #+ models[9]
#
# model_comp['models'] = models
#
# model_comp_main = model_comp.loc[model_comp['models'] == 'main genre']
# model_comp_sub = model_comp.loc[model_comp['models'] == 'sub genre']
# model_comp_rand = model_comp.loc[model_comp['models'] == 'random']
# #model_comp_behav = model_comp.loc[model_comp['models'] == 'behavior']
# model_comp_spectrum = model_comp.loc[model_comp['models'] == 'spectrum']
# model_comp_pitch = model_comp.loc[model_comp['models'] == 'pitch']
# model_comp_chroma = model_comp.loc[model_comp['models'] == 'chroma']
# model_comp_timbre = model_comp.loc[model_comp['models'] == 'timbre']
# model_comp_dynamictemp = model_comp.loc[model_comp['models'] == 'dynamic tempo']
# model_comp_temp = model_comp.loc[model_comp['models'] == 'tempogram']
#
# #model_comp_ord = pd.concat([model_comp_behav, model_comp_main, model_comp_sub, model_comp_rand, model_comp_spectrum, model_comp_pitch, model_comp_chroma, model_comp_timbre, model_comp_dynamictemp, model_comp_temp])
#
# model_comp_ord = pd.concat([model_comp_main, model_comp_sub, model_comp_rand, model_comp_spectrum, model_comp_pitch, model_comp_chroma, model_comp_timbre, model_comp_dynamictemp, model_comp_temp])
#
#
# #
# #rdm_col = ["lightcoral", "peachpuff", "peru", "khaki", "darkolivegreen", "seagreen", "forestgreen", "darkseagreen", "steelblue", "cornflowerblue"]
#
# #rdm_col = ["lightcoral", "peachpuff", "darkolivegreen", "seagreen", "forestgreen", "darkseagreen", "steelblue", "cornflowerblue",  "c", "royalblue"]
#
# #rdm_col = ["lightcoral", "darkolivegreen", "steelblue", "khaki",  "firebrick", "m"]
#
# # behavior
# rdm_col = ["lightcoral", "peachpuff", "peru", "darkolivegreen", "seagreen", "forestgreen", "darkseagreen", "steelblue", "cornflowerblue"]
#
#
#
# #
# plot_model_fit(model_comp_ord, comp='kendalltaua')
# #
# # avg_reg = ['HG_l'] * 15 + ['HG_r'] * 15 + ['PP_l'] * 15 + ['PP_r'] * 15 + ['PT_l'] * 15 + ['PT_r'] * 15 + ['STGa_l'] * 15 + ['STGa_r'] * 15 + ['STGp_l'] * 15 + ['STGp_r'] * 15
# #
# # avg_reg = ['TW 1'] * 11 + ['TW 2'] * 11 + ['TW 3'] * 11 + ['TW 4'] * 11 + ['TW 5'] * 11 + ['TW 6'] * 11
#
#
