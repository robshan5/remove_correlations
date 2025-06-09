# Remove Correlations
Automatically removes correlated columns from a csv file

## Usage
`python main.py [csv_file] [optional: correlation threshold]`
- After it's run, if it finds two correlated columns it will ask whether to delete one of the two columns
- It will keep running until it has searched all column pairs and then return a new csv without any correlations
