def plot_rdm(rdm, mat=0, cmap=None):
    '''function to visualize RDM based rank transformed and scaled similarity values
        (only for plotting, raw/initial values remain unchanged'''

    from os.path import join as opj
    from scipy.io.matlab import loadmat
    from nilearn.connectome import sym_matrix_to_vec
    from scipy.stats import rankdata
    from nilearn.connectome import vec_to_sym_matrix
    from sklearn import preprocessing
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    if mat == 1:
        matfile = loadmat(rdm)
        rdm = matfile['rdm'][0][0]

    if cmap == None:
        cmap = 'Spectral_r'
    else:
        cmap = cmap

    rdm = pd.read_csv(rdm, sep=',')
    if 'Unnamed: 0' in rdm:
        del rdm['Unnamed: 0']

    categories = list(rdm.columns)

    rdm = rdm.as_matrix()

    rdm_vec = sym_matrix_to_vec(rdm)
    rdm_vec = rankdata(rdm_vec)

    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1), copy=True)

    rdm_array = rdm_vec.reshape(-1, 2)
    rdm_array = min_max_scaler.fit_transform(rdm_array)
    rdm_array = rdm_array.flatten()
    rdm_rank_scale = vec_to_sym_matrix(rdm_array)

    ax = sns.heatmap(rdm_rank_scale, xticklabels=categories, yticklabels=categories, cmap=cmap)
    ax.set_yticklabels(categories, rotation=0)
    ax.xaxis.tick_top()
    ax.set_xticklabels(categories, rotation=90)
    ax.collections[0].colorbar.set_label("pairwise similarities (iMDS), rank transformed & scaled [0,1]")
    plt.tight_layout()
