def rdm_dist(rdms, comp=None):
    '''function to compute distances between all
        RDMs in a given dictionary'''

    global DefaultListOrderedDict
    from collections import OrderedDict

    class DefaultListOrderedDict(OrderedDict):
        def __missing__(self,k):
            self[k] = []
            return self[k]

    import pandas as pd
    from collections import OrderedDict
    import pickle
    from scipy.spatial import distance
    from scipy.stats import pearsonr, spearmanr, rankdata
    from itertools import combinations

    if isinstance(rdms, str) is True:
        with open(rdms, 'rb') as f:
            dict_rdms = pickle.load(f)
        rdms = dict_rdms['rdm']
        ids = dict_rdms['id']
    else:
        dict_rdms=rdms
        rdms = dict_rdms['rdm']
        ids = dict_rdms['id']

    global rdms_dist

    if comp is None:
        rdms_dist = [distance.euclidean(x.as_matrix().flatten(), y.as_matrix().flatten()) for x, y in combinations(rdms, 2)]
    elif comp == 'spearman':
         for index, rdm in enumerate(rdms):
             rdms[index] = rankdata(rdm)
         rdms_dist = [spearmanr(x.flatten(), y.flatten()).correlation for x, y in
                      combinations(rdms, 2)]
    elif comp == 'pearson':
        for index, rdm in enumerate(rdms):
                rdms[index] = mstats.zscore(rdm)
        rdms_dist = [pearsonr(x.flatten(), y.flatten())[0] for x, y in combinations(rdms, 2)]

    rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids)

    return rdms_dist