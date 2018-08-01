def plot_rdm(rdm, mat=False, cmap="Spectral_r"):
    '''
    function to visualize RDM based rank transformed and scaled similarity values
    (only for plotting, raw/initial values remain unchanged)
    '''

    from os.path import join as opj
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

    rdm = rdm.as_matrix()

    rdm_vec = sym_matrix_to_vec(rdm)
    rdm_vec = rankdata(rdm_vec)

    rdm_array = rdm_vec.reshape(-1, 1)
    rdm_array = minmax_scale(rdm_array, (0, 1))
    rdm_array = rdm_array.flatten()
    rdm_rank_scale = vec_to_sym_matrix(rdm_array)

    y_categories = list(reversed(categories))

    ax = sns.heatmap(rdm_rank_scale, xticklabels=categories, yticklabels=y_categories, cmap=cmap)
    ax.set_yticklabels(y_categories, rotation=0)
    ax.xaxis.tick_top()
    ax.set_xticklabels(categories, rotation=90)
    ax.collections[0].colorbar.set_label("pairwise similarities, rank transformed & scaled [0,1]")
    plt.tight_layout()

def plot_mds(rdm):
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