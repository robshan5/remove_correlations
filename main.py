import os
import sys

import numpy as np
import pandas as pd
import seaborn as sns

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Enter csv file as an argument")
    print(
        "Optional: change default correlation threshold, enter float value after file name"
    )
    exit(1)

path = sys.argv[1]
if not os.path.exists(path):
    print("File not found")
    exit(2)


with open(path) as file:
    """
    read file as dataframe
    normalise all predictors
    detect correlation between predictors
    eliminate correlated predictors
    """
    df = pd.read_csv(file)

    # normalising the dataframe columns
    normalized_df = (df - df.min()) / (df.max() - df.min())

    # detecting correlations in the dataframe
    correlations = df.corr().to_numpy()
    correlations = np.tril(correlations)

    # removing correlated columns
    for i in range(correlations.shape[1]):
        for j in range(0, i):
            if correlations[i, j] > 0.5 and i != j:
                print(
                    f"Columns '{df.columns[i]}' and '{df.columns[j]}' are correlated: removing '{df.columns[j]}'"
                )
                df = df.drop(df.columns[[j]].tolist(), axis=1)

    result = path[:-4] + "_independent.csv"
    print(f"New csv {result} created with no correlated columns")
    df.to_csv(result)
