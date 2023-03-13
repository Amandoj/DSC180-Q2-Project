from qiime2.plugins.diversity.pipelines import core_metrics, core_metrics_phylogenetic,beta_phylogenetic,beta
from qiime2.plugins.diversity.visualizers import beta_group_significance


def calculate_unifrac_distance_matrices(feature_table, phylogeny):
    distance_matrices = ['unweighted_unifrac','weighted_unifrac']
    u_unifrac_dis_matrix = beta_phylogenetic(feature_table, phylogeny, 'unweighted_unifrac').distance_matrix
    w_unifrac_dis_matrix = beta_phylogenetic(feature_table, phylogeny, 'weighted_unifrac').distance_matrix
    return u_unifrac_dis_matrix, w_unifrac_dis_matrix

def calculate_distance_matrix(feature_table, metric):
    return beta(feature_table, metric).distance_matrix
        

def permanova_test(distance_matrix, metadata_col, metric):
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

