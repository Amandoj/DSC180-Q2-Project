from qiime2.plugins.sample_classifier.pipelines import classify_samples

def sample_classifier_single_disease(feature_table, metadataCol):
    """Create machine learning model of given metadataCol/disease_type

    Args:
        feature_table (FeatureTable[Frequency]): Feature table containing all features that will be used to create model
        metadataCol (MetadataColumn[Categorical]): Metadata column that will be used as prediction target

    Returns:
        SampleEstimator[Classifier]: Trained sample estimator
    """
    results = classify_samples(feature_table, metadataCol, missing_samples='ignore', estimator='GradientBoostingClassifier', 
                               test_size = 0.3, cv = 10, random_state = 100)
    # results
    sample_estimator = results.sample_estimator
    feature_importance = results.feature_importance
    predictions = results.predictions
    model_summary = results.model_summary
    accuracy_results = results.accuracy_results
    probabilities = results.probabilities
    heatmap = results.heatmap
    training_targets = results.training_targets
    test_targets = results.test_targets
    
    accuracy_results.save('data/out/accuracy_results_'+metadataCol.name)
    model_summary.save('data/out/model_summary_'+metadataCol.name)
    return results

def binary_relevance_model(feature_table, metadata, disease_targets):
    """Create machine learning models for all disease targets

    Args:
        feature_table (FeatureTable[Frequency]): Feature table containing all features that will be used to create model
        metadata (Metadata): Metadata containing data about disease targets
        disease_targets (List): List of disease targets

    Returns:
        List: List of all machine learning models
    """
    disease_cols = [metadata.get_column(disease) for disease in disease_targets]
    results = {}
    for metadata_disease_col in disease_cols:
        qiime_model = sample_classifier_single_disease(feature_table, metadata_disease_col)
        results[metadata_disease_col.name] = qiime_model
    return results
    