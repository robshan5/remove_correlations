import os
import sys

import numpy as np
import pandas as pd

# Error Checking
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python main.py [csv_file] [Optional: correlation threshold]")
    exit(1)

path = sys.argv[1]
if not os.path.exists(path):
    print("File not found")
    exit(2)

THRESHOLD = 0.5
if len(sys.argv) == 3:
    try:
        THRESHOLD = float(sys.argv[2])
    except:
        print("invalid threshold, please use a float between 0 to 1")
        exit(3)

if not 0 < THRESHOLD < 1:
    print("invalid threshold, please use a float between 0 to 1")
    exit(3)

print(THRESHOLD)


# reading the file
with open(path) as file:
    """
    read file as dataframe
    normalise all predictors
    detect correlation between predictors
    eliminate correlated predictors
    """
    df = pd.read_csv(file)

    # finding all categorical columns and converting them to numerical data
    cat_cols = df.select_dtypes(include=["object", "category"]).columns

    df = pd.get_dummies(df, columns=cat_cols, drop_first=False)
    df = df.astype({col: "int" for col in df.select_dtypes(include="bool").columns})

    # normalising the dataframe columns
    df = (df - df.min()) / (df.max() - df.min())

    # detecting correlations in the dataframe
    correlations = df.corr().to_numpy()
    correlations = np.tril(correlations)

    # removing correlated columns
    for i in range(correlations.shape[1]):
        for j in range(0, i):
            if correlations[i, j] > THRESHOLD and i != j:
                print(f"Columns '{df.columns[i]}' and '{df.columns[j]}' are correlated")
                while True:
                    print(f"Remove 1){df.columns[i]} or 2){df.columns[j]}")
                    col = input()
                    try:
                        col = int(col)
                    except:
                        print("Enter float between 0-1")
                    if col == 1:
                        df = df.drop(df.columns[[i]].tolist(), axis=1)
                        print(f"Removing {df.columns[i]}")
                        break
                    elif col == 2:
                        df = df.drop(df.columns[[j]].tolist(), axis=1)
                        print(f"Removing {df.columns[j]}")
                        break

    result = path[:-4] + "_independent.csv"
    print(f"New csv {result} created with no correlated columns")
    df.to_csv(result)
