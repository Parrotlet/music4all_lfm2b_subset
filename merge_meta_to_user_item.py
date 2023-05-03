import pandas as pd
import numpy as np

users_path = "./final_data/user_ids.csv"
items_path = "./final_data/item_ids.csv"
users_meta_path = "./lfm2b/users.tsv"
music4all_meta_path = "./music4all/id_metadata.csv"
music4all_info_path = "./music4all/id_information.csv"
music4all_genres_path = "./music4all_onion/id_genres_tf-idf.tsv"
# load users
users = pd.read_csv(users_path, sep=',', header=0)
# load items
items = pd.read_csv(items_path, sep=',', header=0)
# load user meta
users_meta = pd.read_csv(users_meta_path, delimiter='\t', header=0, index_col= 0)
# add user meta data to users
# country = [users_meta[users_meta['user_id'].eq(i)].iloc[0].country for i in users['old_user_id']]
# age = [users_meta[users_meta['user_id'].eq(i)].iloc[0].age for i in users['old_user_id']]
# gender = [users_meta[users_meta['user_id'].eq(i)].iloc[0].gender for i in users['old_user_id']]
country = []
age = []
gender = []
for i in users['old_user_id']:
    country.append(users_meta.loc[i].country)
    age.append(users_meta.loc[i].age)
    gender.append(users_meta.loc[i].gender)
users['country'] = country
users['age'] = age
users['gender'] = gender
print('Unique country number:', len(pd.unique(users['country'])))
users.to_csv("./final_data/user_ids_meta.csv", index=False)

# add item meta data to items

music4all_meta = pd.read_csv(music4all_meta_path, header=0, usecols=[0, 4, 5, 6, 7, 8, 9], index_col=0, delimiter='\t')
music4all_meta.rename(columns={'mode': 'mode_'}, inplace=True)
music4all_info = pd.read_csv(music4all_info_path, header=0, usecols=[0, 1], index_col=0, delimiter='\t')
music4all_genres = pd.read_csv(music4all_genres_path, delimiter='\t', header=0, index_col=0)
music4all_genres['genre'] = music4all_genres.idxmax(axis=1)
music4all_genres = music4all_genres['genre']
# popularity = []
danceability = []
energy = []
key = []
mode = []
valence = []
tempo = []
artist = []
genre = []
for i in items['old_item_id']:
    # popularity.append(music4all_meta.loc[i].popularity / 100)
    danceability.append(music4all_meta.loc[i].danceability)
    energy.append(music4all_meta.loc[i].energy)
    key.append(music4all_meta.loc[i].key)
    mode.append(music4all_meta.loc[i].mode_)
    valence.append(music4all_meta.loc[i].valence)
    tempo.append(music4all_meta.loc[i].tempo / (music4all_meta['tempo'].max()))
    artist.append(music4all_info.loc[i].artist)
    genre.append(music4all_genres.loc[i])
# items['popularity'] = popularity
items['danceability'] = danceability
items['energy'] = energy
items['valence'] = valence
items['tempo'] = tempo
items['key'] = key
items['mode'] = mode
items['artist'] = artist
items['genre'] = genre
#
# print('Unique artist number:', len(pd.unique(items['artist'])))
# print('Unique genre number:', len(pd.unique(items['genre'])))
#
items.drop(columns=['danceability', 'energy', 'valence', 'tempo', 'key', 'mode'], inplace=True)
items.to_csv("./final_data/items_ids_meta.csv", index=False)


