import pandas as pd

df = pd.read_csv('output/clean_data.csv', parse_dates=['Date'])

df = df.drop_duplicates()

df.ffill(inplace=True)

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Week'] = df['Date'].dt.isocalendar().week

df['Revenue_Lag1'] = df['Revenue'].shift(1)
df['Revenue_MA7'] = df['Revenue'].rolling(window=7).mean()

mean_rev = df['Revenue'].mean()
std_rev = df['Revenue'].std()
q1 = df['Revenue'].quantile(0.25)
q3 = df['Revenue'].quantile(0.75)
iqr = q3 - q1

stats = {'mean': mean_rev, 'std': std_rev, 'iqr': iqr}
pd.Series(stats).to_csv('output/baseline_stats.csv')

df.to_csv('output/processed_data.csv', index=False)

print("Data Processing Complete! Check your output folder for processed_data.csv and baseline_stats.csv.")