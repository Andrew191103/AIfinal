import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data_path = "/Users/andrewsebastian/Downloads/pieennnn/New Evaluation/Detected Risks"

def calculate_model_metrics(df):
    metrics = {"BERT": {}, "BART": {}, "GPT": {}}

    mapping = {"TP": 1, "FP": 0, "FN": 0, "TN": 0}
    
    for model in ["BERT", "BART", "GPT"]:
        if model not in df.columns:
            print(f"Warning: {model} column not found in the data.")
            continue

        y_true = df["Ground Truth"].map({"Yes": 1, "No": 0}).fillna(0).tolist()
        y_pred = df[model].map(mapping).fillna(0).tolist()

        if len(y_true) != len(y_pred):
            print(f"Error: Length mismatch in {model} predictions.")
            continue

        metrics[model] = {
            "Accuracy": round(accuracy_score(y_true, y_pred), 2),
            "Precision": round(precision_score(y_true, y_pred, zero_division=0), 2),
            "Recall": round(recall_score(y_true, y_pred, zero_division=0), 2),
            "F1-Score": round(f1_score(y_true, y_pred, zero_division=0), 2),
        }

    return metrics

all_metrics = {"Policy": [], "BERT_Accuracy": [], "BART_Accuracy": [], "GPT_Accuracy": [],
               "BERT_Precision": [], "BART_Precision": [], "GPT_Precision": [],
               "BERT_Recall": [], "BART_Recall": [], "GPT_Recall": [],
               "BERT_F1": [], "BART_F1": [], "GPT_F1": []}

for file in os.listdir(data_path):
    if file.endswith(".csv"): 
        file_path = os.path.join(data_path, file)
        print(f"\nProcessing file: {file}")
        try:
            df = pd.read_csv(file_path)
            file_metrics = calculate_model_metrics(df)
            
            
            all_metrics["Policy"].append(file)
            for model in ["BERT", "BART", "GPT"]:
                all_metrics[f"{model}_Accuracy"].append(file_metrics[model]["Accuracy"])
                all_metrics[f"{model}_Precision"].append(file_metrics[model]["Precision"])
                all_metrics[f"{model}_Recall"].append(file_metrics[model]["Recall"])
                all_metrics[f"{model}_F1"].append(file_metrics[model]["F1-Score"])
        except Exception as e:
            print(f"Error processing {file}: {e}")

df_metrics = pd.DataFrame(all_metrics)

heatmap_data = df_metrics.melt(id_vars='Policy', var_name='Metric', value_name='Score')
heatmap_pivot = heatmap_data.pivot('Policy', 'Metric', 'Score')

plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_pivot, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.5)
plt.title("Combined Model Performance Heatmap Across Policies")
plt.xlabel("Metrics")
plt.ylabel("Privacy Policies")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
