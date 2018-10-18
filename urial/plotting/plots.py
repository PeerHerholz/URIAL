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

        rdm = rdm.as_matrix()

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

        rdm = rdm.as_matrix()

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
    rdm = rdm.as_matrix()

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

    # set plot parameter
    if plot is None or plot=='bar':
        ax = sns.barplot(x=model_comp['models'], y=model_comp['cor'], data=model_comp)
        plt.plot(np.linspace(0, 1, 1000), [model_comp['upper_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(0, 1, 1000), [model_comp['lower_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, model_comp['lower_noise_ceiling'][0]), 10000, (model_comp['upper_noise_ceiling'][0] - model_comp['lower_noise_ceiling'][0]), color='r',
                             alpha=0.5)
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
        plt.plot(np.linspace(0, 1, 1000), [model_comp['upper_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        plt.plot(np.linspace(0, 1, 1000), [model_comp['lower_noise_ceiling'][0]] * 1000, 'r', alpha=0.1)
        rect = plt.Rectangle((-20, model_comp['lower_noise_ceiling'][0]), 10000, (model_comp['upper_noise_ceiling'][0] - model_comp['lower_noise_ceiling'][0]), color='r',
                             alpha=0.5)
        if comp is None or comp == 'spearman':
            ax.set(ylabel='spearman correlation with target RDM')
        if comp == 'pearson':
            ax.set(ylabel='pearson correlation with target RDM')
        if comp == 'kendalltaua':
            ax.set(ylabel='kendall tau a correlation with target RDM')
        ax.add_patch(rect)
        plt.tight_layout()