import pandas as pd
import numpy as np

lfm2b_spotify_uri = './lfm2b/spotify-uris.tsv'
lfm2b_genre = './lfm2b/tags-micro-genres.json'
music4all_metadata = './music4all/id_metadata.csv'
# load item's genre from lfm2b
lfm2b_spotify_uri = pd.read_csv(lfm2b_spotify_uri, delimiter='\t', header=0, index_col=0)
lfm2b_genre = pd.read_json(lfm2b_genre, lines=True)
lfm2b_genre['artist'] = [list(i.values())[0] for i in list(lfm2b_genre['_id'])]
lfm2b_genre['track'] = [list(i.values())[1] for i in list(lfm2b_genre['_id'])]
lfm2b_genre.drop(columns=['_id'], inplace=True)
lfm2b_genre.drop(columns=['track'], inplace=True)
lfm2b_genre['tags'] = [list(i)[0] for i in list(lfm2b_genre['tags'])]

lfm2b_genre.set_index('i', inplace=True)
# get item id which has genre and spotify uri
uri_genre_subset = np.intersect1d(pd.unique(lfm2b_spotify_uri.index), pd.unique(lfm2b_genre.index))
# creat a new dataframe with lfm2b'sid,uri,genre,artist
new_meta = {'id': [i for i in uri_genre_subset],
            'uri': [lfm2b_spotify_uri.loc[i].uri for i in uri_genre_subset],
            'genre': [lfm2b_genre.loc[i].tags for i in uri_genre_subset],
            'artist': [lfm2b_genre.loc[i].artist for i in uri_genre_subset]}
new_meta = pd.DataFrame(data=new_meta)
new_meta.to_csv("./lfm2b/meta_lfm2b_uri_subset.csv")

music4all_metadata = pd.read_csv(music4all_metadata, delimiter='\t', header=0, usecols=[0, 1])
# get subset between music4all and lfm2b
lfm2b_uri_set = pd.unique(new_meta['uri'])
music4all_uri_set = pd.unique(music4all_metadata['spotify_id'])
lfm2b_music4all_subset = np.intersect1d(lfm2b_uri_set, music4all_uri_set)
print('lfm2b uri number : ', len(lfm2b_uri_set))
print('music4all track number : ', len(pd.unique(music4all_metadata['id'])))
print('music4all uri number : ', len(music4all_uri_set))
print('subset number : ', len(lfm2b_music4all_subset))
# add lfm2b's genre and artist to music4all
new_meta.set_index('uri', inplace=True)
music4all_metadata = music4all_metadata[music4all_metadata['spotify_id'].isin(lfm2b_music4all_subset)]
# get genre and artist
genre_list = []
artist_list =[]
for index, row in music4all_metadata.iterrows():
    if isinstance(new_meta.loc[row.spotify_id], pd.core.series.Series):
        genre_list.append(new_meta.loc[row.spotify_id].genre)
        artist_list.append(new_meta.loc[row.spotify_id].artist)
    elif isinstance(new_meta.loc[row.spotify_id], pd.core.frame.DataFrame):
        genre_list.append(new_meta.loc[row.spotify_id].iloc[0].genre)
        artist_list.append(new_meta.loc[row.spotify_id].iloc[0].artist)
    else:
        print('error')

music4all_metadata['genre'] = genre_list
music4all_metadata['artist'] = artist_list

music4all_metadata.to_csv("./subset/meta_lfm2b_uri_music4all_subset.csv", index=False)