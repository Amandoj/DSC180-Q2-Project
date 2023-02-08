from qiime2 import Artifact
from qiime2 import Metadata

import pandas as pd
import biom

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
    return Metadata.load(path)

def feature_table_biom_view(feature_table):
    return feature_table.view(biom.Table)