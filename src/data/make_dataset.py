from qiime2 import Artifact
from qiime2 import Metadata
from qiime2.plugins.feature_table.methods import filter_features, filter_samples, rarefy

import pandas as pd
import biom
import skbio

def read_feature_table(path):
    """Reads Feature Table

    Args:
        path (String): Path of feature table file

    Returns:
        FeatureTable[Frequency]: Feature Table
    """
    feature_table = Artifact.load(path)
    return feature_table

def read_metadata(path):
    """Reads Metadata file

    Args:
        path (String): Path of metadata file

    Returns:
        DataFrame: Metadata in dataframe format
    """
    metadata = pd.read_csv(path, sep='\t', index_col=0)
    return metadata

def read_qiime_metadata(path):
    """Read metadata file in Qiime format

    Args:
        path (String): Path of preprocessed metadata file

    Returns:
        METADATA: Metadata as qiime object
    """
    return Metadata.load(path)

def feature_table_biom_view(feature_table):
    """Reads feature table as biom table. Used to visualize feature table.

    Args:
        feature_table (FeatureTable[Frequency]): Feature table artifact

    Returns:
        biom.Table: a biom table
    """
    return feature_table.view(biom.Table)

def read_tree_table(path):
    """
    Reads the phylogeny tree table 
    
    """
    tree = skbio.TreeNode.read(path)
    tree_artifact = Artifact.import_data('Phylogeny[Rooted]', tree)
    
    return tree_artifact

def filter_feature_table(feature_table, min_samples, metadata):
    """Filter Feature table

    Args:
        feature_table (FeatureTable[Frequency]): Feature table that will be filtered
        min_samples (int): The minimum number of samples that a feature must be present in to remain

    Returns:
        FeatureTable[Frequency]: Filtered table
    """
    filtered_feature_table = filter_features(feature_table, min_samples = min_samples).filtered_table
    return filter_samples(filtered_feature_table, metadata = metadata).filtered_table


def balance_precvd(organized_metadata_tf):
    """_summary_

    Args:
        organized_metadata_tf (_type_): _description_

    Returns:
        _type_: _description_
    """
    precvd_undersample = organized_metadata_tf[['precvd_v2']]
    balanced_precvd_df = pd.concat([precvd_undersample[precvd_undersample['precvd_v2'] == 'T'],
                                    precvd_undersample[precvd_undersample['precvd_v2'] == 'F'].sample(
                                    precvd_undersample.value_counts().min(), random_state=2)])
    balanced_precvd_qiime = Metadata(balanced_precvd_df)
    return balanced_precvd_qiime