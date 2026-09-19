import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output/anomaly_flags.csv', parse_dates=['Date'])

df_anomalies = df[df['anomaly_combined'] == True]

with pd.ExcelWriter('output/anomaly_report.xlsx') as writer:
    df_anomalies.to_excel(writer, sheet_name='Anomalies', index=False)
    kpis = pd.read_csv('output/baseline_stats.csv')
    kpis.to_excel(writer, sheet_name='Baseline Stats', index=False)

plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Revenue'], label='Normal Revenue', color='blue')
plt.scatter(df_anomalies['Date'], df_anomalies['Revenue'], color='red', label='Anomaly Detected', zorder=5)
plt.title('Financial Anomaly Detection Dashboard')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.legend()
plt.grid(True)
plt.savefig('output/anomaly_dashboard.png')
plt.close()

summary_text = f"Total anomalies detected: {len(df_anomalies)}\n\n"
for index, row in df_anomalies.iterrows():
    summary_text += f"Date: {row['Date'].strftime('%Y-%m-%d')} | Revenue: {row['Revenue']:.2f} | Reason: Flagged by AI pipeline.\n"

with open('output/anomaly_summary.txt', 'w') as f:
    f.write(summary_text)

print("Reporting Complete! Check your output folder for the Excel report, Dashboard image, and Summary text.")