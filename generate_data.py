import pandas as pd
import numpy as np

def get_id_dict(lfm2b_spotify_uri, music4all_metadata):
    # load spotify uri vs lfm2b track id data
    lfm2b_spotify_uri = pd.read_csv(lfm2b_spotify_uri, delimiter='\t', header=0)
    music4all_metadata = pd.read_csv(music4all_metadata, delimiter='\t', header=0, usecols=[0, 1])
    lfm2b_uri_set = pd.unique(lfm2b_spotify_uri['uri'])
    music4all_uri_set = pd.unique(music4all_metadata['spotify_id'])
    lfm2b_music4all_subset = np.intersect1d(lfm2b_uri_set, music4all_uri_set)
    print('lfm2b track number : ', len(pd.unique(lfm2b_spotify_uri['track_id'])))
    print('lfm2b uri number : ', len(lfm2b_uri_set))
    print('music4all track number : ', len(pd.unique(music4all_metadata['id'])))
    print('music4all uri number : ', len(music4all_uri_set))
    print('subset number : ', len(lfm2b_music4all_subset))


lfm2b_spotify_uri = './lfm2b/spotify-uris.tsv'
music4all_metadata = './music4all/id_metadata.csv'

get_id_dict(lfm2b_spotify_uri, music4all_metadata)