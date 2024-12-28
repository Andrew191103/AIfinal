import os
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data_path = "/Users/andrewsebastian/Downloads/pieennnn/New Evaluation/Detected Risks"

def calculate_model_metrics(df):
    metrics = {"BERT": [], "BART": [], "GPT": []}

    mapping = {"TP": 1, "FP": 0, "FN": 0, "TN": 0}
    
    for model in ["BERT", "BART", "GPT"]:
        if model not in df.columns:
            print(f"Warning: {model} column not found in the data.")
            continue

        y_true = df["Ground Truth"].map({"Yes": 1, "No": 0}).fillna(0).tolist()
        y_pred = df[model].map(mapping)

        y_pred = y_pred.fillna(0).tolist()

        if len(y_true) != len(y_pred):
            print(f"Error: Length mismatch in {model} predictions.")
            continue

        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)

        metrics[model].extend([accuracy, precision, recall, f1])

    return metrics

all_metrics = {"BERT": [], "BART": [], "GPT": []}

for file in os.listdir(data_path):
    if file.endswith(".csv"):
        file_path = os.path.join(data_path, file)
        print(f"Processing file: {file}")
        try:
            df = pd.read_csv(file_path)
            file_metrics = calculate_model_metrics(df)
            for model in all_metrics:
                if file_metrics.get(model):
                    all_metrics[model].append(file_metrics[model])
        except Exception as e:
            print(f"Error processing {file}: {e}")

average_metrics = {}
for model, metrics in all_metrics.items():
    if metrics: 
        metrics_df = pd.DataFrame(metrics, columns=["Accuracy", "Precision", "Recall", "F1-Score"])
        average_metrics[model] = metrics_df.mean().round(2)

print("\nAverage Metrics Across All Files:")
for model, scores in average_metrics.items():
    print(f"\n{model}:")
    for metric, value in scores.items():
        print(f"  {metric}: {value}")