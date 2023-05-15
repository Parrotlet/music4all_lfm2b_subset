import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

items_path = "./final_data/item_ids.csv"
music4all_ivec512_path = "./music4all_onion/id_ivec512.tsv"
music4all_lyric_tf_path = "./music4all_onion/id_lyrics_tf-idf.tsv"
music4all_essentia_path = "./music4all_onion/id_essentia.tsv"
music4all_chroma_path = "./music4all_onion/id_chroma_bow.tsv"
music4all_emobase_path = "./music4all_onion/id_emobase_bow.tsv"
music4all_blf_logfluc_path = "./music4all_onion/id_blf_logfluc.tsv"
music4all_blf_correlation_path = "./music4all_onion/id_blf_correlation.tsv"


def last_column_to_first(df):
    num_cols = len(df.columns)
    cols = [num_cols - 1] + list(range(num_cols - 1))
    df = df.iloc[:, cols]
    return df


def filter_feature(items_path, feature_name, feature_path, use_pca=True, pca_dim=256):
    items = pd.read_csv(items_path, sep=',', header=0)
    id_set = pd.unique(items['old_item_id'])
    items.set_index('old_item_id', inplace=True)
    music4all_feature = pd.read_csv(feature_path, delimiter='\t', header=0)
    music4all_feature = music4all_feature[music4all_feature['id'].isin(id_set)]
    music4all_feature.set_index('id', inplace=True)
    music4all_feature_id = [items.loc[i].iloc[0] for i, r in music4all_feature.iterrows()]
    music4all_feature['new_id'] = music4all_feature_id
    music4all_feature = last_column_to_first(music4all_feature)
    music4all_feature.sort_values(by='new_id', ascending=True, inplace=True)
    if use_pca:
        item_ids = music4all_feature.iloc[:, 0].values
        data = music4all_feature.iloc[:, 1:].values
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        pca = PCA(n_components=pca_dim)
        pca.fit(data_scaled)
        data_pca = pca.transform(data_scaled)
        data_final = np.concatenate((item_ids.reshape(-1, 1), data_pca), axis=1)
        df_pca = pd.DataFrame(data_final, columns=['item_id'] + [f'pca_{i}' for i in range(pca_dim)])
        df_pca.to_csv("./final_data/items_ids_" + feature_name + "_pca" + str(pca_dim) + ".csv", index=False)
    else:
        music4all_feature.to_csv("./final_data/items_ids_" + feature_name + "_filter.csv", index=False)
    return music4all_feature


def pd_to_pca(df, pca_dim, feature_name):
    item_ids = df.iloc[:, 0].values
    data = df.iloc[:, 1:].values
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    pca = PCA(n_components=pca_dim)
    pca.fit(data_scaled)
    data_pca = pca.transform(data_scaled)
    data_final = np.concatenate((item_ids.reshape(-1, 1), data_pca), axis=1)
    df_pca = pd.DataFrame(data_final, columns=['item_id'] + [f'pca_{i}' for i in range(pca_dim)])
    df_pca.to_csv("./final_data/items_ids_" + feature_name + "_pca" + str(pca_dim) + ".csv", index=False)


# music4all_essentia = filter_feature(items_path=items_path, feature_path=music4all_essentia_path,
#                                     feature_name="essentia",use_pca=False)
# #273,147
# rhythm_cols = music4all_essentia.filter(regex='rhythm|new_id')
# pd_to_pca(rhythm_cols, 256, 'rhythm')
# tonal_cols = music4all_essentia.filter(regex='tonal|new_id')
# pd_to_pca(tonal_cols, 128, 'tonal')
# #500,500,200
# music4all_chroma = filter_feature(items_path=items_path, feature_path=music4all_chroma_path,
#                                     feature_name="chroma",use_pca=True,pca_dim=256)
# music4all_emobase = filter_feature(items_path=items_path, feature_path=music4all_emobase_path,
#                                     feature_name="emobase",use_pca=True,pca_dim=256)
# music4all_ivec512 = filter_feature(items_path=items_path, feature_path=music4all_ivec512_path,
#                                     feature_name="ivec512",use_pca=True,pca_dim=128)
music4all_lyric = filter_feature(items_path=items_path, feature_path=music4all_lyric_tf_path,
                                    feature_name="lyrics_tf-idf",use_pca=True,pca_dim=256)
# music4all_blf_logfluc = filter_feature(items_path=items_path, feature_path=music4all_blf_logfluc_path,
#                                     feature_name="blf_logfluc",use_pca=True,pca_dim=256)
# music4all_blf_correlation = filter_feature(items_path=items_path, feature_path=music4all_blf_correlation_path,
#                                     feature_name="blf_correlation",use_pca=True,pca_dim=256)

