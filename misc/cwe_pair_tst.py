import pandas as pd
import os
import numpy as np

# Define the directory path to start the search
directory_path = r"D:\grad_research_2\misc\results_cwe"
df = pd.DataFrame(columns=['cwe','P-C','P-V','P-B','P-R'])

# Loop through the directory and its subdirectories
for root, dirs, files in os.walk(directory_path):
    for file in files:
        # Check if the file contains 'cwe' and ends with '.csv'
        if 'outcome_counts_by_cwe' in file.lower() and file.endswith('.csv') and 'old' not in root and 'anthropic' not in root and "bryson" not in root:
            pth = os.path.join(root, file)
            df2 = pd.read_csv(pth, header=0)
            df = pd.concat([df, df2])
            print(pth)

result = df.groupby('cwe', as_index=False).sum()  
denominator = result['P-V'] + result['P-B'] + result['P-R']
denominator = denominator.replace(0, np.nan)
result['score'] = result['P-C'] / denominator

sorted_grouped = result.sort_values(by='score', ascending=False)
sorted_grouped = sorted_grouped.drop('true_cwe', axis=1)
sorted_grouped.columns = ['cwe', 'PC', 'PV', 'PB', 'PR', 'score']

# Convert all columns that can be numeric to numeric
sorted_grouped = sorted_grouped.apply(pd.to_numeric, errors='ignore')

# Round numeric columns to 3 decimal places
sorted_grouped = sorted_grouped.round(3)

print(sorted_grouped)

sorted_grouped.to_csv('misc/results/cwe_pairwise_scoring.csv', index=False)