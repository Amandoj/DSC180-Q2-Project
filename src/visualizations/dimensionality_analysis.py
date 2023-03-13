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


def extract_core_metrics_phylogenetic(feat_table, phylogeny, depth, metadata):
    '''
    Applies a collection of diversity metrics (both phylogenetic and non-
    phylogenetic) to a feature table. Returns the 'metrics' object that can be used for various analyses.

    Parameters
    ----------
    table : FeatureTable[Frequency]
        The feature table containing the samples over which diversity metrics
        should be computed.
    phylogeny : Phylogeny[Rooted] (if provided)
        Phylogenetic tree containing tip identifiers that correspond to the
        feature identifiers in the table. This tree can contain tip ids that
        are not present in the table, but all feature ids in the table must be
        present in this tree.
    sampling_depth : Int % Range(1, None)
        The total frequency that each sample should be rarefied to prior to
        computing diversity metrics.
    metadata : Metadata
        The sample metadata to use in the emperor plots.

    Returns
    -------
    rarefied_table : FeatureTable[Frequency]
        The resulting rarefied feature table.
    faith_pd_vector : SampleData[AlphaDiversity]
        Vector of Faith PD values by sample.
    observed_features_vector : SampleData[AlphaDiversity]
        Vector of Observed Features values by sample.
    shannon_vector : SampleData[AlphaDiversity]
        Vector of Shannon diversity values by sample.
    evenness_vector : SampleData[AlphaDiversity]
        Vector of Pielou's evenness values by sample.

    '''
#     if phylogeny == None:
#         metrics = core_metrics(feat_table, depth, metadata)
#         return metrics
#     else:
    metrics = core_metrics_phylogenetic(feat_table, phylogeny, depth, metadata)
    return metrics

def extract_core_metrics(feat_table, depth, metadata):
    '''
    Applies a collection of diversity metrics (both phylogenetic and non-
    phylogenetic) to a feature table. Returns the 'metrics' object that can be used for various analyses.

    Parameters
    ----------
    table : FeatureTable[Frequency]
        The feature table containing the samples over which diversity metrics
        should be computed.
 
    sampling_depth : Int % Range(1, None)
        The total frequency that each sample should be rarefied to prior to
        computing diversity metrics.
    metadata : Metadata
        The sample metadata to use in the emperor plots.

    Returns
    -------
    rarefied_table : FeatureTable[Frequency]
        The resulting rarefied feature table.
    faith_pd_vector : SampleData[AlphaDiversity]
        Vector of Faith PD values by sample.
    observed_features_vector : SampleData[AlphaDiversity]
        Vector of Observed Features values by sample.
    shannon_vector : SampleData[AlphaDiversity]
        Vector of Shannon diversity values by sample.
    evenness_vector : SampleData[AlphaDiversity]
        Vector of Pielou's evenness values by sample.

    '''
#     if phylogeny == None:
#         metrics = core_metrics(feat_table, depth, metadata)
#         return metrics
#     else:
    metrics = core_metrics(feat_table, depth, metadata)
    return metrics
    

def extract_distance_matrices(metrics):
    '''
    Returns
    --------

    jaccard_distance_matrix : DistanceMatrix
        Matrix of Jaccard distances between pairs of samples.
    bray_curtis_distance_matrix : DistanceMatrix
        Matrix of Bray-Curtis distances between pairs of samples.
    '''
    jaccard_dis_matrix = metrics.jaccard_distance_matrix
    bc_dis_matrix = metrics.bray_curtis_distance_matrix
    
    return  jaccard_dis_matrix, bc_dis_matrix    
    


def extract_pcoa_results(metrics):
    '''
    Returns
    --------

    jaccard_pcoa_results : PCoAResults
        PCoA matrix computed from Jaccard distances between samples.
    bray_curtis_pcoa_results : PCoAResults
        PCoA matrix computed from Bray-Curtis distances between samples.
    '''

    jaccard_pcoa_results = metrics.jaccard_pcoa_results
    bray_curtis_pcoa_results = metrics.bray_curtis_pcoa_results
    
    return jaccard_pcoa_results, bray_curtis_pcoa_results



def extract_pcoa_emperor_vis(metrics):
    '''
    Returns the emperor visualization objects (in .qzv format) that can be used to view the PCoA matrix plots
    
    Returns
    -------

    jaccard_emperor : Visualization
        Emperor plot of the PCoA matrix computed from Jaccard.
    bray_curtis_emperor : Visualization
        Emperor plot of the PCoA matrix computed from Bray-Curtis.
        '''
    
    jaccard_emperor = metrics.jaccard_emperor
    bray_curtis_emperor = metrics.bray_curtis_emperor
    
    return jaccard_emperor, bray_curtis_emperor


def extract_distance_matrices_t(metrics):
    '''
    Returns
    --------
    unweighted_unifrac_distance_matrix : DistanceMatrix
        Matrix of unweighted UniFrac distances between pairs of samples.
    weighted_unifrac_distance_matrix : DistanceMatrix
        Matrix of weighted UniFrac distances between pairs of samples.
    jaccard_distance_matrix : DistanceMatrix
        Matrix of Jaccard distances between pairs of samples.
    bray_curtis_distance_matrix : DistanceMatrix
        Matrix of Bray-Curtis distances between pairs of samples.
    '''
    jaccard_dis_matrix = metrics.jaccard_distance_matrix
    bc_dis_matrix = metrics.bray_curtis_distance_matrix
    u_unifrac_dis_matrix = metrics.unweighted_unifrac_distance_matrix
    w_unifrac_dis_matrix = metrics.weighted_unifrac_distance_matrix
    
    return u_unifrac_dis_matrix, w_unifrac_dis_matrix, jaccard_dis_matrix, bc_dis_matrix

