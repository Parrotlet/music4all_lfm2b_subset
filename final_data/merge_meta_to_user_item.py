import pandas as pd
import numpy as np

users_path="./user_ids.csv"
items_path="./item_ids.csv"
users_meta_path="./users.tsv"
tags_micro_genres_path = "./tags-micro-genres.json"
# load users
users = pd.read_csv(users_path, sep=',', header=0)
# load items
items = pd.read_csv(items_path, sep=',', header=0)
# load user meta
users_meta = pd.read_csv(users_meta_path, delimiter='\t', header=0)
# process tags
tags_micro_genres = pd.read_json(tags_micro_genres_path, lines=True)
tags_micro_genres['artist'] = [list(i.values())[0] for i in list(tags_micro_genres['_id'])]
tags_micro_genres['track'] = [list(i.values())[1] for i in list(tags_micro_genres['_id'])]
tags_micro_genres.drop(columns=['_id'], inplace=True)
tags_micro_genres['tags'] = [list(i)[0] for i in list(tags_micro_genres['tags'])]
# print('Unique tags number:', len(pd.unique(tags_micro_genres['tags'])))

# add user meta data to users

country = [users_meta[users_meta['user_id'].eq(i)].iloc[0].country for i in users['old_user_id']]
age = [users_meta[users_meta['user_id'].eq(i)].iloc[0].age for i in users['old_user_id']]
gender = [users_meta[users_meta['user_id'].eq(i)].iloc[0].gender for i in users['old_user_id']]

users['country'] = country
users['age'] = age
users['gender'] = gender
print('Unique country number:', len(pd.unique(users['country'])))

# add item meta data to items

tag = [tags_micro_genres[tags_micro_genres['i'].eq(i)].iloc[0].tags for i in items['old_item_id']]
artist = [tags_micro_genres[tags_micro_genres['i'].eq(i)].iloc[0].artist for i in items['old_item_id']]

items['tag'] = tag
items['artist'] = artist
print('Unique tag number:', len(pd.unique(items['tag'])))
print('Unique artist number:', len(pd.unique(items['artist'])))

users.to_csv("./user_ids_meta.csv", index=False)
items.to_csv("./item_ids_meta.csv", index=False)

