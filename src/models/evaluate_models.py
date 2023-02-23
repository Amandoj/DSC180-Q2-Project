from sklearn.metrics import accuracy_score
import pandas as pd


def binary_relevance_accuracy_scores(model_results, disease_cols):
    disease_accuracy_scores = {}
    for i in disease_cols:
        score = accuracy_score(model_results[i].test_targets.view(pd.Series), model_results[i].predictions.view(pd.Series))
        disease_accuracy_scores[i] = score
        
    return disease_accuracy_scores