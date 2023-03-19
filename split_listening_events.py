import pandas as pd
import json
import numpy as np
from datetime import datetime

custom_date_parser = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

'''
filter data by metadata
'''
meta_lfm2b_uri_music4all_subset=pd.read_csv('./final_data/meta_lfm2b_uri_music4all_subset.csv')
events = pd.read_csv('./music4all_onion/userid_trackid_count.tsv', delimiter='\t', header=0, usecols=[0,1])

a = pd.unique(meta_lfm2b_uri_music4all_subset['id'])
b = pd.unique(events['track_id'])
c = np.intersect1d(a, b)
print('meta_lfm2b_uri_music4all_subset id number : ', len(a))
print('events uri number : ', len(b))
print('subset number : ', len(c))

'''
filter data by date and micro genres tags
'''
start_date = datetime.strptime('2020-02-20 00:00:00', "%Y-%m-%d %H:%M:%S")
end_date = datetime.strptime('2020-03-19 23:59:59', "%Y-%m-%d %H:%M:%S")

# read data
listening_events_path = "./music4all_onion/userid_trackid_timestamp.tsv"


# users = pd.read_csv(users_path, sep='\t')
# tracks = pd.read_csv(tracks_path, sep='\t')
header = ['user_id', 'track_id', 'timestamp']
listening_events = pd.read_csv(listening_events_path, sep='\t', header=0, parse_dates=['timestamp'],
                               date_parser=custom_date_parser,
                               dtype={'user_id': np.int32, 'track_id': 'str',
                                      'timestamp': 'str'}, chunksize=10000000)

for i,chunk in enumerate(listening_events):
    chunk = chunk.loc[(chunk['timestamp'] >= start_date) & (chunk['timestamp'] <= end_date) & chunk['track_id'].isin(c)]
    chunk.to_csv("./listening_events_music4all_lfm2b_1mon_filter.tsv",
                 sep='\t',header=header, mode='a', index=False)
    header = False
