def rdm_mat2csv(matfile, key, name=None, path=None, columns=None):
    '''function to convert RDM from mat file to csv'''

    from os.path import join as opj
    from scipy.io.matlab import loadmat
    import pandas as pd
    from scipy.spatial.distance import squareform

    mat = loadmat(matfile)

    global rdm

    if len(mat[key][0]) == len(mat[key][1]):
        rdm = pd.DataFrame(mat[key])
    else:
        rdm = squareform(mat[key][0])
        rdm = pd.DataFrame(rdm)

    if columns == None:
        print('no column names list provided')
    else:
        rdm.columns = columns

    if name == None:
        name = matfile.split(',')[0]
        name = name[(name.rfind('/')+1):name.rfind('.')]

    if path == None:
        path = matfile.split(',')[0]
        path = path[0:path.rfind('/')]

    rdm.to_csv(opj(path, name + '_rdm.csv'), index=False)

    return(rdm)