def extract_pcoa_results_t(metrics):
    '''
    Returns
    --------
    unweighted_unifrac_pcoa_results : PCoAResults
        PCoA matrix computed from unweighted UniFrac distances between samples.
    weighted_unifrac_pcoa_results : PCoAResults
        PCoA matrix computed from weighted UniFrac distances between samples.
    jaccard_pcoa_results : PCoAResults
        PCoA matrix computed from Jaccard distances between samples.
    bray_curtis_pcoa_results : PCoAResults
        PCoA matrix computed from Bray-Curtis distances between samples.
    '''
    
    unweighted_unifrac_pcoa_results = metrics.unweighted_unifrac_pcoa_results
    weighted_unifrac_pcoa_results = metrics.weighted_unifrac_pcoa_results
    jaccard_pcoa_results = metrics.jaccard_pcoa_results
    bray_curtis_pcoa_results = metrics.bray_curtis_pcoa_results
    
    return unweighted_unifrac_pcoa_results, weighted_unifrac_pcoa_results, jaccard_pcoa_results, bray_curtis_pcoa_results



def extract_umap_results_t(distance_matrix, n_dim, n_neighbors, min_dist=0.4, random_seed=1):
    '''
    Parameters
    ----------
    distance_matrix : DistanceMatrix
        The distance matrix on which UMAP should be computed.
    number_of_dimensions : Int % Range(2, None), optional
        Dimensions to reduce the distance matrix to.
    n_neighbors : Int % Range(1, None), optional
        Provide the balance between local and global structure. Low values
        prioritize the preservation of local structures. Large values sacrifice
        local details for a broader global embedding.
    min_dist : Float % Range(0, None), optional
        Controls the cluster size. Low values cause clumpier clusters. Higher
        values preserve a broad topological structure. To get less overlapping
        data points the default value is set to 0.4. For more details visit:
        https://umap-learn.readthedocs.io/en/latest/parameters.html
    random_state : Int, optional
        Seed used by random number generator.
    
    Returns
    -------
    umap : PCoAResults
    The resulting UMAP matrix.
    '''
    umap_results = umap(distance_matrix, n_dim, n_neighbors, min_dist, random_seed)

    return umap_results

def extract_pcoa_emperor_vis_t(metrics):
    '''
    Returns the emperor visualization objects (in .qzv format) that can be used to view the PCoA matrix plots
    
    Returns
    -------
    unweighted_unifrac_emperor : Visualization
        Emperor plot of the PCoA matrix computed from unweighted UniFrac.
    weighted_unifrac_emperor : Visualization
        Emperor plot of the PCoA matrix computed from weighted UniFrac.
    jaccard_emperor : Visualization
        Emperor plot of the PCoA matrix computed from Jaccard.
    bray_curtis_emperor : Visualization
        Emperor plot of the PCoA matrix computed from Bray-Curtis.
        '''
    
    unweighted_unifrac_emperor = metrics.unweighted_unifrac_emperor
    weighted_unifrac_emperor = metrics.weighted_unifrac_emperor
    jaccard_emperor = metrics.jaccard_emperor
    bray_curtis_emperor = metrics.bray_curtis_emperor
    
    return unweighted_unifrac_emperor, weighted_unifrac_emperor, jaccard_emperor, bray_curtis_emperor

def save_pcoa_outputs(metrics):
    ''' Save all the PCoA Matrices and PCoA Emperor Plots that are in .qzv format to view on the web'''
    
    #PCoA coordinates embedding 
    unweighted_unifrac_pcoa_results, weighted_unifrac_pcoa_results, jaccard_pcoa_results, bray_curtis_pcoa_results = extract_pcoa_results_t(metrics)

    #3D PCoA Plots using Qiime2 Emperor plotting library
    unweighted_unifrac_emperor, weighted_unifrac_emperor, jaccard_emperor, bray_curtis_emperor = extract_pcoa_emperor_vis_t(metrics)
        
    jaccard_pcoa_results.save('outputs/jac_pcoa_matrix')
    bray_curtis_pcoa_results.save('outputs/bc_pcoa_matrix')
    unweighted_unifrac_pcoa_results.save('outputs/u_unifrac_pcoa_matrix')
    weighted_unifrac_pcoa_results.save('outputs/w_unifrac_pcoa_matrix')
    
    jaccard_emperor.save('outputs/jac_pcoa_emp')
    bray_curtis_emperor.save('outputs/bc_pcoa_emp')
    unweighted_unifrac_emperor.save('outputs/u_unifrac_pcoa_emp')
    weighted_unifrac_emperor.save('outputs/w_unifrac_pcoa_emp')
    
    return


def process_table_umap(table, metadata_df):
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
    filtered_metadata_df = metadata_df.drop(['hispanic_origin', 'agegroup_c6_v2'], axis=1)
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

