import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_bar_col_binary(df, col_name):
    ax = df[col_name].value_counts().sort_index(ascending=False).plot(kind='barh')
    ax.set_xlabel('count')
    ax.set_ylabel('outcome')
    ax.set_title(col_name)
    
def disease_counts_graph(metadata, disease_cols):
    metadata[disease_cols].sum().sort_values(ascending=False).plot(kind='bar')