from qiime2.plugins.diversity.pipelines import core_metrics
from qiime2.plugins.diversity.pipelines import core_metrics_phylogenetic
from qiime2.plugins.diversity.visualizers import beta_group_significance
from qiime2.plugins.diversity.methods import umap
from qiime2.plugins.emperor.visualizers import plot


def extract_core_metrics(feat_table, depth, metadata, phylogeny=None):
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
    if phylogeny == None:
        metrics = core_metrics(feat_table, depth, metadata)
        return metrics
    else:
        metrics = core_metrics_phylogenetic(feat_table, depth, metadata)
        return metrics
    

def extract_distance_matrices(metrics):
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



def extract_pcoa_results(metrics):
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



def extract_umap_results(distance_matrix, n_dim, n_neighbors, min_dist=0.4, random_seed=1):
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

def extract_pcoa_emperor_vis(metrics):
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

def extract_umap_vis(umap_matrix, metadata):
    '''
    Returns the emperor visualization objects (in .qzv format)
    
    Parameters
    ----------
    biplot : PCoAResults % Properties('biplot')
        The principal coordinates matrix to be plotted.
    sample_metadata : Metadata
        The sample metadata
    feature_metadata : Metadata, optional
        The feature metadata (useful to manipulate the arrows in the plot).
        
        
    Returns
    -------
    visualization : Visualization
    '''
    umap_vis = plot(umap_matrix, metadata)
    
    return umap_vis

def permanova_test(u_unifrac_dis_matrix, w_unifrac_dis_matrix, metadata_col):
    """Perform permanova test on given metadata column using both unweighted and weighted unifrac distance matrix

    Args:
        u_unifrac_dis_matrix (DistanceMatrix): _description_
        w_unifrac_dis_matrix (DistanceMatrix): _description_
        metadata_col (_type_): _description_
    """
    u_unifrac_permanova_result = beta_group_significance(u_unifrac_dis_matrix, metadata_col, method='permanova')
    u_unifrac_permanova_result.visualization.save('data/out/u_unifrac_permanova_test_'+metadata_col.name)
    
    w_unifrac_permanova_result = beta_group_significance(w_unifrac_dis_matrix, metadata_col, method='permanova')
    w_unifrac_permanova_result.visualization.save('data/out/w_unifrac_permanova_test_'+metadata_col.name)

def permanova_test_all_diseases(u_unifrac_dis_matrix, w_unifrac_dis_matrix, metadata, disease_targets):
    """Perform permanova test on all disease columns

    Args:
        u_unifrac_dis_matrix (_type_): _description_
        w_unifrac_dis_matrix (_type_): _description_
        metadata (_type_): _description_
        disease_targets (_type_): _description_
    """
    disease_cols = [metadata.get_column(disease) for disease in disease_targets]
    
    for metadata_disease_col in disease_cols:
        permanova_test(u_unifrac_dis_matrix, w_unifrac_dis_matrix, metadata_disease_col)