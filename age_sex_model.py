import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from dementia_cohort import process_dementia_data, has_dementia_phenotype
from control_matching import match_controls, match_controls_to_cases
from model import logistic_regression, model_summary
from plots_binary_classifier import plot_roc_curve, plot_precision_recall_curve, plot_confusion_matrix

path_to_all_controls_file = 'path/to/all_controls.csv'
path_to_dementia_file = 'path/to/dementia_cases.csv'
path_to_demographics_file = 'path/to/demographics.csv'

dementia_age_cutoff_lower = 45
dementia_age_cutoff_higher = 85
num_controls = 25
age_tolerance = 1

prediction_range = 3

columns_for_wide_file = ['age_model','age','gender','person_id','diagnosis']
categorical_columns = ['gender']
continuous_columns = ['age_model']

# Load data
dementia_df = process_dementia_data(path_to_dementia_file, path_to_demographics_file)
control_df_all = pd.read_csv(path_to_all_controls_file)

control_df = match_controls_to_cases(control_df_all, dementia_df, 
                            dementia_age_cutoff_lower, dementia_age_cutoff_higher, 
                            num_controls, age_tolerance)

dementia_df_considered = dementia_df[
        (dementia_df['condition_start_age'] > dementia_age_cutoff_lower) &
        (dementia_df['condition_start_age'] < dementia_age_cutoff_higher)
    ].reset_index(drop=True)
dementia_df_considered = dementia_df_considered.rename(columns = {'condition_start_age':'age'})

dementia_df_considered['age_model'] = dementia_df_considered['age'] - prediction_range
matched_df['age_model'] = matched_df['age'] - prediction_range

#wide_file
wide_df = pd.concat([dementia_df_considered[columns_for_wide_file],\
                 matched_df[columns_for_wide_file]],ignore_index=True)
wide_df = wide_df.sample(frac=1, random_state=42).reset_index(drop=True)

if 'M' in set(wide_df['gender']):
    wide_df['gender'] = wide_df['gender'].apply(lambda x: 1 if x=='M' else 0)

X = wide_df.drop(columns=['diagnosis','person_id'])
y = wide_df['diagnosis']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = X_train.reset_index(drop=True)
X_test = X_test.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

#standardization
scaler = StandardScaler()
scaled_data = scaler.fit_transform(X_train[continuous_columns])
scaled_df = pd.DataFrame(scaled_data, columns=X_train[continuous_columns].columns)
derivation_set = pd.concat([X_train[categorical_columns], scaled_df], axis=1)

test_scaled_data = scaler.transform(X_test[continuous_columns])
test_scaled_df = pd.DataFrame(test_scaled_data, columns=X_test[continuous_columns].columns)
test_set = pd.concat([X_test[categorical_columns], test_scaled_df], axis=1)


# Model training and evaluation
model, accuracy = logistic_regression(derivation_set, y_train, test_set, y_test)
print("Final Model Accuracy:", accuracy)

# Plot performance metrics
y_pred = model.predict(test_set)
conf_matrix = confusion_matrix(y_test, y_pred)
plot_confusion_matrix(conf_matrix, ['No dementia', 'Dementia'], title='Confusion Matrix')
plot_roc_curve(model, test_set, np.array([[0,1] if i==1 else [1,0] for i in y_test]), title='ROC Curve')
plot_precision_recall_curve(model, test_set, np.array([[0,1] if i==1 else [1,0] for i in y_test]), title='Precision-Recall Curve')

# Statistical summary
results_df = model_summary(model, derivation_set, y_train)
print(results_df)

