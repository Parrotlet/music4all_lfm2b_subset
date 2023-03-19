import pandas as pd
import numpy as np

lfm2b_spotify_uri = './lfm2b/spotify-uris.tsv'
lfm2b_track = './lfm2b/tracks.tsv'
music4all_metadata = './music4all/id_metadata.csv'

# load track's artist from lfm2b
lfm2b_track = pd.read_csv(lfm2b_track, delimiter='\t', header=0, index_col=0,usecols=[0, 1])
# load spotify_uri from lfm2b
lfm2b_spotify_uri = pd.read_csv(lfm2b_spotify_uri, delimiter='\t', header=0, index_col=0)

# get item id which has spotify uri
uri_artist_subset = np.intersect1d(pd.unique(lfm2b_spotify_uri.index), pd.unique(lfm2b_track.index))
# creat a new dataframe with lfm2b'sid,uri,artist
new_meta = {'id': [i for i in uri_artist_subset],
            'uri': [lfm2b_spotify_uri.loc[i].uri for i in uri_artist_subset],
            'artist': [lfm2b_track.loc[i].artist_name for i in uri_artist_subset]}
new_meta = pd.DataFrame(data=new_meta)
new_meta.to_csv("./lfm2b/artist_lfm2b_uri_subset.csv")

music4all_metadata = pd.read_csv(music4all_metadata, delimiter='\t', header=0, usecols=[0, 1])
# get subset between music4all and lfm2b
lfm2b_uri_set = pd.unique(new_meta['uri'])
music4all_uri_set = pd.unique(music4all_metadata['spotify_id'])
lfm2b_music4all_subset = np.intersect1d(lfm2b_uri_set, music4all_uri_set)
print('lfm2b uri number : ', len(lfm2b_uri_set))
print('music4all track number : ', len(pd.unique(music4all_metadata['id'])))
print('music4all uri number : ', len(music4all_uri_set))
print('subset number : ', len(lfm2b_music4all_subset))
# add lfm2b's artist to music4all
new_meta.set_index('uri', inplace=True)
music4all_metadata = music4all_metadata[music4all_metadata['spotify_id'].isin(lfm2b_music4all_subset)]
# get artist
artist_list =[]
for index, row in music4all_metadata.iterrows():
    if isinstance(new_meta.loc[row.spotify_id], pd.core.series.Series):
        artist_list.append(new_meta.loc[row.spotify_id].artist)
    elif isinstance(new_meta.loc[row.spotify_id], pd.core.frame.DataFrame):
        artist_list.append(new_meta.loc[row.spotify_id].iloc[0].artist)
    else:
        print('error')

music4all_metadata['artist'] = artist_list

music4all_metadata.to_csv("./final_data/artist_lfm2b_uri_music4all_subset.csv", index=False)