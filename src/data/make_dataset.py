from qiime2 import Artifact
from qiime2 import Metadata
from qiime2.plugins.feature_table.methods import filter_features

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

def filter_feature_table(feature_table, min_frequency):
    """Filter Feature table

    Args:
        feature_table (FeatureTable[Frequency]): Feature table that will be filtered
        min_frequency (int): The minimum total frequency a feature must retain 

    Returns:
        FeatureTable[Frequency]: Filtered table
    """
    return filter_features(feature_table, min_frequency = min_frequency).filtered_table