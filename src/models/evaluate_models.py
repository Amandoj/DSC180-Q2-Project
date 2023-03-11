from sklearn.metrics import accuracy_score
import pandas as pd


def binary_relevance_accuracy_scores(model_results, disease_cols):
    """Calculate accuracy scores of all binary classifers within binary relevance model

    Args:
        model_results (): _description_
        disease_cols (List): List of disease column names 

    Returns:
        Dict: Accuracy scores for binary relevance model keyed by disease column name
    """
    disease_accuracy_scores = {}
    for i in disease_cols:
        ## Maybe can include auc in this
        score = accuracy_score(model_results[i].test_targets.view(pd.Series), model_results[i].predictions.view(pd.Series))
        disease_accuracy_scores[i] = score
        
    return disease_accuracy_scores