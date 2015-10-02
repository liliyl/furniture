
import numpy as np
import pandas as pd
import cPickle as pickle
import skimage
from skimage import transform
from image_processing_app import get_domi_color_new_image
from scipy.spatial.distance import cosine, euclidean


def recommender(image, text, category, n_recomm_items=8, color=False, price_limit=None):

    # Unpickling transformers and loading json:
    path = 'static/pickle/' + category + '_pca_scaler.pkl'
    with open(path) as f:
        pca_scaler = pickle.load(f)

    path = 'static/pickle/' + category + '_pca_model.pkl'
    with open(path) as f:
        pca_model = pickle.load(f)

    path = 'static/pickle/' + category + '_tfidf.pkl'
    with open(path) as f:
        tfidf  = pickle.load(f)

    path = 'static/json/' + category + '_vec_info.json'
    all_info_df = pd.read_json(path)


    # Dominant color
    domi_color = get_domi_color_new_image(image)
    # PCA
    image = skimage.color.rgb2gray(image)
    image = transform.resize(image, (150,150))
    features = np.array([image[irow][icol] for irow in range(150) for icol in range(150)])
    features_scaled = pca_scaler.transform(features)
    pca_feature = pca_model.transform(features_scaled)
    # tfidf
    tfidf_vec = tfidf.transform([text]).todense()

    # Calculating distances & get recommended items in final_df:
    all_info_df['domi_distance'] = all_info_df['domi'].apply(lambda x:euclidean(domi_color, x))
    all_info_df['pca_distance'] = all_info_df['pca'].apply(lambda x:euclidean(pca_feature, x))
    all_info_df['text_distance'] = all_info_df['tfidf_vec'].apply(lambda x:cosine(tfidf_vec, x))

    domi_weight = 1
    if color:
        domi_weight = 10

    all_info_df['total_distance'] = all_info_df['domi_distance'] * domi_weight + all_info_df['pca_distance']/500 + all_info_df['text_distance']

    #display_df = all_info_df[['path', 'product_id', 'title', 'price', 'url', 'rating_avg', 'rating_count', 'total_distance']]
    display_df = all_info_df[['path', 'product_id', 'title', 'price', 'url', 'total_distance']]

    display_df.sort(columns='total_distance', axis=0, ascending=True, inplace=True)

    index = display_df.index
    final_df = pd.DataFrame(display_df.ix[index[0]]).T
    for i in index[1:]:
    	if price_limit is None:
            if final_df.shape[0] < n_recomm_items and display_df.ix[i, 'product_id'] not in final_df['product_id'].values:
                product_df = pd.DataFrame(display_df.ix[i]).T
                final_df = pd.concat([final_df, product_df], axis=0)
        else:
            if final_df.shape[0] < n_recomm_items and display_df.ix[i, 'price'] < price_limit and display_df.ix[i, 'product_id'] not in final_df['product_id'].values:
                product_df = pd.DataFrame(display_df.ix[i]).T
                final_df = pd.concat([final_df, product_df], axis=0)

    final_df.sort(columns='price', axis=0, ascending=True, inplace=True)
    final_df['price'] = final_df['price'].apply(lambda x:str(x))

    return final_df