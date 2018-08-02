def rdm_concat_df(path, outfile=None, prefix=None, addata=None, columns=None):
    '''function to create an dictionary containing
        all RDMs from a given dictory'''

    global dict_rdms
    global DefaultListOrderedDict

    import sys
    from glob import glob
    import pandas as pd
    from collections import OrderedDict
    import pickle

    if prefix is None:
        list_rdms=glob(path + '*.csv')
    else:
        list_rdms=glob(path + prefix + '*.csv')

    class DefaultListOrderedDict(OrderedDict):
        def __missing__(self,k):
            self[k] = []
            return self[k]

    keys=['id','rdm']

    id = []
    rdms =[]

    for file in list_rdms:
        id.append(file[(file.rfind('/') + 1):file.rfind('.')])
        rdms.append(pd.read_csv(file))

    global dict_rdms

    dict_rdms = DefaultListOrderedDict()

    for key in keys:
        for id_rdm in enumerate(id):
            if key == 'id':
                dict_rdms[key].append(id[id_rdm[0]])
            elif key == 'rdm':
                dict_rdms[key].append(rdms[id_rdm[0]])

    if addata is None:
        print('no additional data added')
    else:
        if columns is None:
            sys.exit('adding additional data requires the definition of columns to include as additional data')
        else:
            addata_df=pd.read_csv(addata)
            addata_df=addata_df[columns]
            for value in addata_df:
                for index, row_value in addata_df.iterrows():
                    dict_rdms[value].append(row_value[value])

    if outfile is None:
        print('outputfile is saved as `rdm.pkl` in your current directory')
        pkl_rdm = open("rdm.pkl", "wb")
        pickle.dump(dict_rdms, pkl_rdm)
        pkl_rdm.close()
    else:
        outfile = outfile
        print('outputfile is saved as `%s.pkl` in your current directory' % outfile)
        pkl_rdm = open("%s.pkl" % outfile, "wb")
        pickle.dump(dict_rdms, pkl_rdm)
        pkl_rdm.close()
