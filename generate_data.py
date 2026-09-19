import pandas as pd
import numpy as np

dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
np.random.seed(0)

revenue = 1000 + 50*np.sin(2*np.pi*dates.dayofyear.to_numpy()/365) + np.random.normal(0, 30, len(dates))

revenue[100] *= 3   
revenue[200] /= 2    

df = pd.DataFrame({'Date': dates, 'Revenue': revenue})
df.to_excel('data/synthetic_financials.xlsx', index=False)

print("Success! The fake financial data has been created in the 'data' folder.")