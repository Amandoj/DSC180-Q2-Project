#!/usr/bin/env python

## NECESSARY IMPORTS
import sys
import json
import os
import shutil

from src.data import make_dataset
from src.features import build_features,metrics_analysis
from src.models import make_models, evaluate_models
from src.visualizations import make_visualizations, dimensionality_analysis


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
        
        with open("config/test-feature-params.json") as fh:
            test_feature_params = json.load(fh)
        
        # Organizing metadata and returning two metadata tables
        # organized_metadata: 0/1 binary; organized_metadata_tf:T/F binary 
        organized_metadata, organized_metadata_tf  = build_features.organize_metadata(metadata,biom_table.ids(), **test_feature_params)
        
        # Create Disease Count Graph
        make_visualizations.disease_counts_graph(organized_metadata,test_feature_params['disease_cols'])
        
        # Convert metadata dataframe to qiime Metadata object
        qiime_metadata_tf = make_dataset.read_qiime_metadata("data/temp/final_metadata_tf.tsv")
        filtered_table = make_dataset.filter_feature_table(feature_table, min_samples=1, metadata=qiime_metadata_tf)
        
        # Calculate distance matrix
        braycurtis_matrix = metrics_analysis.calculate_distance_matrices(filtered_table,['braycurtis'])
        
        # Obtain pcoa results based on distance matrices
        pcoa_results = metrics_analysis.calculate_pcoa(braycurtis_matrix, n_dimensions=3)
        
        # Plot pcoa results
        dimensionality_analysis.plot_pcoa(pcoa_results, qiime_metadata_tf)
        
        #Permanova Test
        metrics_analysis.permanova_test(braycurtis_matrix['braycurtis'], qiime_metadata_tf.get_column('abdominal_obesity_ncep_v2') ,'braycurtis')
        
        ## Obtaining model params
        with open("config/model-params.json") as fh:
            model_params = json.load(fh)
        
        # Creating machine learning models
        binary_relevance_model = make_models.binary_relevance_model(filtered_table, qiime_metadata_tf, qiime_metadata_tf, model_params['disease_targets'])
        # Model Performance 
        disease_accuracy_scores = evaluate_models.binary_relevance_accuracy_scores(binary_relevance_model, model_params['disease_targets'])
        make_visualizations.binary_relevance_accuracy_scores_graph(disease_accuracy_scores)
        print('End')
        return binary_relevance_model

    
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
        
        # Create disease count graph
        make_visualizations.disease_counts_graph(organized_metadata, feature_params['disease_cols'])
        
        # Converting metadata dataframe to Qiime metadata object
        qiime_metadata_tf = make_dataset.read_qiime_metadata("data/temp/final_metadata_tf.tsv") #Metadata with True and False booleans
        qiime_metadata = make_dataset.read_qiime_metadata("data/temp/final_metadata.tsv") #Metadata with 1 and 0s floats
        # Balance Precvd classes
        qiime_metadata_precvd = build_features.balance_precvd(organized_metadata_tf)

        
        #DIMENSIONALITY ANALYSIS
        print('Dimensionality Analysis')
        
        #Filtering metadata and feature table to only get samples with 1 target disease type, to remove disease ambiguity and perform supervised UMAP
        metadata_df = qiime_metadata.to_dataframe()
        feature_df_target_disease, target_disease_map, target_disease_dict = dimensionality_analysis.process_table_umap(feature_table, metadata_df, feature_params['disease_cols'])
        
        #Perform the supervised UMAP with params from json file
        with open("config/umap-params.json") as fh:
            umap_params = json.load(fh)

        #Create the UMAP embeddings matrix and plot the UMAP results
        umap_embedding = dimensionality_analysis.umap_plot_supervised(feature_df_target_disease, target_disease_map, target_disease_dict, **umap_params)
        
        
        with open("config/dim-analysis-params.json") as fh:
            dim_analysis_params = json.load(fh)
        
        # Minimum number of samples a given feature must be present in
        min_samples = dim_analysis_params['filter_min_samples'] 
        
        # Filtering Feature Tables 
        filtered_table = make_dataset.filter_feature_table(feature_table, min_samples, qiime_metadata_tf)
        filtered_table_precvd = make_dataset.filter_feature_table(feature_table, min_samples, qiime_metadata_precvd)
        
            
        rarefied_table = make_dataset.rarefy_feature_table(filtered_table, dim_analysis_params['rarefy_sampling_depth'])
        # Obtain distance matrices
        distance_matrices = metrics_analysis.calculate_distance_matrices(rarefied_table,metrics = dim_analysis_params['metrics'], phylogeny = tree_artifact)
        
        # Obtain pcoa results based on distance matrices
        pcoa_results = metrics_analysis.calculate_pcoa(distance_matrices, dim_analysis_params['pcoa_n_dimensions'])
        
        # Plot pcoa results
        dimensionality_analysis.plot_pcoa(pcoa_results, qiime_metadata_tf)
        
        print('Permanova Test')
        
        # Permanova Tests - all diseases w/o precvd
        metrics_analysis.permanova_test_all_diseases(distance_matrices['unweighted_unifrac'], distance_matrices['weighted_unifrac'], qiime_metadata_tf, feature_params['disease_cols'])

        # Permanova Test - balanced precvd
        distance_matrices_precvd = metrics_analysis.calculate_distance_matrices(filtered_table_precvd, metrics = dim_analysis_params['precvd_metrics'], phylogeny = tree_artifact)       

        metrics_analysis.permanova_test(distance_matrices_precvd["unweighted_unifrac"], qiime_metadata_precvd.get_column('precvd_v2'),'u_unifrac')
        metrics_analysis.permanova_test(distance_matrices_precvd["weighted_unifrac"], qiime_metadata_precvd.get_column('precvd_v2'),'w_unifrac')


        ## Obtaining model params
        with open("config/model-params.json") as fh:
            model_params = json.load(fh)
            
        print('Model Training Begins')
        # Creating machine learning model
        binary_relevance_model = make_models.binary_relevance_model(feature_table, qiime_metadata_tf, qiime_metadata_precvd, **model_params)
        
        #Model Performance 
        disease_accuracy_scores = evaluate_models.binary_relevance_accuracy_scores(binary_relevance_model, **model_params)
        make_visualizations.binary_relevance_accuracy_scores_graph(disease_accuracy_scores)
        print('END')

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
    