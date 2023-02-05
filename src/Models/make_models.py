from qiime2.plugins.sample_classifier.pipelines import classify_samples

def sample_classifier_single_disease(feature_table, metadataCol):
    return classify_samples(feature_table, metadataCol, missing_samples='ignore')