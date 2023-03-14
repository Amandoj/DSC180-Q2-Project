from qiime2.plugins.diversity.pipelines import core_metrics
from qiime2.plugins.diversity.pipelines import core_metrics_phylogenetic
from qiime2.plugins.diversity.methods import umap
from qiime2.plugins.emperor.visualizers import plot
from qiime2.plugins.feature_table.methods import filter_samples
from qiime2 import Metadata

import umap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_pcoa(pcoa, metadata, metric):
    plot(pcoa=pcoa, metadata=metadata).visualization.save('outputs/'+metric+'_pcoa_emp')

def plot_multiple_pcoa(pcoa_results, metadata):
    for metric in pcoa_results.keys():
        pcoa = pcoa_results[metric]
        plot_pcoa(pcoa, metadata, metric)
        
def process_table_umap(table, metadata_df, disease_cols):
    '''
    Process the feature table by mapping disease labels into parameters for the UMAP algorithm

    Parameters
    ----------
    table

    metadata_df
    
    Returns
    -------
    feature_df_target_disease: Feature table in Pandas dataframe format, that has been filtered with the metadata of samples with only 1 target disease
    target_disease_mapped: Metadata information that has been processed to only include the target disease types and sample ID, mapped to the numeric encoding of the disease type (e.g, 1,2,3,4 or 5)
    target_disease_dict: The dictionary of the mapping of target disease
    '''
    filtered_metadata_df = metadata_df[disease_cols]
    filtered_metadata_df = filtered_metadata_df[(filtered_metadata_df.sum(axis=1) == 1)] #We have around 300 samples left
    
    #Convert binary columns into a single categorical target column for disease type
    filtered_metadata_df["target_disease"] = filtered_metadata_df.idxmax(axis=1)

    #Get the target disease and sample name,then create the metadata and filterd feature table
    target_disease = filtered_metadata_df['target_disease']
    target_disease.to_csv('data/temp/target_disease.tsv', sep="\t")

    metadata_target_disease = Metadata.load("data/temp/target_disease.tsv") 
    feature_table_target_disease = filter_samples(table, metadata = metadata_target_disease).filtered_table

    #View as a DF to perform cleaning
    feature_df_target_disease = feature_table_target_disease.view(pd.DataFrame)
    feature_df_target_disease = feature_df_target_disease[feature_df_target_disease.columns[((feature_df_target_disease > 0).sum() > 3)]] #Dropping features that appear in less than 3 samples
    
    #Rename disease labels for better readability
    target_disease_renamed = {'abdominal_obesity_ncep_v2': 'Obesity',
    'ckd_v2': 'CKD',
    'dyslipidemia_v2': 'Dyslipidemia',
    'elevated_bp_selfmeds_v2': 'Elevated BP',
    'diabetes2_v2': 'Diabetes'}
    target_disease = target_disease.map(target_disease_renamed)

    #Convert target disease into categorical numbers
    target_disease_dict = {}

    for i in range(len(target_disease.unique())):
        target_disease_dict[target_disease.unique()[i]] = i

    #Map the target diseases
    target_disease_mapped = target_disease.map(target_disease_dict)

    return feature_df_target_disease, target_disease_mapped, target_disease_dict 


def umap_plot_supervised(feature_table, target, target_dict,n_neighbors, n_components, metric):
    '''
    Perform supervised UMAP on the Single Disease samples, returns the embedding and save the matplotlib plot in .png format
    '''
    embedding = umap.UMAP(n_neighbors=n_neighbors, n_components= n_components,metric=metric, random_state=10).fit_transform(feature_table, y=target)
    fig, ax = plt.subplots(1, figsize=(7, 4))
    plt.scatter(*embedding.T, s=10, c=target, cmap='rainbow', alpha=1.0)
    plt.setp(ax, xticks=[], yticks=[])
    cbar = plt.colorbar(boundaries=np.arange(6)-0.5)
    cbar.set_ticks(np.arange(5))
    cbar.set_ticklabels(target_dict.keys())
    
    plt.title(
    "Sample Size: 324",
    fontsize=7,
    pad=6.5,
    loc="left",
    )
    plt.suptitle(
    'UMAP single-disease types (n_neighbors:{0}, {1} metric)'.format(n_neighbors, metric),
    fontsize=11,
    fontweight="bold",
    x=0.122,
    y=0.97,
    ha="left",
    )
    plt.savefig('outputs/umap_supervised.png', dpi=300)
    return embedding

