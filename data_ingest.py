import pandas as pd


df = pd.read_excel('data/synthetic_financials.xlsx', parse_dates=['Date'])

df.sort_values('Date', inplace=True)

df.to_csv('output/clean_data.csv', index=False)

print("Data Ingestion Complete! Clean CSV saved in the output folder.")