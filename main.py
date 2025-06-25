import argparse
import fileinput

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

COLUMNS = ""
THRESHOLD = 0.5

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--file", "-f", type=str, required=True, help="Define the csv file to be checked"
)
parser.add_argument(
    "--columns", "-c", type=str, help="Define file that lists columns to be used"
)
parser.add_argument(
    "--threshold",
    "-t",
    type=float,
    help="Define threshold value for the correlation coefficient",
)
args = parser.parse_args()

if args.columns:
    COLUMNS = args.columns

if args.threshold:
    try:
        THRESHOLD = float(args.threshold)
    except:
        print("invalid threshold, please use a float between 0 to 1")
        exit(3)
    if not 0 < THRESHOLD < 1:
        print("invalid threshold, please use a float between 0 to 1")
        exit(3)

path = args.file

# reading the file
with open(path) as file:
    """
    read file as dataframe
    normalise all predictors
    detect correlation between predictors
    eliminate correlated predictors
    """
    df = pd.read_csv(file)

    cols = []
    if args.columns:
        for line in fileinput.input(files=COLUMNS):
            cols.append(line.strip())
    else:
        cols = df.columns

    full = df
    df = df[cols]

    # finding all categorical columns and converting them to numerical data
    cat_cols = df.select_dtypes(include=["object", "category"]).columns

    df = pd.get_dummies(df, columns=cat_cols, drop_first=False)
    df = df.astype({col: "int" for col in df.select_dtypes(include="bool").columns})

    # normalising the dataframe columns
    df = (df - df.min()) / (df.max() - df.min())

    # detecting correlations in the dataframe
    correlations = df.corr().to_numpy()
    correlations = np.tril(correlations)

    matches = [
        (i, j)
        for i in range(correlations.shape[1])
        for j in range(correlations.shape[0])
        if correlations[i, j] >= THRESHOLD and i != j
    ]

    deleteList = []
    for i, j in matches:
        print(f"Columns 1){df.columns[i]} and 2){df.columns[j]} are correlated")
        while True:
            print(f"Remove (1, 2): ", end="")
            col = input()
            rem = 0

            try:
                col = int(col)
            except:
                print("Enter float between 0-1")

            if col == 1:
                rem = i
            elif col == 2:
                rem = j

            deleteList.append(df.columns[rem])
            print()
            break

    df = full.drop(deleteList, axis=1)

    result = path[:-4] + "_independent.csv"
    df.to_csv(result)
    print(f"\nNew csv {result} created!")

    graph = sns.pairplot(df, kind="kde")
    graph.figure.savefig("correlations.png", dpi = 300, bbox_inches="tight")
    print(f"\nPair plot graph created!")
