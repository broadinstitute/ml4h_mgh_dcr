import statsmodels.api as sm
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def logistic_regression(X_train, y_train, X_test, y_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return model, accuracy

def model_summary(model, X, y):
    model_test = sm.Logit(y, sm.add_constant(X)).fit()
    results_df = pd.DataFrame({
        'Predictor Variable': X.columns,
        'Beta Coefficient': model_test.params[1:].round(3),
        'p-value': model_test.pvalues[1:].round(3),
        'Odds Ratio': np.exp(model_test.params[1:]).round(3),
        '2.5% CI': np.exp(model_test.conf_int()).iloc[1:, 0].round(3),
        '97.5% CI': np.exp(model_test.conf_int()).iloc[1:, 1].round(3)
    })
    return results_df
