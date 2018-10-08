def gen_model_rdm(model, cond, columns=None, name=None, path=None):
    '''function to generate model RDMs, more preciseley
        hypothesis based conceptual models'''

    import pandas as pd
    import numpy as np
    import os

    if model is None:
        print('You need to specify what kind of model you want to generate.'
              'The current options are: all_separate & random')
    elif model == 'all_separate':
        model_rdm = pd.DataFrame(np.ones((cond, cond), int))
        np.fill_diagonal(model_rdm.values, 0)
    elif model == 'random':
        model_rdm = np.random.rand(cond, cond)
        model_rdm = pd.DataFrame(np.tril(model_rdm) + np.tril(model_rdm, -1).T)
        np.fill_diagonal(model_rdm.values, 0)

    if columns is None:
        print('no condition names will be added to the dataframe')
    elif columns is not None:
        model_rdm.columns=columns
        print('conditions names will be added to the dataframe as specified')

    if path is None:
        print('model RDM will not be saved')
    elif path is not None:
        if name is None:
            if path is None:
                print('model RDM  is saved as `model_rdm.csv` in your current directory')
                model_rdm.to_csv('model_rdm.csv', index=False)
            elif path is not None:
                path=path
                print('model RDM  is saved as `model_rdm.csv` in %s' % path)
                model_rdm.to_csv(os.path.join(os.getcwd(), 'model_rdm.csv'), index=False)
        elif name is not None:
            name=name
            if path is None:
                print('model RDM  is saved as `%s.csv` in your current directory' % name)
                model_rdm.to_csv('%s.csv', index=False % name)
            elif path is not None:
                path=path
                print('model RDM is saved as `%s.csv` in %s' %(name, path))
                model_rdm.to_csv(os.path.join(path, '%s.csv' % name), index=False)

    return model_rdm
