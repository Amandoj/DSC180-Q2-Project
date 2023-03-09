from qiime2.plugins.sample_classifier.pipelines import classify_samples

def sample_classifier_single_disease(feature_table, metadataCol):
    """Create machine learning model of given metadataCol/disease_type

    Args:
        feature_table (FeatureTable[Frequency]): Feature table containing all features that will be used to create model
        metadataCol (MetadataColumn[Categorical]): Metadata column that will be used as prediction target

    Returns:
        Results
    """
    results = classify_samples(feature_table, metadataCol, estimator='GradientBoostingClassifier', 
                               test_size = 0.3, cv = 10, random_state = 100, missing_samples='ignore')
    # results
    model_summary = results.model_summary
    accuracy_results = results.accuracy_results
    
    # Saving Accuracy Results
    accuracy_results.save('data/out/accuracy_results_'+metadataCol.name)
    # Saving model summary information
    model_summary.save('data/out/model_summary_'+metadataCol.name)
    return results

def binary_relevance_model(feature_table, metadata, disease_targets, precvd_col=None):
    """Create machine learning models for all disease targets

    Args:
        feature_table (FeatureTable[Frequency]): Feature table containing all features that will be used to create model
        metadata (Metadata): Metadata containing data about disease targets
        disease_targets (List): List of disease targets

    Returns:
        Dict: Dictionary of model results by disease type: {'disease_col': Qiime results}
    """
    # Create list of metadata columns
    disease_cols = [metadata.get_column(disease) for disease in disease_targets]
    results = {}
    # Iterate through every disease
    for metadata_disease_col in disease_cols:
        if metadata_disease_col.name == 'precvd_v2':
            qiime_model = sample_classifier_single_disease(feature_table, precvd_col)
        # Create model for each disease
        else:
            qiime_model = sample_classifier_single_disease(feature_table, metadata_disease_col)
        results[metadata_disease_col.name] = qiime_model
    return results
    