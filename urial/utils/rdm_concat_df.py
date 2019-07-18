def rdm_concat_df(rdm_list=None, sub_ids=None, outfile=None, prefix=None):
    '''function to create an dictionary containing
        all RDMs from a given dictory'''

    from glob import glob
    import pandas as pd
    import json

    ids = []
    rdms =[]

    if isinstance(rdm_list, str) is False:
            if sub_ids is None:
                print('Please provide a list of subject identifiers that corresponds to the list of RDMs you indicated.')
            elif len(sub_ids) != len(rdm_list):
                print('The lengths of the RDM and subject identifier lists do not match, please check again.')
            elif len(sub_ids) == len(rdm_list):
                print('You provided the following subject identifiers:')
                print(*sub_ids, sep="\n")
                ids = sub_ids
                rdms = rdm_list
    elif isinstance(rdm_list, str) is True:
            if prefix is None:
                list_rdms=glob(rdm_list + '*.csv')
            else:
                list_rdms=glob(rdm_list + prefix + '*.csv')

            for file in list_rdms:
                ids.append(file[(file.rfind('/') + 1):file.rfind('.')])
                rdms.append(pd.read_csv(file))

    dict_rdms = {}

    for ind, id in enumerate(ids):
        dict_rdms[str(id)] = rdms[ind]

    if outfile is None:
        print('No output file provided.')
        print('Hence, the resulting dictionary containing the list of subject specific RDMs will not be saved automatically.')
    elif outfile:
        dict_rdms_out = {}
        for ind, id in enumerate(ids):
        dict_rdms_out[str(id)] = rdms[ind].to_json(orient='columns')
        outfile = outfile
        print('outputfile is saved as `%s.json` .' % outfile)
        with open('%s.json' % outfile, 'w') as json_file:
            json.dump(dict_rdms_out, json_file, indent=4)

    return dict_rdms

