import matplotlib.pyplot as plt
import numpy as np

# Data for Detected Risks
models = ['BERT', 'BART', 'GPT']
tp = [43, 53, 62]
fp = [7, 14, 22]
fn = [19, 9, 0]
tn = [26, 19, 12]

# Plot Detected Risks
fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(len(models))
bar_width = 0.2

ax.bar(x - 1.5 * bar_width, tp, width=bar_width, label='True Positives (TP)')
ax.bar(x - 0.5 * bar_width, fp, width=bar_width, label='False Positives (FP)')
ax.bar(x + 0.5 * bar_width, fn, width=bar_width, label='False Negatives (FN)')
ax.bar(x + 1.5 * bar_width, tn, width=bar_width, label='True Negatives (TN)')

ax.set_xlabel('Models')
ax.set_ylabel('Counts')
ax.set_title('Detected Risks: Model Performance')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Move legend outside

plt.tight_layout()
plt.show()

# Data for Permissions/Allowances
tp_perm = [23, 24, 26]
fp_perm = [0, 0, 0]
fn_perm = [29, 28, 26]
tn_perm = [0, 0, 0]

# Plot Permissions/Allowances
fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(len(models))

ax.bar(x - 1.5 * bar_width, tp_perm, width=bar_width, label='True Positives (TP)')
ax.bar(x - 0.5 * bar_width, fp_perm, width=bar_width, label='False Positives (FP)')
ax.bar(x + 0.5 * bar_width, fn_perm, width=bar_width, label='False Negatives (FN)')
ax.bar(x + 1.5 * bar_width, tn_perm, width=bar_width, label='True Negatives (TN)')

ax.set_xlabel('Models')
ax.set_ylabel('Counts')
ax.set_title('Permissions/Allowances: Model Performance')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Move legend outside

plt.tight_layout()
plt.show()
