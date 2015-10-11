import numpy as np
import pandas as pd
import cPickle as pickle
import time
from pymongo import MongoClient
from collections import defaultdict
from scipy.spatial.distance import cosine, euclidean
from sklearn.feature_extraction.text import TfidfVectorizer
from helper import get_paths
from image_processing import get_domi_color, image_featurizer

def build_all_vec_info_json(category):
    '''
    For each image within the category, calculate the dominant color and the PCAed vector.
    For each item within the category, use tfidf to vectorize the description.
    Merge the info above, together with product info (title, price, URL etc.) to one dataframe,
        then save it to a json file.

    INPUT:
        category: string
    OUTPUT:
        None
    '''

    paths = get_paths(category)
    print len(paths)


    # Get dominant color:
    start_time =  time.time()
    domi_color_dict = get_domi_color(paths, category)
    time_1 =  time.time()
    print 'Time to run get_domi_color (s): ', time_1 - start_time


    # Get PCAed features and pickle transformers:
    feature_dict_pca, pca_scaler, pca_model = image_featurizer(category, pca=True)

    path = 'wayfair/pickle/' + category + '_pca_scaler.pkl'
    with open(path, 'w') as f:
        pickle.dump(pca_scaler, f)
    path = 'wayfair/pickle/' + category + '_pca_model.pkl'
    with open(path, 'w') as f:
        pickle.dump(pca_model, f)


    # Building dataframe from dictionaries:
    domi_pca_dict = defaultdict(dict)
    for i in domi_color_dict:
        domi_pca_dict[i]['domi'] = domi_color_dict[i]
    for i in feature_dict_pca:
        domi_pca_dict[i]['pca'] = feature_dict_pca[i]

    domi_pca_df = pd.DataFrame(domi_pca_dict).T
    domi_pca_df = domi_pca_df.reset_index()
    domi_pca_df.rename(columns={'index': 'path'}, inplace=True)
    domi_pca_df['product_id'] = domi_pca_df['path'].apply(lambda x:x.split('.')[0].split('_')[-2])

    client = MongoClient()
    db = client['furniture']
    collection = db[category]
    products_df = pd.DataFrame(list(collection.find()))

    products_df_small = products_df[['product_id', 'title', 'price', 'url', 'description_all', 'rating_avg', 'rating_count']]

    all_info_df = pd.merge(domi_pca_df, products_df_small, how='inner', left_on='product_id', 
                                right_on='product_id')


    # Train a tfidf vectorizer & pickle it:
    X = all_info_df['description_all']
    tfidf = TfidfVectorizer(strip_accents='unicode', stop_words='english', max_df=0.8, 
                            max_features=1000, ngram_range = (1,2))
    tfidf_matrix = tfidf.fit_transform(X).todense()

    path = 'wayfair/pickle/' + category + '_tfidf.pkl'
    with open(path, 'w') as f:
        pickle.dump(tfidf, f)


    # Add tfidf vectors to the dataframe:
    tfidf_matrix = np.array(tfidf_matrix)

    tfidf_dict = defaultdict(dict)
    for i in xrange(tfidf_matrix.shape[0]):
        index = X.index[i]
        tfidf_dict[index]['tfidf_vec'] = tfidf_matrix[i,:]

    tfidf_df = pd.DataFrame(tfidf_dict).T
    tfidf_df = tfidf_df.reset_index()
    tfidf_df.rename(columns={'index': 'ixx'}, inplace=True)

    all_info_df = pd.merge(all_info_df, tfidf_df, how='inner', left_index=True, right_on='ixx')
    all_info_df.drop('ixx', axis=1, inplace=True)


    # Some final clearning & save to json:
    all_info_df = all_info_df[all_info_df['domi'].notnull()]
    all_info_df = all_info_df[all_info_df['pca'].notnull()]
    all_info_df = all_info_df[all_info_df['description_all'].notnull()]

    path = 'wayfair/' + category + '_vec_info.json'
    all_info_df.to_json(path)


if __name__ == '__main__':
    categories = ['sofa', 'coffee_table', 'office', 'dining', 'bookcase', 'nightstand', 'bed', 'dresser']
    for category in categories:
        build_all_vec_info_json(category)
