from qiime2.plugins.sample_classifier.pipelines import classify_samples

def sample_classifier_single_disease(feature_table, metadataCol):
    results = classify_samples(feature_table, metadataCol, missing_samples='ignore')
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
    heatmap.save('data/out/heatmap_'+metadataCol.name)
    
    return results

def sample_classifier_diseases(feature_table, metadata, disease_targets):
    disease_cols = [metadata.get_column(disease) for disease in disease_targets]
    results = []
    for metadata_disease_col in disease_cols:
        qiime_model = sample_classifier_single_disease(feature_table, metadata_disease_col)
        results.append(qiime_model)
    return results
    