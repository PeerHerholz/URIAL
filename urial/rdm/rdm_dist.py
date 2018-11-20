def rdm_dist(rdms, comp=None, order=None):
    '''function to compute distances between all
        RDMs in a given dictionary'''

    #global DefaultListOrderedDict
    from collections import OrderedDict

    class DefaultListOrderedDict(OrderedDict):
        def __missing__(self,k):
            self[k] = []
            return self[k]

    import pandas as pd
    from collections import OrderedDict
    import pickle
    from scipy.spatial import distance
    from scipy.stats import pearsonr, spearmanr, rankdata, mstats
    from itertools import combinations
    from nilearn.connectome import sym_matrix_to_vec
    import numpy as np

    if isinstance(rdms, str) is True:
        with open(rdms, 'rb') as f:
            dict_rdms = pickle.load(f)
        rdms = dict_rdms['rdm']
        ids = dict_rdms['id']
    else:
        dict_rdms=rdms
        rdms = dict_rdms['rdm']
        ids = dict_rdms['id']

    if order is None:
        print('RDM comparisons will be written to the results data frame in the order they are found in the pkl file')
    elif order is not None:
        print('RDM comparisons will be written to the results data frame in the order specified by the user')
        order=order
        df_order=pd.DataFrame()
        df_order['rdms']=rdms
        df_order['rdm_id']=ids
        df_order.index = ids

        df_order_user = pd.DataFrame(df_order.reindex(order))

        rdms=df_order_user['rdms']
        ids=df_order_user['rdm_id']

    global rdms_dist

    if comp is None or comp == 'euclidean':
        rdms_dist = [distance.euclidean(sym_matrix_to_vec(x.as_matrix(), discard_diagonal=True), sym_matrix_to_vec(y.as_matrix(), discard_diagonal=True)) for x, y in combinations(rdms, 2)]
        rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids)
    elif comp == 'spearman':
         for index, rdm in enumerate(rdms):
             rdms[index] = rankdata(sym_matrix_to_vec(rdm.as_matrix(), discard_diagonal=True))
         rdms_dist = [spearmanr(x, y).correlation for x, y in combinations(rdms, 2)]
         rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids)
         np.fill_diagonal(rdms_dist.values, 1)
         rdms_dist = rdms_dist.mask(rdms_dist.values > -1.05, 1 - rdms_dist.values)
    elif comp == 'pearson':
        for index, rdm in enumerate(rdms):
                rdms[index] = mstats.zscore(sym_matrix_to_vec(rdm.as_matrix(), discard_diagonal=True))
        rdms_dist = [pearsonr(x, y)[0] for x, y in combinations(rdms, 2)]
        rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids)
        np.fill_diagonal(rdms_dist.values, 1)
        rdms_dist = rdms_dist.mask(rdms_dist.values > -1.05, 1 - rdms_dist.values)

    return rdms_dist