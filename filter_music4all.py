import pandas as pd

items_path = "./final_data/item_ids.csv"
music4all_ivec256_path = "./music4all_onion/id_ivec256.tsv"
music4all_lyric_tf_path = "./music4all_onion/id_lyrics_tf-idf.tsv"


def last_column_to_first(df):
    num_cols = len(df.columns)
    cols = [num_cols - 1] + list(range(num_cols - 1))
    df = df.iloc[:, cols]
    return df


items = pd.read_csv(items_path, sep=',', header=0)
id_set = pd.unique(items['old_item_id'])
items.set_index('old_item_id', inplace=True)
music4all_ivec256 = pd.read_csv(music4all_ivec256_path, delimiter='\t', header=0)
music4all_lyric_tf = pd.read_csv(music4all_lyric_tf_path, delimiter='\t', header=0)

music4all_ivec256 = music4all_ivec256[music4all_ivec256['id'].isin(id_set)]
music4all_lyric_tf = music4all_lyric_tf[music4all_lyric_tf['id'].isin(id_set)]
music4all_ivec256.set_index('id', inplace=True)
music4all_lyric_tf.set_index('id', inplace=True)
music4all_ivec256_id = [items.loc[i].iloc[0] for i, r in music4all_ivec256.iterrows()]
music4all_lyric_tf_id = [items.loc[i].iloc[0] for i, r in music4all_lyric_tf.iterrows()]
music4all_ivec256['id'] = music4all_ivec256_id
music4all_lyric_tf['id'] = music4all_lyric_tf_id
music4all_ivec256 = last_column_to_first(music4all_ivec256)
music4all_lyric_tf = last_column_to_first(music4all_lyric_tf)

music4all_ivec256.to_csv("./final_data/items_ids_ivec256_filter.csv", index=False)
music4all_lyric_tf.to_csv("./final_data/items_ids_lyric_tf_filter.csv", index=False)
