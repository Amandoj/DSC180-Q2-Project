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
    ax = metadata_df[disease_cols].sum().sort_values(ascending=False).plot(kind='bar', color = sns.color_palette())
    ax.set_ylabel('Count')
    ax.set_title('Disease counts')
    ax.set_xlabel('Disease Type')
    plt.savefig('data/out/disease_counts.png', bbox_inches='tight')

def co_occurence_graph(metadata_df, disease_cols):
    """Create Co-occurence graph between disease types

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_cols (List): List of disease columns
    """
    disease_data = metadata_df[disease_cols]
    co_matrix = disease_data.T.dot(disease_data)
    sns.heatmap(co_matrix)
    plt.savefig('data/out/co_occurence.png', bbox_inches='tight')
    
def total_disease_count_graph(metadata_df, disease_cols):
    """Create bar graph of total disease counts within samples

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_cols (List): List of disease columns
    """
    total_disease_counts = metadata_df[disease_cols].sum(axis=1)
    ax = total_disease_counts.value_counts().sort_values(ascending=False).plot(kind='bar', color = sns.color_palette("ch:s=.25,rot=-.25",n_colors=8))
    ax.set_title('Samples with multiple diseases')
    ax.tick_params(axis='x', labelrotation = 0)
    ax.set_ylabel('Number of samples')
    ax.set_xlabel('Number of diseases')
    plt.savefig('data/out/total_disease_counts.png', bbox_inches='tight')
    
def binary_relevance_accuracy_scores_graph(disease_accuracy_scores):
    plt.figure(figsize=(12,4))
    ax = sns.barplot(x=list(disease_accuracy_scores.keys()), y=list(disease_accuracy_scores.values()))
    ax.set_xlabel('Disease Type')
    ax.set_title('Gradient Boosting Classifier Accuracy Scores')
    ax.set_ylabel('Accuracy Score')
    plt.tight_layout()
    plt.savefig('data/out/GBC_accuracy_scores.png')
    plt.show()
