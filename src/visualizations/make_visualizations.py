import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def create_bar_col_binary(metadata, col_name):
    """Create bar graph for disease outcomes

    Args:
        metadata (_type_): _description_
        col_name (_type_): _description_
    """
    ax = metadata[col_name].value_counts().sort_index(ascending=False).plot(kind='barh')
    ax.set_xlabel('count')
    ax.set_ylabel('outcome')
    ax.set_title(col_name)
    
def disease_counts_graph(metadata, disease_cols):
    ax = metadata[disease_cols].sum().sort_values(ascending=False).plot(kind='bar')
    ax.set_ylabel('count')
    ax.set_title('Disease counts')

def co_occurence_graph(metadata, disease_cols):
    disease_data = metadata[disease_cols]
    co_matrix = disease_data.T.dot(disease_data)
    sns.heatmap(co_matrix)
    
def total_disease_count_graphs(metadata, disease_cols):
    total_disease_counts = metadata[disease_cols].sum(axis=1)
    ax = total_disease_counts.value_counts().sort_values(ascending=False).plot(kind='barh')
    ax.set_title('Disease Per Sample Counts')
    ax.set_ylabel('Num of Unique Diseases')
    ax.set_xlabel('Num of Samples')