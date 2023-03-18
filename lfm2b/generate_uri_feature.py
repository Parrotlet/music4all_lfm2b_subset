import pandas as pd
import numpy as np

lfm2b_spotify_uri = 'spotify-uris.tsv'
lfm2b_gerne = 'tags-micro-genres.json'
music4all_metadata = 'id_metadata.csv'
# load item's gerne from lfm2b
lfm2b_spotify_uri = pd.read_csv(lfm2b_spotify_uri, delimiter='\t', header=0, index_col=0)
lfm2b_gerne = pd.read_json(lfm2b_gerne, lines=True)
lfm2b_gerne['artist'] = [list(i.values())[0] for i in list(lfm2b_gerne['_id'])]
lfm2b_gerne['track'] = [list(i.values())[1] for i in list(lfm2b_gerne['_id'])]
lfm2b_gerne.drop(columns=['_id'], inplace=True)
lfm2b_gerne.drop(columns=['track'], inplace=True)
lfm2b_gerne['tags'] = [list(i)[0] for i in list(lfm2b_gerne['tags'])]

lfm2b_gerne.set_index('i', inplace=True)
# get item id which has gerne and spotify uri
uri_gerne_subset = np.intersect1d(pd.unique(lfm2b_spotify_uri.index), pd.unique(lfm2b_gerne.index))
# creat a new dataframe with lfm2b'sid,uri,genre,artist
new_meta = {'id': [i for i in uri_gerne_subset],
            'uri': [lfm2b_spotify_uri.loc[i].uri for i in uri_gerne_subset],
            'genre': [lfm2b_gerne.loc[i].tags for i in uri_gerne_subset],
            'artist': [lfm2b_gerne.loc[i].artist for i in uri_gerne_subset]}
new_meta = pd.DataFrame(data=new_meta)
new_meta.to_csv("meta_lfm2b_uri_subset.csv")

music4all_metadata = pd.read_csv(music4all_metadata, delimiter='\t', header=0, usecols=[0, 1])
# get subset between music4all and lfm2b
lfm2b_uri_set = pd.unique(new_meta['uri'])
music4all_uri_set = pd.unique(music4all_metadata['spotify_id'])
lfm2b_music4all_subset = np.intersect1d(lfm2b_uri_set, music4all_uri_set)
print('lfm2b uri number : ', len(lfm2b_uri_set))
print('music4all track number : ', len(pd.unique(music4all_metadata['id'])))
print('music4all uri number : ', len(music4all_uri_set))
print('subset number : ', len(lfm2b_music4all_subset))

