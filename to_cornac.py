import pandas as pd
import numpy as np

cornac_data = pd.read_csv('lfm2b_1mon.inter', header=0,
                    dtype={'user_id:token': np.int32, 'item_id:token': np.int32, 'timestamp:float': np.int32}, sep='\t')
cornac_data.drop(columns=['timestamp:float'], inplace=True)

cornac_data.rename(columns={'user_id:token': 'userID', 'item_id:token': 'itemID'}, inplace=True)

cornac_data.insert(2,"rating", 5)

cornac_data.to_csv(
    './cornac_lfm2b_1mon_full', index=False)