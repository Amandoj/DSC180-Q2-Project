#!/usr/bin/env python


## NECESSARY IMPORTS
import sys
import json
import os
import shutil

from src.data import make_dataset
from src.features import build_features
from src.models import make_models
# from src.visualization import visualize


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
        
        with open("config/feature-params.json") as fh:
            feature_params = json.load(fh)
        
        organized_metadata = build_features.organize_metadata(metadata, **feature_params)
        
        # need to convert metadata df to qiime Metadata object
        qiime_metadata_tf = make_dataset.read_qiime_metadata("data/temp/final_metadata_tf.tsv")
        
        
        ## Obtaining model params
        with open("config/model-params.json") as fh:
            model_params = json.load(fh)
            
        disease_model = make_models.sample_classifier_diseases(feature_table, qiime_metadata_tf, feature_params['disease_cols'])
        print('done')
        

    
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
        
        ## Obtaining file paths
        with open("config/feature-params.json") as fh:
            feature_params = json.load(fh)
        # Organizing metadata and returning two metadata tables
        organized_metadata, organized_metadata_tf = build_features.organize_metadata(metadata, **feature_params)
        
        qiime_metadata_tf = make_dataset.read_qiime_metadata("data/temp/final_metadata_tf.tsv")
        
        ## Obtaining model params
        with open("config/model-params.json") as fh:
            model_params = json.load(fh)
        
        models = make_models.sample_classifier_single_disease(feature_table, qiime_metadata_tf.get_column('ckd_v2'))
        
        return models
        
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
    