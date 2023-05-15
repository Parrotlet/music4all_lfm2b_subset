import pandas as pd
items_ids_meta = pd.read_csv("items_ids_meta2.csv")
listening_history_train = pd.read_csv("listening_history_train.csv")
items_ids_meta['count']=0
for index, row in items_ids_meta.iterrows():
    # Access the row data
    item_id = row['item_id']
    count = listening_history_train['item_id'].value_counts()[item_id]

    # Set the value in the original dataframe
    items_ids_meta.at[index, 'count'] = count
items_ids_meta.to_csv("items_ids_meta2_count.csv", index=False)
