import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def create_bar_col_binary(metadata_df, disease_col):
    """Create bar graph of outcomes for given disease type

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_col (String): Disease type name
    """
    ax = metadata_df[disease_col].value_counts().sort_index(ascending=False).plot(kind='barh')
    ax.set_xlabel('count')
    ax.set_ylabel('outcome')
    ax.set_title(disease_col)
    
def disease_counts_graph(metadata_df, disease_cols):
    """Creates bar graph of disease counts

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_cols (List): List of disease columns
    """
    ax = metadata_df[disease_cols].sum().sort_values(ascending=False).plot(kind='bar')
    ax.set_ylabel('count')
    ax.set_title('Disease counts')

def co_occurence_graph(metadata_df, disease_cols):
    """Create Co-occurence graph between disease types

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_cols (List): List of disease columns
    """
    disease_data = metadata_df[disease_cols]
    co_matrix = disease_data.T.dot(disease_data)
    sns.heatmap(co_matrix)
    
def total_disease_count_graphs(metadata_df, disease_cols):
    """Create bar graph of total disease counts within samples

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_cols (List): List of disease columns
    """
    total_disease_counts = metadata_df[disease_cols].sum(axis=1)
    ax = total_disease_counts.value_counts().sort_values(ascending=False).plot(kind='barh')
    ax.set_title('Disease Per Sample Counts')
    ax.set_ylabel('Num of Unique Diseases')
    ax.set_xlabel('Num of Samples')