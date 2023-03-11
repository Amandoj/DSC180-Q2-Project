import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_bar_col_binary(metadata_df, disease_col_name):
    """Create bar graph of outcomes for given disease type

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_col (String): Disease type name
    """
    outcomes = metadata_df[disease_col_name].value_counts().sort_index(ascending=False)
    ax = sns.barplot(x=outcomes.index,y=outcomes.values)
    ax.set_xlabel('count')
    ax.set_ylabel('outcome')
    ax.set_title(disease_col_name)
    
def disease_counts_graph(metadata_df, disease_cols):
    """Creates bar graph of disease counts

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_cols (List): List of disease columns
    """
    plt.figure(figsize=(22,8))
    sns.set(font_scale=2)
    disease_counts = metadata_df[disease_cols].sum()
    ax = sns.barplot(x=disease_counts.index,y=disease_counts.values)
    ax.set_ylabel('Count')
    ax.set_title('Disease counts')
    ax.set_xlabel('Disease Type')
    ax.tick_params(axis='x', labelrotation = 0)
    plt.savefig('data/out/disease_counts.png', bbox_inches='tight',dpi=300)

    
def total_disease_count_graph(metadata_df, disease_cols):
    """Create bar graph of total disease counts within samples

    Args:
        metadata_df (DataFrame): Metadata containing data about disease targets 
        disease_cols (List): List of disease columns
    """
    plt.figure(figsize=(8,9))
    total_disease_counts = metadata_df[disease_cols].sum(axis=1).value_counts().sort_values(ascending=False)
    ax = sns.barplot(x=total_disease_counts.index, y=total_disease_counts.values, palette=sns.color_palette("ch:s=.25,rot=-.25",n_colors=7))
    ax.set_title('Samples with multiple diseases')
    ax.tick_params(axis='x', labelrotation = 0)
    ax.set_ylabel('Number of samples')
    ax.set_xlabel('Number of diseases')
    plt.savefig('data/out/total_disease_counts.png', bbox_inches='tight',dpi=300)
    
def binary_relevance_accuracy_scores_graph(disease_accuracy_scores):
    """Create bar graph of accuracy scores of binary relevance model

    Args:
        disease_accuracy_scores (Dict): Dictionary containing scores of model accuracy scores by disease type
    """
    plt.figure(figsize=(12,4))
    ax = sns.barplot(x=list(disease_accuracy_scores.keys()), y=list(disease_accuracy_scores.values()))
    ax.set_xlabel('Disease Type')
    ax.set_title('Gradient Boosting Classifier Accuracy Scores')
    ax.set_ylabel('Accuracy Score')
    plt.tight_layout()
    plt.savefig('data/out/GBC_accuracy_scores.png',bbox_inches='tight',dpi=300)
