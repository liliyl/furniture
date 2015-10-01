
import numpy as np
import pandas as pd
import cPickle as pickle
from image_processing import get_domi_color_new_image
from scipy.spatial.distance import cosine, euclidean


def recommender(image, text, category, color=False):

    # Unpickling transformers and loading json:
    path = 'wayfair/pickle/' + category + '_pca_scaler.pkl'
    with open(path) as f:
        pca_scaler = pickle.load(f)

    path = 'wayfair/pickle/' + category + '_pca_model.pkl'
    with open(path) as f:
        pca_model = pickle.load(f)

    path = 'wayfair/pickle/' + category + '_tfidf.pkl'
    with open(path) as f:
        tfidf  = pickle.load(f)

    path = 'wayfair/' + category + '_vec_info.json'
    all_info_df = pd.read_json(path)


    # Dominant color
    domi_color = get_domi_color_new_image(image)
    # PCA
    image = skimage.color.rgb2gray(image)
    image = skimage.transform.resize(image, (150,150))
    features = np.array([image[irow][icol] for irow in range(150) for icol in range(150)])
    features_scaled = pca_scaler.transform(features)
    pca_feature = pca_model.transform(features_scaled)
    # tfidf
    tfidf_vec = tfidf.transform([text]).todense()

    # Calculating distances & get recommended items in final_df:
    color = False
    n_recomm_items = 9

    all_info_df['domi_distance'] = all_info_df['domi'].apply(lambda x:euclidean(domi_color, x))
    all_info_df['pca_distance'] = all_info_df['pca'].apply(lambda x:euclidean(pca_feature, x))
    all_info_df['text_distance'] = all_info_df['tfidf_vec'].apply(lambda x:cosine(tfidf_vec, x))

    domi_weight = 1
    if color:
        domi_weight = 10

    all_info_df['total_distance'] = all_info_df['domi_distance'] * domi_weight + all_info_df['pca_distance']/500 + all_info_df['text_distance']

    display_df = all_info_df[['path', 'product_id', 'title', 'price', 'url', 'rating_avg', 'rating_count', 'total_distance']]

    display_df.sort(columns='total_distance', axis=0, ascending=True, inplace=True)

    index = display_df.index
    final_df = pd.DataFrame(display_df.ix[index[0]]).T
    for i in index[1:]:
        if final_df.shape[0] < n_recomm_items and display_df.ix[i, 'product_id'] not in final_df['product_id'].values:
            product_df = pd.DataFrame(display_df.ix[i]).T
            final_df = pd.concat([final_df, product_df], axis=0)

    return final_df