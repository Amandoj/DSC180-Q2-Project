from qiime2.plugins.sample_classifier.pipelines import classify_samples

def sample_classifier_single_disease(feature_table, metadataCol):
    return classify_samples(feature_table, metadataCol, missing_samples='ignore')

def sample_classifier_diseases(feature_table, metadata, disease_targets):
    disease_cols = [metadata.get_column(disease) for disease in disease_targets]
    results = []
    for metadata_disease_col in disease_cols:
        qiime_model = sample_classifier_single_disease(feature_table, metadata_disease_col)
        results.append(qiime_model)
    return results
    