#!/usr/bin/env python


## NECESSARY IMPORTS
import sys
import json
import os
import shutil

from src.data import make_dataset
from src.features import build_features,metrics_analysis
from src.models import make_models, evaluate_models
from src.visualizations import make_visualizations


def main(targets):
    if "test" in targets:
        if not os.path.exists("data/temp"):
            os.makedirs("data/temp")
        if not os.path.exists("data/out"):
            os.makedirs("data/out")
        
        test_path_metadata="test/test_metadata.tsv"
        test_path_feature_table = "test/test_feature_table.qza"

        metadata = make_dataset.read_metadata(test_path_metadata)
        feature_table = make_dataset.read_feature_table(test_path_feature_table)
        biom_table = make_dataset.feature_table_biom_view(feature_table)
        
        with open("config/feature-params.json") as fh:
            feature_params = json.load(fh)
        
        # Organizing metadata and returning two metadata tables
        # organized_metadata: 0/1 binary; organized_metadata_tf:T/F binary 
        organized_metadata, organized_metadata_tf  = build_features.organize_metadata(metadata,biom_table.ids(), **feature_params)
        
        # Create Disease Count Graph
        make_visualizations.disease_counts_graph(organized_metadata,feature_params['disease_cols'])
        
        # need to convert metadata dataframe to qiime Metadata object
        qiime_metadata_tf = make_dataset.read_qiime_metadata("data/temp/final_metadata_tf.tsv")
        filtered_table = make_dataset.filter_feature_table(feature_table, 1, qiime_metadata_tf)
        
        braycurtis_matrix = metrics_analysis.calculate_distance_matrix(filtered_table,'braycurtis')
        metrics_analysis.permanova_test(braycurtis_matrix,qiime_metadata_tf.get_column('abdominal_obesity_ncep_v2') ,'braycurtis')
        ## Obtaining model params
        with open("config/model-params.json") as fh:
            model_params = json.load(fh)
        
        # Creating machine learning models
        disease_models = make_models.binary_relevance_model(filtered_table, qiime_metadata_tf,feature_params['disease_cols'])
        # Model Performance 
        disease_accuracy_scores = evaluate_models.binary_relevance_accuracy_scores(binary_relevance_model, model_params['disease_targets'])
        make_visualizations.binary_relevance_accuracy_scores_graph(disease_accuracy_scores)
        print('done')
        return disease_models

    
    if "all" in targets:
        if not os.path.exists("data/temp"):
            os.makedirs("data/temp")
        if not os.path.exists("data/out"):
            os.makedirs("data/out")
            
        with open("config/data-params.json") as fh:
            file_paths = json.load(fh)
            
        # Reading feature table as Qiime Artifact and biom table
        feature_table = make_dataset.read_feature_table(file_paths["feature_table_path"])
        biom_table = make_dataset.feature_table_biom_view(feature_table)
        # Reading metadata
        metadata = make_dataset.read_metadata(file_paths["metadata_path"])
        
        # Reading Phylogenetic Tree
        tree_artifact = make_dataset.read_tree_table(file_paths['tree_path']) 

        ## Obtaining feature parameters
        with open("config/feature-params.json") as fh:
            feature_params = json.load(fh)
            
        # Organizing metadata and returning two metadata tables
        # organized_metadata: 0/1 binary; organized_metadata_tf:T/F binary 
        organized_metadata, organized_metadata_tf = build_features.organize_metadata(metadata,biom_table.ids(),**feature_params)
        
        # Balance Precvd classes
        qiime_metadata_precvd = build_features.balance_precvd(organized_metadata_tf)
        
        # Converting metadata dataframe to Qiime metadata object
        qiime_metadata_tf = make_dataset.read_qiime_metadata("data/temp/final_metadata_tf.tsv")
        
        # Filtering Feature Tables 
        filtered_table = make_dataset.filter_feature_table(feature_table, 4, qiime_metadata_tf)
        filtered_table_precvd = make_dataset.filter_feature_table(feature_table, 4, qiime_metadata_precvd)

        print('feature analysis')
        #Feature Analysis
        rarefied_table = make_dataset.rarefy_feature_table(filtered_table, 7930)
        u_unifrac_distance_matrix, w_unifrac_distance_matrix = metrics_analysis.calculate_unifrac_distance_matrices(rarefied_table, tree_artifact)
        # Permanova Test
        metrics_analysis.permanova_test_all_diseases(u_unifrac_distance_matrix, w_unifrac_distance_matrix, qiime_metadata_tf, feature_params['disease_cols'])
        
        #Feature Analysis precvd
        u_unifrac_distance_matrix_precvd,w_unifrac_distance_matrix_precvd = metrics_analysis.calculate_unifrac_distance_matrices(filtered_table_precvd, tree_artifact)
        metrics_analysis.permanova_test(u_unifrac_distance_matrix_precvd, w_unifrac_distance_matrix_precvd, qiime_metadata_precvd.get_column('precvd_v2'))

        ## Obtaining model params
        with open("config/model-params.json") as fh:
            model_params = json.load(fh)
        print('model begin')
        # Creating machine learning models
        binary_relevance_model = make_models.binary_relevance_model(feature_table, qiime_metadata_tf, qiime_metadata_precvd, model_params['disease_targets'])
        
        #Model Performance 
        disease_accuracy_scores = evaluate_models.binary_relevance_accuracy_scores(binary_relevance_model, model_params['disease_targets'])
        make_visualizations.binary_relevance_accuracy_scores_graph(disease_accuracy_scores)
        print('end')

        return binary_relevance_model
        
    if 'clean' in targets:
        try:
            shutil.rmtree("data/temp")
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
        try:
            shutil.rmtree("data/out")
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == "__main__":
    # python run.py test
    targets = sys.argv[1:]
    main(targets)
    