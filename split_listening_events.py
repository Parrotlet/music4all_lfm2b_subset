import pandas as pd
import json
import numpy as np
from datetime import datetime

custom_date_parser = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

# '''
# filter data by metadata
# '''
# meta_lfm2b_uri_music4all_subset=pd.read_csv('./final_data/artist_lfm2b_uri_music4all_subset.csv')
# events = pd.read_csv('./music4all_onion/userid_trackid_count.tsv', delimiter='\t', header=0, usecols=[0,1])

# a = pd.unique(meta_lfm2b_uri_music4all_subset['id'])
# b = pd.unique(events['track_id'])
# c = np.intersect1d(a, b)
# print('meta_lfm2b_uri_music4all_subset id number : ', len(a))
# print('events uri number : ', len(b))
# print('subset number : ', len(c))
'''
get the id set
'''
essentia = pd.read_csv("./music4all_onion/id_essentia.tsv", delimiter='\t', header=0)
id_set_essentia = pd.unique(essentia["id"])
del essentia
blf_correlation = pd.read_csv("./music4all_onion/id_blf_correlation.tsv", delimiter='\t', header=0)
id_set_blf = pd.unique(blf_correlation["id"])
del blf_correlation
id_set = np.intersect1d(id_set_essentia, id_set_blf)
'''
filter data by date and micro genres tags
'''
start_date = datetime.strptime('2020-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
end_date = datetime.strptime('2020-03-19 23:59:59', "%Y-%m-%d %H:%M:%S")

# read data
# listening_events_path = "./music4all_onion/userid_trackid_timestamp.tsv"
listening_events_path = "./music4all_onion/listening_events_music4all_lfm2b_2023_filter.tsv"


# users = pd.read_csv(users_path, sep='\t')
# tracks = pd.read_csv(tracks_path, sep='\t')
header = ['user_id', 'track_id', 'timestamp']
listening_events = pd.read_csv(listening_events_path, sep='\t', header=0, parse_dates=['timestamp'],
                               date_parser=custom_date_parser,
                               dtype={'user_id': np.int32, 'track_id': 'str',
                                      'timestamp': 'str'}, chunksize=10000000)

for i,chunk in enumerate(listening_events):
    # chunk = chunk.loc[(chunk['timestamp'] >= start_date) & (chunk['timestamp'] <= end_date) & chunk['track_id'].isin(c)]
    chunk = chunk.loc[(chunk['timestamp'] >= start_date) & (chunk['timestamp'] <= end_date) & chunk['track_id'].isin(id_set)]
    chunk.to_csv("./music4all_onion/listening_events_music4all_lfm2b_2023_filter2.tsv",
                 sep='\t', header=header, mode='a', index=False)
    header = False
