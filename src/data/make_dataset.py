from qiime2.plugins import feature_table
from qiime2 import Artifact

import numpy as np
import pandas as pd

def read_feature_table(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    feature_table = Artifact.load(path)
    return feature_table

def read_metadata(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO Might need to convert to qiime2 metadata object 
    # to make it easier to use with Artifact API
    return pd.read_csv(path, sep='\t',index_col=0)

def missing_values(col, type):
    """Creates a single representation for missing values

    Args:
        col (Series): column that needs to be analyzed
        type (String): data type of column

    Returns:
        Series: Series containing single representation for missing values
    """
    temp = col.apply(lambda x: np.nan if x == 'not applicable' or x == 'not provided' else x)
    if type == 'numeric':
        temp = temp.apply(lambda x: x if pd.isnull(x) else np.float64(x))
    return temp