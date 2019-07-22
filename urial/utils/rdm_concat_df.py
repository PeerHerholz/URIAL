def rdm_concat_df(rdm_list=None, sub_ids=None, prefix=None, outfile=None):
    """
    Concatenate a list of RDMs into a dictionary (sub-id : RDM). Either a list of dataframes
    or a path can be provided.

    Parameters
    ----------
    rdm_list : list or str
        Either list of dataframes or path to directory containing .csv files. In case a list of dataframes is provided
        the order of dataframes should correspond to that of sub_ids. In case a path is provided
        the directory should contain .csv files as follows: <sub-id>_<rdm-name>.csv, e.g. sub-01_rdm.csv.
    sub_ids: list
        List of str, indicating the subjects to include. Only the identifier itself should be indicated, e.g., '01'.
    prefix: str
        Prefix of .csv files to be included, in case a path is provided in rdm_list. If None,
        all .csv files will be included.
    outfile: str
        Path and name of the dictionary. If none, the dictionary won't be saved automatically.


    Returns
    -------
    dict_rdms : dict
        Dictionary containing the RDMs of the specified subjects (subject: RDM mapping).

    Examples
    --------
    >>> rdm_concat_df('/home/urial/Desktop', ['01', '02', '03', '04'], 'sub', '/home/urial/Desktop/rdm_dict')
    dict_rdms
    """

    from glob import glob
    import pandas as pd
    import json
    from os.path import join as opj

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
                list_rdms=glob(opj(rdm_list, '*.csv'))
            else:
                list_rdms=glob(opj(rdm_list, prefix + '*.csv'))

            for rdm in list_rdms:
                ids.append(rdm[(rdm.rfind('/') + 5):rdm.rfind('_')])
                rdms.append(pd.read_csv(rdm))

    dict_rdms = {}

    for ind, id in enumerate(ids):
        dict_rdms[str(id)] = rdms[ind]

    if outfile is None:
        print('No output filename provided.')
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

