import pandas as pd
def load_excel_to_dataframe(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        yearly_links_split = [xls.parse(sheet_name) for sheet_name in xls.sheet_names]
        return yearly_links_split
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

file_path = 'yearly_links_split.xlsx'
yearly_links_split = load_excel_to_dataframe(file_path)
unique_pairs_list = [df.drop_duplicates(subset=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT']) for df in yearly_links_split]
pairs_as_tuples = [set(zip(df['SOURCE_SUBREDDIT'], df['TARGET_SUBREDDIT'])) for df in unique_pairs_list]
common_pairs = set.intersection(*pairs_as_tuples)
filtered_yearly_links_split = [
    df[df.apply(lambda row: (row['SOURCE_SUBREDDIT'], row['TARGET_SUBREDDIT']) in common_pairs, axis=1)]
    for df in yearly_links_split
]
all_ids = set()
for df in filtered_yearly_links_split:
    all_ids.update(df['SOURCE_SUBREDDIT'])
    all_ids.update(df['TARGET_SUBREDDIT'])
print(f"Total unique ids: {len(all_ids)}")
with open('unique_ids.csv', 'w') as f:
    for id in all_ids:
        f.write(f"{id}\n")
for i, df in enumerate(filtered_yearly_links_split):
    df.to_csv(f'yearly_links_{i}.csv', index=False)