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

def represents_float(s):
    try: 
        np.float64(s)
    except ValueError:
        return False
    else:
        return True

def unified_rep_values(col):
    """Creates unified representation of numbers as only floats. Can only be used on numeric columns.

    Args:
        col (_type_): _description_

    Returns:
        _type_: _description_
    """
    temp = col.apply(lambda x: np.float64(x) if represents_float(x) else x)
    return temp



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
    """Changing binary 0-1 to true-false

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
        return val
    
    
def organize_metadata(metadata, disease_cols, additional_info_cols, diabetes_binary, ckd_binary):
    features = disease_cols + additional_info_cols
    
    # Drop na, 'not applicable' and 'not provided'
    sub_metadata = metadata[features].apply(lambda x: missing_values(x), axis = 1)
    sub_metadata = sub_metadata.dropna()
    # unified values
    sub_metadata = sub_metadata.apply(lambda x: unified_rep_values(x))
    # change categorical to binary - will try to abstract this process
    sub_metadata['diabetes2_v2'] = sub_metadata['diabetes2_v2'].apply(lambda x: eval(diabetes_binary)[x])
    sub_metadata['ckd_v2'] = sub_metadata['ckd_v2'].apply(lambda x: eval(ckd_binary)[x])
    sub_metadata.to_csv("data/temp/final_metadata.tsv", sep="\t")
    # create seperate file for tf metadata - will be used for qiime models
    sub_metadata_df = disease_metadata_to_tf(sub_metadata, disease_cols)
    
    return sub_metadata, sub_metadata_df

def disease_metadata_to_tf(sub_metadata, disease_cols):
    """Convert metadata df 0-1 binary to T-F binary

    Args:
        metadata (_type_): _description_
        disease_cols (_type_): _description_
    """
    metadata_df = sub_metadata.copy()
    metadata_df.loc[:,disease_cols] = metadata_df.loc[:,disease_cols].applymap(lambda x: binary_to_tf(x))
    metadata_df.to_csv("data/temp/final_metadata_disease_tf.tsv",sep="\t")
    return metadata_df