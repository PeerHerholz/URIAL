def feature_dist(path, prefix=None, dist=None, order=None):
    '''function to compute the distance between extracted
        stimuli features within a given directory'''

    global dict_rdms
    global DefaultListOrderedDict
    global feat_dis_mat

    from glob import glob
    import pandas as pd
    from collections import OrderedDict
    from scipy.spatial import distance
    from scipy.stats import spearmanr, pearsonr
    from itertools import combinations
    import numpy as np

    if prefix is None:
        list_features = glob(path + '*.csv')
    else:
        list_features = glob(path + prefix + '*.csv')

    class DefaultListOrderedDict(OrderedDict):
        def __missing__(self, k):
            self[k] = []
            return self[k]

    keys = ['id', 'feature', 'data']

    id = []
    feature = []
    data = []

    for file in list_features:
        id.append(file[(file.rfind('_') + 1):file.rfind('.')])
        feature.append(file[(file.rfind('/') + 1):file.rfind('.')])
        data.append(pd.read_csv(file))

    global dict_features

    dict_features = DefaultListOrderedDict()

    if order is None:
        print('No condition order provided, index will be as found in the directory (alphabetically)')
        for key in keys:
            for id_feat in enumerate(id):
                if key == 'id':
                    dict_features[key].append(id[id_feat[0]])
                elif key == 'feature':
                    dict_features[key].append(feature[id_feat[0]])
                elif key == 'data':
                    dict_features[key].append(data[id_feat[0]])
    else:
        order = order

        df_feat = pd.DataFrame()
        df_feat['id'] = id
        df_feat['feature'] = feature
        df_feat['data'] = data
        df_feat.index = id

        df_feat_order = pd.DataFrame(df_feat.reindex(order))

        id = df_feat_order['id']
        feature = df_feat_order['feature']
        data = df_feat_order['data']

        print('index will be as in the specified order')
        for key in keys:
            for id_feat in enumerate(id):
                if key == 'id':
                    dict_features[key].append(id[id_feat[0]])
                elif key == 'feature':
                    dict_features[key].append(feature[id_feat[0]])
                elif key == 'data':
                    dict_features[key].append(data[id_feat[0]])

    features = dict_features['data']
    ids = dict_features['id']

    if dist is None or dist == 'euclidean':
        feat_dis_mat = [distance.euclidean(x.to_numpy().flatten(), y.to_numpy().flatten()) for x, y in
                        combinations(features, 2)]
        feat_dis_mat = pd.DataFrame(distance.squareform(feat_dis_mat), columns=ids)
    elif dist == 'correlation':
        feat_dis_mat = [distance.correlation(x.to_numpy().flatten(), y.to_numpy().flatten()) for x, y in
                        combinations(features, 2)]
        feat_dis_mat = pd.DataFrame(distance.squareform(feat_dis_mat), columns=ids)
    elif dist == 'spearman':
        feat_dis_mat = [spearmanr(x.to_numpy().flatten(), y.to_numpy().flatten()).correlation for x, y in
                        combinations(features, 2)]
        feat_dis_mat = pd.DataFrame(distance.squareform(feat_dis_mat), columns=ids)
        np.fill_diagonal(feat_dis_mat.values, 1)
        feat_dis_mat = feat_dis_mat.mask(feat_dis_mat.values > -1.05, 1 - feat_dis_mat.values)
    elif dist == 'pearson':
        feat_dis_mat = [pearsonr(x.to_numpy().flatten(), y.to_numpy().flatten())[0] for x, y in
                        combinations(features, 2)]
        feat_dis_mat = pd.DataFrame(distance.squareform(feat_dis_mat), columns=ids)
        np.fill_diagonal(feat_dis_mat.values, 1)
        feat_dis_mat = feat_dis_mat.mask(feat_dis_mat.values > -1.05, 1 - feat_dis_mat.values)

    return feat_dis_mat
