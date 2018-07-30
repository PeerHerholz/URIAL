def rdm_dist(rdms):
    '''function to compute distances between all
        RDMs in a given dictionary'''

    global DefaultListOrderedDict
    from collections import OrderedDict


    class DefaultListOrderedDict(OrderedDict):
        def __missing__(self,k):
            self[k] = []
            return self[k]


    from os.path import join as opj
    from scipy.io.matlab import loadmat
    import pandas as pd
    from collections import OrderedDict
    import pickle
    import numpy as np
    from scipy.spatial import distance
    from itertools import combinations

    with open(rdms, 'rb') as f:
        dict_rdms = pickle.load(f)

    rdms = dict_rdms['rdm']
    ids = dict_rdms['id']

    global rdms_dist

    rdms_dist = [distance.euclidean(x.as_matrix().flatten(), y.as_matrix().flatten()) for x, y in combinations(rdms, 2)]

    rdms_dist = pd.DataFrame(distance.squareform(rdms_dist), columns=ids)

    return(rdms_dist)