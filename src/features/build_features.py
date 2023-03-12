from qiime2 import Metadata

import numpy as np
import pandas as pd

def missing_values(col):
    """Create unified representation for missing values

    Args:
        col (Series): Column containing multiple representations of missing values

    Returns:
        Series: Column with a unified representation (NaN) of missing values
    """
    temp = col.apply(lambda x: np.nan if x == 'not applicable' or x == 'not provided' else x)
    return temp

def represents_float(s):
    """Identify if string is a float number

    Args:
        s (String): String that will be analyzed 

    Returns:
        Boolean: Whether or not given string represents a float number
    """
    try: 
        np.float64(s)
    except ValueError:
        return False
    else:
        return True

def unified_rep_values(col):
    """Creates unified representation of numbers as only floats. Can only be used on numeric columns.

    Args:
        col (Series): Column with integer and float numbers

    Returns:
        Series: Column with only float numbers
    """
    temp = col.apply(lambda x: np.float64(x) if represents_float(x) else x)
    return temp



def cat_to_binary(col, values):
    """Changing categorical variables to binary variables

    Args:
        col (Series): Column with categorical varibales
        values (Dict): Dictionary to map categorical values to binary values
        
    Returns:
        Series: Column of binary values
    """
    binary_col = col.apply(lambda x: values[x])
    return binary_col 

def binary_to_tf(val):
    """Changing binary 0-1 to false-true

    Args:
        val (Float): Float that will be converted to true or false

    Returns:
        String: 'T' or 'F' depending on initial value
    """
    if val == 1.0:
        return 'T'
    elif val == 0.0:
        return 'F'
    else:
        return val
    
    
def organize_metadata(metadata_df, feauture_table_samples, disease_cols, additional_info_cols, diabetes_binary, ckd_binary):
    """Organizes metadata_df by dropping missing values and converting categorical variables to binary variables.

    Args:
        metadata_df (DataFrame): Metadata dataframe that will be organized
        disease_cols (List): List of disease column names 
        additional_info_cols (List): List of additional metadata columns
        diabetes_binary (Dict): Dictionary of diabetes mappings
        ckd_binary (Dict): Dictionary of ckd mappings

    Returns:
        List: Returns two dataframes, final_metadata which contains orginal disease binary representation of 0/1 
        and final_metadata_tf which contains disease data as 'T' and 'F' binary values
    """
    features = disease_cols + additional_info_cols
    # Drop na, 'not applicable' and 'not provided'
    sub_metadata = metadata_df[features].apply(lambda x: missing_values(x), axis = 1)
    # only drop rows with missing disease data
    sub_metadata = sub_metadata.dropna(subset = disease_cols)
    
    # unified values
    sub_metadata = sub_metadata.apply(lambda x: unified_rep_values(x))
    
    # change categorical to binary - will try to abstract this process
    sub_metadata['diabetes2_v2'] = sub_metadata['diabetes2_v2'].apply(lambda x: eval(diabetes_binary)[x])
    sub_metadata['ckd_v2'] = sub_metadata['ckd_v2'].apply(lambda x: eval(ckd_binary)[x])
    
    # Filter metadata samples based on those that exist in the feature table
    final_metadata = sub_metadata.loc[sub_metadata.index.isin(feauture_table_samples)]
    # save file for 0-1 metadata - will be used for visualizations
    final_metadata.to_csv('data/temp/final_metadata.tsv',sep='\t')
    # create seperate file for tf metadata - will be used for qiime models
    final_metadata_tf = disease_metadata_to_tf(final_metadata, disease_cols)
    
    return final_metadata, final_metadata_tf

def disease_metadata_to_tf(final_metadata, disease_cols):
    """Convert metadata dataframe 0-1 binary to T-F binary

    Args:
        metadata (DataFrame): Dataframe with 0-1 binary values
        disease_cols (List): List of disease types
    
    Returns:
        DataFrame: Dataframe with T and F values
    """
    metadata_df = final_metadata.copy()
    metadata_df.loc[:,disease_cols] = metadata_df.loc[:,disease_cols].applymap(lambda x: binary_to_tf(x))
    metadata_df.to_csv("data/temp/final_metadata_tf.tsv",sep="\t")
    return metadata_df

def balance_precvd(organized_metadata_tf):
    """Balance PreCVD Classes

    Args:
        organized_metadata_tf (DataFrame): Organized metadata dataframe

    Returns:
        METADATA: Balanced PreCVD qiime Metadata Object
    """
    precvd_undersample = organized_metadata_tf[['precvd_v2']]
    balanced_precvd_df = pd.concat([precvd_undersample[precvd_undersample['precvd_v2'] == 'T'],
                                    precvd_undersample[precvd_undersample['precvd_v2'] == 'F'].sample(
                                    precvd_undersample.value_counts().min(), random_state=2)])
    balanced_precvd_df.to_csv('data/out/balanced_precvd_samples.tsv', sep='\t')
    balanced_precvd_qiime = Metadata(balanced_precvd_df)
    return balanced_precvd_qiime