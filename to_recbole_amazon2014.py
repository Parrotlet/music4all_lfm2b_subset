import pandas as pd
import numpy as np
from datetime import datetime

custom_date_parser = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")


train = pd.read_csv('./amazon2014/listening_history_train.csv', header=0,
                    dtype={'user': 'str', 'item': 'str', 'timestamp': np.int64,
                           'user_id': np.int32, 'item_id': np.int32})
val = pd.read_csv('./amazon2014/listening_history_val.csv', header=0,
                  dtype={'user': 'str', 'item': 'str', 'timestamp': np.int64,
                         'user_id': np.int32, 'item_id': np.int32})
test = pd.read_csv('./amazon2014/listening_history_test.csv', header=0,
                   dtype={'user': 'str', 'item': 'str', 'timestamp': np.int64,
                          'user_id': np.int32, 'item_id': np.int32})
inter = pd.concat([train, val, test])
inter = inter.drop(columns=['user', 'item'])
inter = inter[['user_id', 'item_id', 'timestamp']]
inter.rename(columns={'user_id': 'user_id:token', 'item_id': 'item_id:token', 'timestamp': 'timestamp:float'},
             inplace=True)
# inter['timestamp:float'] = pd.to_datetime(inter['timestamp:float']).map(pd.Timestamp.timestamp)
# inter['timestamp:float'] = inter['timestamp:float'].astype('int64')

user = pd.read_csv('./amazon2014/user_ids.csv', header=0,
                    dtype={'user_id': np.int32, 'user': 'str'})
user = user.drop(columns=['user'])
user.rename(columns={'user_id': 'user_id:token'}, inplace=True)

item = pd.read_csv('./amazon2014/item_ids.csv', header=0,
                    dtype={'item_id': np.int32, 'item': 'str'})
item = item.drop(columns=['item'])
item.rename(columns={'item_id': 'item_id:token'}, inplace=True)

inter.to_csv(
    './amazon2014/amazon2014.inter', index=False,
    sep='\t')
user.to_csv(
    './amazon2014/amazon2014.user', index=False,
    sep='\t')
item.to_csv(
    './amazon2014/amazon2014.item', index=False,
    sep='\t')