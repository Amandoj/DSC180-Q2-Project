import numpy as np
import pandas as pd

def missing_values(col, col_type='categorical'):
    """Crete unified representation for missing values

    Args:
        col (Series): _description_
        type (str, optional): _description_. Defaults to 'categorical'.

    Returns:
        _type_: _description_
    """
    temp = col.apply(lambda x: np.nan if x == 'not applicable' or x == 'not provided' else x)
    if col_type == 'numeric':
        temp = temp.apply(lambda x: x if pd.isnull(x) else np.float64(x))
    return temp


def replace_missing_values(df):
    updated_df = df.apply(lambda x: missing_values(x,'numeric'))
    return updated_df