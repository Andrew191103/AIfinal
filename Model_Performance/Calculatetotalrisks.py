import pandas as pd
from collections import defaultdict

data = """
Aspect,Ground Truth,BERT,BART,GPT
Personal data,Yes,TP,TP,TP
Location,Yes,TP,TP,TP
Third-party,Yes,TP,TP,TP
Cookies,Yes,TP,TP,TP
Payment information,Yes,TP,TP,TP
Marketing purposes,No,FP,FP,FP
Device information,Yes,TP,TP,TP
Health data,Yes,TP,TP,TP
Advertising,Yes,TP,TP,TP
Profiling,No,TN,FP,FP
Financial information,No,TN,TN,FP
Loss,Yes,FN,FN,TP
Aspect,Ground Truth,BERT,BART,GPT
Personal information,Yes,TP,TP,TP
Personal data,Yes,TP,TP,TP
IP address,Yes,FN,TP,TP
Cookies,Yes,FN,TP,TP
Loss,No,TN,TN,FP
Aspect,Ground Truth,BERT,BART,GPT
Personal information,Yes,TP,TP,TP
Personal data,Yes,TP,TP,TP
Location,No,TN,FP,FP
IP address,Yes,FN,FN,TP
Geolocation,No,TN,FP,FP
Third-party,Yes,TP,TP,TP
Advertising,No,FP,FP,FP
Cookies,Yes,TP,TP,TP
Analytics,Yes,TP,TP,TP
Payment information,Yes,TP,FN,TP
Third-party services,No,TN,TN,FP
Data portability,No,TN,TN,FP
Aspect,Ground Truth,BERT,BART,GPT
Personal data,Yes,TP,TP,TP
Ip address,Yes,TP,TP,TP
Third-party,Yes,TP,TP,TP
Cookies,Yes,TP,TP,TP
Analytics,Yes,TP,TP,TP
Data retention,Yes,TP,FN,TP
Location,Yes,FN,TP,TP
Advertising,Yes,FN,TP,TP
Device information,Yes,FN,TP,TP
User activity,No,TN,TN,FP
Payment information,No,TN,TN,TN
Unauthorized access,No,TN,TN,FP
Loss,No,FP,TN,TN
Third-party services,No,TN,TN,TN
Aspect,Ground Truth,BERT,BART,GPT
Personal information,Yes,FN,TP,TP
Personal data,Yes,FN,TP,TP
Location,No,TN,TN,TN
IP address,Yes,TP,TP,TP
Third-party,Yes,TP,TP,TP
Advertising,No,TN,FP,FP
Cookies,Yes,TP,TP,TP
Marketing purposes,Yes,TP,FN,TP
Aspect,Ground Truth,BERT,BART,GPT
Personal information,Yes,FN,FN,TP
Location,No,TN,FP,FP
IP address,Yes,FN,TP,TP
Camera,Yes,TP,TP,TP
Third-party,Yes,TP,TP,TP
Cookies,Yes,FN,FN,TP
Analytics,Yes,TP,TP,TP
Payment information,Yes,FN,TP,TP
Device information,Yes,FN,FN,TP
Third-party services,No,TN,FP,FP
Face recognition,Yes,TP,TP,TP
Aspect,Ground Truth,BERT,BART,GPT
Personal information,Yes,TP,TP,TP
Location,No,TN,FP,TN
IP address,Yes,FN,TP,TP
Cookies,Yes,TP,TP,TP
Analytics,No,TN,FP,FP
Data retention,No,TN,TN,FP
Data processing,No,TN,TN,TN
Aspect,Ground Truth,BERT,BART,GPT
Personal information,Yes,TP,TP,TP
Personal data,No,No,No,FP
Location,No,TN,FP,TN
IP address,Yes,FN,TP,TP
Third-party,Yes,TP,TP,TP
Advertising,No,FP,FP,FP
Cookies,Yes,TP,TP,TP
Analytics,Yes,TP,TP,TP
Biometric data,No,TN,TN,TN
Payment information,Yes,TP,TP,TP
Data breach,No,FP,TN,TN
Unauthorized access,Yes,FN,FN,TP
Marketing purposes,No,TN,TN,FP
Data retention,No,TN,TN,TN
Device information,No,TN,TN,FP
Loss,No,TN,TN,FP
Data portability,No,FP,TN,FP
Cross-border data transfer,No,TN,FP,TN
Aspect,Ground Truth,BERT,BART,GPT
Personal information,Yes,TP,TP,TP
Location,Yes,TP,TP,TP
IP address,Yes,TP,TP,TP
Advertising,Yes,TP,TP,TP
Cookies,Yes,TP,TP,TP
Analytics,Yes,TP,TP,TP
Third-party,Yes,FN,TP,TP
Device information,Yes,FN,TP,TP
Unauthorized access,No,FP,FP,TN
"""

lines = data.strip().split("\n")
rows = [line.split(",") for line in lines]
df = pd.DataFrame(rows[1:], columns=rows[0])

counts = defaultdict(lambda: defaultdict(int))

for index, row in df.iterrows():
    for model in ['BERT', 'BART', 'GPT']:
        counts[model][row[model]] += 1

results = {}
for model in ['BERT', 'BART', 'GPT']:
    results[model] = {
        "TP": counts[model].get("TP", 0),
        "FP": counts[model].get("FP", 0),
        "FN": counts[model].get("FN", 0),
        "TN": counts[model].get("TN", 0),
    }

results
