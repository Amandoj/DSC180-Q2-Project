from qiime2.plugins.sample_classifier.pipelines import classify_samples

def sample_classifier_single_disease(feature_table, metadataCol):
    """Create machine learning model of given metadataCol/disease_type

    Args:
        feature_table (FeatureTable[Frequency]): Feature table containing all features that will be used to create model
        metadataCol (MetadataColumn[Categorical]): Metadata column that will be used as prediction target

    Returns:
        sample_estimator : SampleEstimator[Classifier]
            Trained sample estimator.
        feature_importance : FeatureData[Importance]
            Importance of each input feature to model accuracy.
        predictions : SampleData[ClassifierPredictions]
            Predicted target values for each input sample.
        model_summary : Visualization
            Summarized parameter and (if enabled) feature selection information for
            the trained estimator.
        accuracy_results : Visualization
            Accuracy results visualization.
        probabilities : SampleData[Probabilities]
            Predicted class probabilities for each input sample.
        heatmap : Visualization
            A heatmap of the top 50 most important features from the table.
        training_targets : SampleData[TrueTargets]
            Series containing true target values of train samples
        test_targets : SampleData[TrueTargets]
            Series containing true target values of test samples
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

def binary_relevance_model(feature_table, metadata, precvd_metadata, disease_targets):
    """Create machine learning models for all disease targets

    Args:
        feature_table (FeatureTable[Frequency]): Feature table containing all features that will be used to create model
        metadata (Metadata): Metadata containing data about disease targets
        disease_targets (List): List of disease targets

    Returns:
        Dict: Dictionary of model results by disease type: {'disease_col': Qiime results}
    """
    results = {}
    # Iterate through every disease
    for disease_name in disease_targets:
        if disease_name == 'precvd_v2':
            disease_col = precvd_metadata.get_column('precvd_v2')
        else:
            disease_col = metadata.get_column(disease_name) 
        qiime_model = sample_classifier_single_disease(feature_table, disease_col)
        results[disease_name] = qiime_model
    return results
    