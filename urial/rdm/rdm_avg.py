def rdm_avg(list_rdms):
    '''function to compute an average rdm from all
        RDMs in a given dictionary'''


    import pandas as pd
    import numpy as np
    import json

    if isinstance(list_rdms, str) is True:
        with open(list_rdms) as json_file:
            data = json.load(json_file)

        dict_rdms = {}

        for key, value in data.items():
            dict_rdms[key] = pd.read_json(value)

    if isinstance(list_rdms, dict) is True:
        dict_rdms = list_rdms

        rdms = []

        for rdm in dict_rdms.values():
            rdms.append(rdm.to_numpy())

    avg_rdm = pd.DataFrame(np.mean(rdms, axis=0), columns=list(dict_rdms[list(dict_rdms.keys())[0]].columns))

    return avg_rdm