import os
import dotenv
import json
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dotenv.load_dotenv()

def get_primevul_pairs(idxs):
    with open(os.getenv('PRIMEVUL'), "r") as f:
        samples = f.readlines()
    samples = [json.loads(sample) for sample in samples]

    # Step 1: Group relevant idx values by commit_url and file_name
    alpha_groups = defaultdict(list)
    for sample in samples:
        sample_idx = sample.get("idx")
        if sample_idx in idxs:  # Only consider idxs in the provided list
            key = (sample.get("commit_url", None),None)
            alpha_groups[key].append(sample_idx)

    unpaired = {}
    fixed = {}
    rem_keys = []
    for key, sublist in alpha_groups.items():
        if len(sublist) > 2:
            rem_keys.append(key)
            print("\nToo many values in this group!")
            print(sublist)
            fixed_ids = []
            for i in range(0, len(sublist)//2):
                while True:
                    pair = input("Enter a pair of IDs separated by a comma: ")
                    split_pair = list(map(lambda x: int(x.strip()), pair.split(',')))
                    if len(split_pair) > 2:
                        print("Entry contains too many values. Please enter the IDs in pairs.")
                    elif split_pair[0] not in sublist or split_pair[1] not in sublist:
                        print("Invalid IDs entered, please try again.")
                    # elif split_pair[0] in fixed_ids or split_pair[1] in fixed_ids:
                    #     print('At least one of these IDs have already been paired, please try again.')
                    else:
                        break
                fixed[(key[0], key[1] or i)] = split_pair
                fixed_ids.extend(split_pair)
            if len(sublist)%2 != 0:
                for val in sublist:
                    if val not in fixed_ids:
                        unpaired[val] = key
        elif len(sublist) < 2:
            rem_keys.append(key)
            for val in sublist:
                unpaired[val] = key
    
    isNone = False
    while len(unpaired) > 0:
        print("\nUNPAIRED:")
        valid_ids = []
        for id, key in unpaired.items():
            print(key, id) 
            valid_ids.append(id)

        while True:
            pair = input("Enter a pair of IDs separated by a comma, or -1 if no pairs exist: ")
            split_pair = list(map(lambda x: int(x.strip()), pair.split(',')))
            if split_pair[0] == -1:
                isNone = True
                break
            if len(split_pair) > 2:
                print("Entry contains too many values. Please enter the IDs in pairs.")
            elif split_pair[0] not in valid_ids or split_pair[1] not in valid_ids:
                print("Invalid IDs entered, please try again.")
            else:
                break
        if isNone:
            break
        else:
            fixed[(unpaired[split_pair[0]],unpaired[split_pair[1]])] = split_pair
            del unpaired[split_pair[0]]
            del unpaired[split_pair[1]]

    for key in rem_keys:
        del alpha_groups[key]

    alpha_groups.update(fixed)

    return alpha_groups.values()

def calculate_pairwise_outcomes(df):
    """
    Calculate pairwise outcomes (P-C, P-V, P-B, P-R) for each pair of idx values.

    Args:
        df (pandas.DataFrame): DataFrame containing the CSV data.
        pairs (list of tuples): List of idx pairs.

    Returns:
        pandas.DataFrame: DataFrame with the pairwise outcomes.
    """

    # Get pairs:
    idxs = df['idx'].astype(int).tolist()
    pairs = get_primevul_pairs(idxs)

    # Create a mapping from idx to its true_vuln and predicted_vuln for fast lookup
    idx_map = df.set_index('idx')[['true_vuln', 'predicted_vuln', 'cwe']]

    # Initialize a list to store the results
    outcomes = []

    # Loop through each pair
    for idx1, idx2 in pairs:
        # Get the true and predicted values for both idxs
        true_vuln_1 = idx_map.loc[idx1, 'true_vuln']
        pred_vuln_1 = idx_map.loc[idx1, 'predicted_vuln']
        true_vuln_2 = idx_map.loc[idx2, 'true_vuln']
        pred_vuln_2 = idx_map.loc[idx2, 'predicted_vuln']
        cwe = idx_map.loc[idx1, 'cwe']
        # Determine the outcome for the pair
        if true_vuln_1 == pred_vuln_1 and true_vuln_2 == pred_vuln_2:
            outcome = 'P-C'  # Pair-wise Correct Prediction
        elif (true_vuln_1 == pred_vuln_2) and (true_vuln_2 == pred_vuln_1):
            outcome = 'P-R'  # Pair-wise Reversed Prediction
        elif (true_vuln_1 != pred_vuln_1 or true_vuln_2 != pred_vuln_2) and (pred_vuln_1 == pred_vuln_2):
            if pred_vuln_1 == 0:
                outcome = 'P-B'  # Pair-wise Benign Prediction
            else:
                outcome = 'P-V'  # Pair-wise Vulnerable Prediction
        else:
            print({
            'idx1': idx1,
            'idx2': idx2,
            'true_vuln_1': true_vuln_1,
            'pred_vuln_1': pred_vuln_1,
            'true_vuln_2': true_vuln_2,
            'pred_vuln_2': pred_vuln_2,
            'outcome': "FAILURE",
            'cwe': cwe
        })
            
            continue  # If no match, skip (although shouldn't happen with proper pairs)

        # Append the result
        outcomes.append({
            'idx1': idx1,
            'idx2': idx2,
            'true_vuln_1': true_vuln_1,
            'pred_vuln_1': pred_vuln_1,
            'true_vuln_2': true_vuln_2,
            'pred_vuln_2': pred_vuln_2,
            'outcome': outcome,
            'cwe': cwe
        })

    # Create a DataFrame from the outcomes
    return pd.DataFrame(outcomes)

def generate_outcome_graphs(src_df, SHOW, ROOT_PTH):
    """
    Generate bar graphs for counts and rates of outcomes, including grouping by CWE.
    Even if some outcomes don't exist in the DataFrame, they will be displayed in the graph.
    """
    df = calculate_pairwise_outcomes(src_df)
    # Sum four specific columns and store the result in a new column
    df.to_csv(ROOT_PTH + '/outcomes_paired.csv', index=False)

    # Define all possible outcomes to ensure they appear in the graph, even if missing in the DataFrame
    all_outcomes = ['P-C', 'P-V', 'P-B', 'P-R']

    # Step 1: Explode the CWE array into separate rows
    df_exploded = df.explode('cwe')

    # Step 2: Count total occurrences of each outcome, ensuring all outcomes are included
    outcome_counts = df['outcome'].value_counts().reindex(all_outcomes, fill_value=0).reset_index()
    outcome_counts.columns = ['Outcome', 'Count']
    outcome_counts.to_csv(ROOT_PTH + '/outcome_counts.csv', index=False)

    # Step 3: Calculate rates of each outcome
    total_pairs = len(df)
    outcome_rates = outcome_counts.copy()
    outcome_rates['Rate'] = outcome_rates['Count'] / total_pairs

    # Save outcome rates to CSV
    outcome_rates = outcome_rates[['Outcome', 'Rate']]
    outcome_rates.to_csv(ROOT_PTH + '/outcome_rates.csv', index=False)

    # Step 4: Group counts and rates by CWE
    # Group counts by 'cwe' and 'outcome', ensure all outcomes are included
    cwe_outcome_counts = (
        df_exploded.groupby(['cwe', 'outcome'])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=all_outcomes, fill_value=0)
    )

    # Reset the index to include CWEs as a column in the saved CSV
    cwe_outcome_counts = cwe_outcome_counts.reset_index()

    # Save the counts to CSV
    cwe_outcome_counts.to_csv(ROOT_PTH + '/outcome_counts_by_cwe.csv', index=False)

    # Calculate rates by dividing each count by the total per CWE
    cwe_outcome_rates = cwe_outcome_counts.set_index('cwe')
    cwe_outcome_rates = cwe_outcome_rates.div(cwe_outcome_rates.sum(axis=1), axis=0).reset_index()

    # Save the rates to CSV
    cwe_outcome_rates.to_csv(ROOT_PTH + '/outcome_rates_by_cwe.csv', index=False)


    # Step 5: Generate Bar Graphs
    # Count Bar Graph (overall)
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Outcome', y='Count', hue='Outcome', data=outcome_counts,  palette='Set2')
    plt.title("Counts of Outcomes")
    plt.ylabel("Count")
    plt.xlabel("Outcome")
    plt.savefig(ROOT_PTH + '/outcome_counts.png')
    plt.show() if SHOW else None

    # Rate Bar Graph (overall)
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Outcome', y='Rate', hue='Outcome', data=outcome_rates,  palette='Set2')
    plt.title("Rates of Outcomes")
    plt.ylabel("Rate")
    plt.xlabel("Outcome")
    plt.savefig(ROOT_PTH + '/outcome_rates.png')
    plt.show() if SHOW else None

    # Outcome Counts Grouped by CWE
    plt.figure(figsize=(14, 8))  # Increase figure size for readability
    sns.barplot(
        x='Outcome',
        y='Count',
        hue='cwe',
        data=cwe_outcome_counts.melt(id_vars=['cwe'], var_name='Outcome', value_name='Count'),
        palette='tab20',
        errorbar=None
    )
    plt.title('Counts of Outcomes Grouped by CWE')
    plt.xlabel('Outcome')
    plt.ylabel('Count')
    plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
    plt.legend(title='CWE', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend position
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.savefig(ROOT_PTH + '/outcome_counts_by_cwe.png')
    plt.show() if SHOW else None


    # Outcome Rates Grouped by CWE
    plt.figure(figsize=(14, 8))  # Increase figure size for readability
    sns.barplot(
        x='Outcome', 
        y='Rate', 
        hue='cwe', 
        data=cwe_outcome_rates.melt(id_vars=['cwe'], var_name='Outcome', value_name='Rate'), 
        palette='tab20', 
        errorbar=None
    )
    plt.title('Rates of Outcomes Grouped by CWE')
    plt.xlabel('Outcome')
    plt.ylabel('Rate')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.legend(title='CWE', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend position
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.savefig(ROOT_PTH + '/outcome_rates_by_cwe.png')
    plt.show() if SHOW else None

# import ast
# # # Load CSV into DataFrame, skipping the first row and stripping whitespace from headers
# file_path = 'outputs/verdicts.csv'  # Replace with your file path
# df = pd.read_csv(file_path, header=0)
# df.columns = df.columns.str.strip()  # Remove any leading/trailing whitespace
# df['cwe'] = df['cwe'].apply(ast.literal_eval)
# pairwise_df = calculate_pairwise_outcomes(df)
# print(pairwise_df)
# generate_outcome_graphs(pairwise_df)