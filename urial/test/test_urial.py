import numpy as np
import pandas as pd

from urial.utils import rdm_concat_df
from urial.rdm import gen_model_rdm, rdm_avg


def test_gen_model_rdm():

    model='all_separate'
    conds = 10
    actual = np.diagonal(gen_model_rdm(model, conds))
    expected = np.array([0] * conds)
    np.testing.assert_array_equal(actual,expected)



def test_rdm_avg():

    df_1 = pd.DataFrame({'cond_1' : [0, 1, 1], 'cond_2' : [1,0,1], 'cond_3' : [1,1,0]})
    df_2 = pd.DataFrame({'cond_1' : [0, 2, 2], 'cond_2' : [2,0,2], 'cond_3' : [2,2,0]})
    l_df = rdm_concat_df(rdm_list=[df_1, df_2], sub_ids=['01', '02'])
    avg_rdm = rdm_avg(l_df)
    actual = avg_rdm.to_numpy()
    expected = np.array([0, 1.5, 1.5, 1.5, 0, 1.5, 1.5, 1.5, 1.5]).reshape(3, 3)
    np.testing.assert_array_equal(actual,expected)
