from qiime2.plugins.diversity.pipelines import core_metrics, core_metrics_phylogenetic,beta_phylogenetic,beta
from qiime2.plugins.diversity.visualizers import beta_group_significance
from qiime2.plugins.diversity.methods import pcoa

# def calculate_distance_matrix(feature_table, metric):
#     """Calculate distance matrix based on given metric, no phylogeny tree necessary

#     Args:
#         feature_table (FeatureTable[Frequency]): Feature table that will be used to calculate distance matrix
#         metric (String): The beta diversity metric to be computed

#     Returns:
#         DistanceMatrix: Distance matrix based on feature table
#     """
#     return beta(feature_table, metric).distance_matrix

        
def calculate_distance_matrices(feature_table, metrics, phylogeny=None):
    """Calculate distance matrices based on given metrics

    Args:
        feature_table (FeatureTable[Frequency]): Feature table that will be used to calculate distance matrix
        metrics (List): List of metrics for which the beta diversity will be computed
        phylogeny (_type_, optional): _description_. Defaults to None.

    Returns:
        Dict: {"Metric": DistanceMatrix}
    """
    output = {}
    for x in metrics:
        if (x == 'unweighted_unifrac') or (x == 'weighted_unifrac'):
            if phylogeny is None:
                print("Can't Calculate " + x +" distance matrix without phylogeny tree")
                continue
            else:
                distance_matrix = beta_phylogenetic(feature_table, phylogeny, x).distance_matrix
        else:
            distance_matrix = beta(feature_table, x).distance_matrix
        output[x] = distance_matrix
    return output

def calculate_pcoa(distance_matrix_dict, n_dimensions):
    """Calculate Principle Coordinates Analysis for multiple distance matrices

    Args:
        distance_matrix_dict (Dict): Dictionary containing distance matrices
        n_dimensions (Int): Dimensions to reduce the distance matrix to

    Returns:
        Dict: {"Metric": PcoA Results}
    """
    pcoa_results = {}
    for i in distance_matrix_dict.keys():
        pcoa_results[i] = pcoa(distance_matrix_dict[i], n_dimensions).pcoa
    return pcoa_results

def permanova_test(distance_matrix, metadata_col, metric):
    """Perform permanova test on given column

    Args:
        distance_matrix (DistanceMatrix): Distance Matrix
        metadata_col (_type_): Column that will undergo permanova test
        metric (String): The beta diversity metric to be computed.
    """
    permanova_result = beta_group_significance(distance_matrix, metadata_col, method='permanova')
    permanova_result.visualization.save('data/out/'+metric+'_permanova_test_'+metadata_col.name)
    
def permanova_test_all_diseases(u_unifrac_dis_matrix, w_unifrac_dis_matrix, metadata, disease_targets):
    """Perform permanova test on all disease columns using weighted/unweighted unifrac distance matrices

    Args:
        u_unifrac_dis_matrix (DistanceMatrix): Unweighted Unifrac Distance Matrix
        w_unifrac_dis_matrix (DistanceMatrix): Weighted Unifrac Distance Matrix
        metadata (METADATA): Disease metadata
        disease_targets (List): Disease column names that will undergo permanova test
    """    
    for disease in disease_targets:
        if disease == 'precvd_v2':
            continue
        metadata_disease_col = metadata.get_column(disease)
        permanova_test(u_unifrac_dis_matrix, metadata_disease_col,'u_unifrac')
        permanova_test(w_unifrac_dis_matrix, metadata_disease_col,'w_unifrac')

