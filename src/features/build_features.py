import numpy as np
import pandas as pd

def missing_values(col):
    """Create unified representation for missing values

    Args:
        col (Series): _description_

    Returns:
        _type_: _description_
    """
    temp = col.apply(lambda x: np.nan if x == 'not applicable' or x == 'not provided' else x)
    return temp


def unified_rep_values(col):
    """Creates unified representation of numbers as only floats. Can only be used on numeric columns.

    Args:
        col (_type_): _description_

    Returns:
        _type_: _description_
    """
    temp = col.apply(lambda x: x if pd.isnull(x) else np.float64(x))
    return temp


def replace_df_values(df, numeric_cols):
    """_summary_

    Args:
        df (_type_): _description_
        numeric_cols (_type_): _description_

    Returns:
        _type_: _description_
    """
    updated_df = df.apply(lambda x: missing_values(x), axis = 1)
    updated_df.loc[:,numeric_cols] = updated_df.loc[:,numeric_cols].apply(lambda x: unified_rep_values(x))
    # changing dtypes of columns
    convert_dict =  {x: np.float64 for x in numeric_cols}
    sub_metadata_no_nan = sub_metadata_no_nan.astype(convert_dict)
    
    return sub_metadata_no_nan

def subset_metadata(df, features):
    """Creates subset of metadata

    Args:
        df (_type_): _description_
        features (_type_): _description_
        
    Returns:
        _type_: _description_
    """
    subset_metadata = df[features]
    return subset_metadata


def cat_to_binary(col, values):
    """Changing categorical variables to binary variables

    Args:
        col (Series): _description_
        values (Dict): _description_
        
    Returns:
        _type_: _description_
    """
    binary_col = col.apply(lambda x: values[x])
    return binary_col 

def binary_to_tf(val):
    """Changing binary 0-1 to F-T

    Args:
        val (_type_): _description_

    Returns:
        _type_: _description_
    """
    if val == 1.0:
        return 'T'
    elif val == 0.0:
        return 'F'
    else:
        return 'missing'