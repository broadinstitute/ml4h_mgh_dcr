import argparse
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from dementia_cohort import process_dementia_data
from control_matching import match_controls_to_cases
from model import logistic_regression, model_summary
from plots_binary_classifier import plot_roc_curve, plot_precision_recall_curve, plot_confusion_matrix

def main(args):
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load and process dementia data
    dementia_df = process_dementia_data(args.dementia_file, args.demographics_file)
    control_df_all = pd.read_csv(args.controls_file)

    # Match controls
    matched_df = match_controls_to_cases(
        control_df_all, dementia_df, args.age_cutoff_lower, args.age_cutoff_higher, 
        args.num_controls, args.age_tolerance
    )
    dementia_df_considered = dementia_df[
        (dementia_df['condition_start_age'] > args.age_cutoff_lower) &
        (dementia_df['condition_start_age'] < args.age_cutoff_higher)
    ].reset_index(drop=True)
    
    dementia_df_considered = dementia_df_considered.rename(columns={'condition_start_age': 'age'})
    
    dementia_df_considered['age_model'] = dementia_df_considered['age'] - args.prediction_range
    matched_df['age_model'] = matched_df['age'] - args.prediction_range

    # Create wide file for modeling
    wide_df = pd.concat([dementia_df_considered[args.columns_for_wide_file], matched_df[args.columns_for_wide_file]], ignore_index=True)
    wide_df = wide_df.sample(frac=1, random_state=42).reset_index(drop=True)
    if 'M' in set(wide_df['gender']):
        wide_df['gender'] = wide_df['gender'].apply(lambda x: 1 if x == 'M' else 0)

    # Prepare data for modeling
    X = wide_df.drop(columns=['diagnosis', 'person_id'])
    y = wide_df['diagnosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    X_train = X_train.reset_index(drop=True)
    X_test = X_test.reset_index(drop=True)
    y_train = y_train.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)

    
    # Standardize continuous variables
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(X_train[args.continuous_columns])
    scaled_df = pd.DataFrame(scaled_data, columns=X_train[args.continuous_columns].columns)
    derivation_set = pd.concat([X_train[args.categorical_columns], scaled_df], axis=1)
    test_scaled_data = scaler.transform(X_test[args.continuous_columns])
    test_scaled_df = pd.DataFrame(test_scaled_data, columns=X_test[args.continuous_columns].columns)
    test_set = pd.concat([X_test[args.categorical_columns], test_scaled_df], axis=1)

    # Train and evaluate model
    model, accuracy = logistic_regression(derivation_set, y_train, test_set, y_test)
    

    # Save accuracy to file
    accuracy_file = os.path.join(args.output_dir, "model_accuracy.txt")
    with open(accuracy_file, "w") as f:
        f.write(f"Final Model Accuracy: {accuracy}\n")

    # Plot and save performance metrics
    y_pred = model.predict(test_set)
    conf_matrix = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(conf_matrix, classes = ['No dementia', 'Dementia'], title='Confusion Matrix', cmap=plt.cm.Blues, save_path=os.path.join(args.output_dir, "confusion_matrix.png"))
    plot_roc_curve(model, test_set, np.array([[0, 1] if i == 1 else [1, 0] for i in y_test]), title='ROC Curve', labels=['No dementia','dementia'],save_path=os.path.join(args.output_dir, "roc_curve.png"))
    plot_precision_recall_curve(model, test_set, np.array([[0, 1] if i == 1 else [1, 0] for i in y_test]), title='Precision-Recall Curve', labels=['No dementia','dementia'], save_path=os.path.join(args.output_dir, "precision_recall_curve.png"))

    # Statistical summary
    results_df = model_summary(model, derivation_set, y_train)
    

    # Save results summary to file
    results_file = os.path.join(args.output_dir, "model_summary.csv")
    results_df.to_csv(results_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls_file", required=True, help="Path to the all controls file")
    parser.add_argument("--dementia_file", required=True, help="Path to the dementia file")
    parser.add_argument("--demographics_file", required=True, help="Path to the demographics file")
    parser.add_argument("--age_cutoff_lower", type=int, default=45, help="Lower age cutoff for dementia")
    parser.add_argument("--age_cutoff_higher", type=int, default=85, help="Higher age cutoff for dementia")
    parser.add_argument("--num_controls", type=int, default=25, help="Number of controls to match per case")
    parser.add_argument("--age_tolerance", type=int, default=1, help="Age tolerance in years for matching")
    parser.add_argument("--prediction_range", type=int, default=3, help="Prediction range for age model")
    parser.add_argument("--columns_for_wide_file", nargs='+', default=['age_model', 'age', 'gender', 'person_id', 'diagnosis'], help="Columns for wide file")
    parser.add_argument("--categorical_columns", nargs='+', default=['gender'], help="Categorical columns")
    parser.add_argument("--continuous_columns", nargs='+', default=['age_model'], help="Continuous columns")
    parser.add_argument("--output_dir", default="output", help="Directory to save figures, model accuracy and results")

    args = parser.parse_args()
    main(args)

