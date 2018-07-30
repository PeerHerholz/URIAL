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

<<<<<<< Updated upstream:plot_rdm.py
    rdm = pd.read_csv(rdm, sep=',')
    if 'Unnamed: 0' in rdm:
        del rdm['Unnamed: 0']
=======
    if cmap == None:
        cmap = 'Spectral_r'
    else:
        cmap = cmap

    if isinstance(rdm, str) is True:
        rdm = pd.read_csv(rdm, sep=',')
        if 'Unnamed: 0' in rdm:
            del rdm['Unnamed: 0']
    else:
        rdm=rdm
>>>>>>> Stashed changes:urial/plotting/plot_rdm.py

    categories = list(rdm.columns)

    rdm = rdm.as_matrix()

    rdm_vec = sym_matrix_to_vec(rdm)
    rdm_vec = rankdata(rdm_vec)

    rdm_array = rdm_vec.reshape(-1, 2)
    rdm_array = minmax_scale(rdm_array, (0, 1))
    rdm_array = rdm_array.flatten()
    rdm_rank_scale = vec_to_sym_matrix(rdm_array)

    categories_y = list(reversed(categories))

    ax = sns.heatmap(rdm_rank_scale, xticklabels=categories, cmap=cmap)
    ax.set_yticklabels(categories_y, rotation=0)
    ax.xaxis.tick_top()
    ax.set_xticklabels(categories, rotation=90)
    ax.collections[0].colorbar.set_label("pairwise similarities (iMDS), rank transformed & scaled [0,1]")
    plt.tight_layout()
