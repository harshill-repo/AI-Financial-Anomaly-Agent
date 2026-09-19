import pandas as pd
import numpy as np
import json
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.seasonal import seasonal_decompose

df = pd.read_csv('output/processed_data.csv', parse_dates=['Date'])

total_revenue = float(df['Revenue'].sum())
avg_revenue = float(df['Revenue'].mean())

with open('output/kpi_summary.json', 'w') as f:
    json.dump({'total_revenue': total_revenue, 'avg_revenue': avg_revenue}, f)

df['z_score'] = (df['Revenue'] - df['Revenue'].mean()) / df['Revenue'].std()
df['anomaly_zscore'] = abs(df['z_score']) > 3

q1 = df['Revenue'].quantile(0.25)
q3 = df['Revenue'].quantile(0.75)
iqr = q3 - q1
df['anomaly_iqr'] = (df['Revenue'] < (q1 - 1.5*iqr)) | (df['Revenue'] > (q3 + 1.5*iqr))

span = 30
ewma = df['Revenue'].ewm(span=span, adjust=False).mean()
ewma_std = df['Revenue'].ewm(span=span, adjust=False).std()
df['anomaly_ewma'] = abs(df['Revenue'] - ewma) > 3 * ewma_std

try:
    result = seasonal_decompose(df['Revenue'], model='additive', period=365)
    resid = result.resid.fillna(0)
    df['anomaly_seasonal'] = abs(resid) > 3 * resid.std()
except Exception as e:
    df['anomaly_seasonal'] = False  

clf = IsolationForest(contamination=0.01, random_state=42)
df['iso_label'] = clf.fit_predict(df[['Revenue']])
df['anomaly_iforest'] = (df['iso_label'] == -1)

df['anomaly_combined'] = df[['anomaly_zscore','anomaly_iqr','anomaly_ewma','anomaly_iforest','anomaly_seasonal']].any(axis=1)

df.to_csv('output/anomaly_flags.csv', index=False)

print("AI Anomaly Detection Complete! Check the output folder for anomaly_flags.csv and kpi_summary.json.")