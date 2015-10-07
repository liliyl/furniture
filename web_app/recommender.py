
import numpy as np
import pandas as pd
import cPickle as pickle
import skimage
from skimage import transform
from image_processing_app import get_domi_color_new_image
from scipy.spatial.distance import cosine, euclidean


def recommender(image, text, category, pca_scaler_dict, pca_model_dict, tfidf_dict, 
    all_info_df_dict, n_recomm_items=8, color=False, price_limit=None):
    '''
    Vectorize the image and/or text input, find the most similar items in the database,
    and return the information of those items in a dataframe.

    INPUT:
        image: numpy array
        text: string
        category: string
        pca_scaler_dict: dictionary
        pca_model_dict: dictionary
        tfidf_dict: dictionary
        all_info_df_dict: dictionary
        n_recomm_items: integer
        color: boolean
        price_limit: integer
    OUTPUT:
        final_df: pandas dataframe
    '''

    pca_scaler = pca_scaler_dict[category]
    pca_model = pca_model_dict[category]
    tfidf = tfidf_dict[category]
    all_info_df = all_info_df_dict[category]

    if image is not None:
        # Get dominant color:
        domi_color = get_domi_color_new_image(image)
        # Do PCA:
        image = skimage.color.rgb2gray(image)
        image = transform.resize(image, (150,150))
        features = np.array([image[irow][icol] for irow in range(150) for icol in range(150)])
        features_scaled = pca_scaler.transform(features)
        pca_feature = pca_model.transform(features_scaled)
        # Calculate image distances:
        all_info_df['domi_distance'] = all_info_df['domi'].apply(lambda x:euclidean(domi_color, x))
        all_info_df['pca_distance'] = all_info_df['pca'].apply(lambda x:euclidean(pca_feature, x))
    else:
        all_info_df['domi_distance'] = 0
        all_info_df['pca_distance'] = 0

    if len(text) != 0:
        # Tf-idf transform:
        tfidf_vec = tfidf.transform([text]).todense()
        # Calculate text distance:
        all_info_df['text_distance'] = all_info_df['tfidf_vec'].apply(lambda x:cosine(tfidf_vec, x))
    else:
        all_info_df['text_distance'] = 0

    domi_weight = 2
    if color:
        domi_weight = 10

    # Calculate total distance:
    all_info_df['total_distance'] = all_info_df['domi_distance'] * domi_weight + all_info_df['pca_distance']/500 + all_info_df['text_distance']

    display_df = all_info_df[['path', 'product_id', 'title', 'price', 'url', 'total_distance']]
    display_df.sort(columns='total_distance', axis=0, ascending=True, inplace=True)

    # Get recommended items in final_df:
    index = display_df.index
    flag = True
    final_df = pd.DataFrame({'product_id': {0: 0}})
    for i in index:
    	if price_limit is None:
            if final_df.shape[0] < n_recomm_items and display_df.ix[i, 'product_id'] not in final_df['product_id'].values:
                product_df = pd.DataFrame(display_df.ix[i]).T
                if flag:
                    final_df = product_df
                    flag = False
                else:
                    final_df = pd.concat([final_df, product_df], axis=0)
        else:
            if final_df.shape[0] < n_recomm_items and display_df.ix[i, 'price'] < price_limit and display_df.ix[i, 'product_id'] not in final_df['product_id'].values:
                product_df = pd.DataFrame(display_df.ix[i]).T
                if flag:
                    final_df = product_df
                    flag = False
                else:
                    final_df = pd.concat([final_df, product_df], axis=0)
    
    if final_df.shape[0] > 1:
        final_df.sort(columns='price', axis=0, ascending=True, inplace=True)
        final_df['price'] = final_df['price'].apply(lambda x:str(x))
        return final_df
    else:
        return None
