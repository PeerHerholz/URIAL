def plot_mds_cond(rdm):
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
    df = pd.read_csv(rdm, index_col=0)
    df.index = df.columns # set data frame index based on columns

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