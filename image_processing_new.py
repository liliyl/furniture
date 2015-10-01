
import numpy as np
import os.path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import skimage
from skimage import transform

from pyimage.pipeline import ImagePipeline



def get_paths(category, image=True, white=False):
    base_path = 'wayfair/images/' 
    if white:
        paths = os.listdir(base_path + category + '/white')
    else:
        paths = os.listdir(base_path + category)

    if image:
        paths = [x for x in paths if x[-3:] == 'jpg']
    else:
        paths = [x for x in paths if x[0] != '.']

    return paths



def get_domi_color(paths, category):
    '''
    For all files in paths, tease out photos without a clear white background 
    and save those into the 'background' folder.
    For those with white background, save them to the 'white' folder.
    Then get the dominant furniture color for images with white background.

    INPUT:
        paths: list
            paths of image files

    OUTPUT:
        domi_color_dict: dictionary
            key: path 
            value: dominant color (just one) if the image has a white background.
                   'False' if the image doesn't have a white background.
    '''

    domi_color_dict = {}
    
    for path in paths:
        #category = '_'.join(path.split('_')[0:-2])
        image = skimage.io.imread('wayfair/images/' + category + '/' + path)
        
        # If the picture is grayscale, discard it for now. Think about how to improve it later.
        
        gray = 0
        if len(image.shape) == 2:
            gray += 1
            # print 'gray'
            continue
            
        image = transform.resize(image, (300,300,3))

        nrow, ncol, depth = image.shape 
        lst_of_pixels = [image[irow][icol] for irow in range(nrow) for icol in range(ncol)]

        kmean1 = KMeans(n_clusters=2)
        kmean1.fit_transform(lst_of_pixels)
        domi_colors_all = kmean1.cluster_centers_ 
        white_color_arr = np.array([0.98, 0.98, 0.98])

        """Remove photos without clean white background:
            If one of the two dominant color is perfectly white, 
            then the photo has a clean white background and flag=True."""
        
        flag = False
        for color in domi_colors_all:
            if flag:
                domi_color = color
            elif np.mean(color > white_color_arr) == 1:
                flag = True
            else:
                domi_color = color

        if not flag:    
            new_path = 'wayfair/images/' + category + '/background/' + path
            skimage.io.imsave(new_path, image)
        else:
            new_path = 'wayfair/images/' + category + '/white/' + path
            skimage.io.imsave(new_path, image)
            domi_color_dict[path] = domi_color 

    print '# of grayscaled photos: ', gray
        
    return domi_color_dict



def image_featurizer(category, sub_dir='white', edge=False, pca=True):

    '''
    Taking image file path info and using ImagePipeline to vectorize images within the folder.

    INPUT:
        sub_dir: string
        edge: boolean
        pca: boolean

    OUTPUT:
        feature_dict: dictionary
            key: path (filename)
            value: vectorized image
    '''
    base_path = 'wayfair/images/' + category + '/'
    image_pipe = ImagePipeline(base_path)
    image_pipe.read(sub_dirs=(sub_dir,))

    image_pipe.resize((150,150,3))
    image_pipe.transform(skimage.color.rgb2gray, {})
    if edge:
        image_pipe.transform(skimage.feature.canny, {})

    image_pipe.vectorize()
    features = image_pipe.features

    if pca:
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        pca_model = PCA(n_components=100)
        pca_data = pca_model.fit_transform(features_scaled)
        features = pca_data


    paths = os.listdir(base_path + sub_dir)
    paths = [x for x in paths if x[0] != '.']

    feature_dict = {}
    for i in xrange(len(paths)):
        path = paths[i]
        feature = features[i]
        feature_dict[path] = feature

    if pca:
        return feature_dict, scaler, pca_model
    else:
        return feature_dict
        


# ----------------------------------------------------------------------------
# For new images: 
# ----------------------------------------------------------------------------

def get_domi_color_new_image(image, n_clusters=2):
    
    if len(image.shape) == 3:
        image = transform.resize(image, (300,300,3))
    else:
        return -1

    nrow, ncol, depth = image.shape 
    lst_of_pixels = [image[irow][icol] for irow in range(nrow) for icol in range(ncol)]
    kmean = KMeans(n_clusters=n_clusters)
    kmean.fit_transform(lst_of_pixels)
    domi_colors_all = kmean.cluster_centers_ 
    white_color_arr = np.array([0.95, 0.95, 0.95])

    domi_color = None
    for color in domi_colors_all:
        if np.mean(color > white_color_arr) != 1:
            domi_color = color
    return domi_color



# ----------------------------------------------------------------------------
# For trying out color distribution vectorizaiton: 
# ----------------------------------------------------------------------------

def vectorize_color_distribution(paths, category):
    
    '''INPUT:
            paths: list of strings
                file paths
       OUTPUT:
            color_dist_dict: dictionary 
                key: path 
                value: vectorized color distribution (a 1D numpy array of 30 numbers representing RBG 
                                                        intensities, 10 numbers for each color)
    '''
    
    color_dist_dict = {}
    
    for path in paths:
        
        image = skimage.io.imread('wayfair/images/' + category + '/' + path)
        image = transform.resize(image, (300,300,3))
    
        nrow, ncol, depth = image.shape 
        white_pixel = np.array([ .99, .99, .99])
        lst_of_pixels = np.array([image[irow][icol] for irow in range(nrow) for icol in range(ncol) if np.mean(image[irow][icol]>white_pixel) != 1])

        red_values = lst_of_pixels[:,0]
        green_values = lst_of_pixels[:,1]
        blue_values = lst_of_pixels[:,2]

        (n_red, bins) = np.histogram(red_values, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        (n_green, bins) = np.histogram(green_values, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        (n_blue, bins) = np.histogram(blue_values, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        
        num_of_pixels = float(len(lst_of_pixels))
        n_red = n_red / num_of_pixels
        n_green = n_green / num_of_pixels
        n_blue = n_blue / num_of_pixels

        color_dist_vector = np.hstack((n_red, n_green, n_blue))
        color_dist_dict[path] = color_dist_vector
        
    return color_dist_dict



# ----------------------------------------------------------------------------
# For testing vectorizing results by clustering: 
# ----------------------------------------------------------------------------

def clustering_with_color(color_dict, category, n_clusters=10, save_image=True, domi_color=True):
    '''
    Cluster by color & save files to different folders according to labels.

    INPUT: 
        color_dict: dictionary
            * key: path
            * value: dominant color (just one) or color distribution vector
      
    OUTPUT: 
        cluster_label_dict: dictionary
            * key: path
            * value: cluster label
        color_centroids: list
            * index: label 
            * value: centroid
    '''

    color_values = color_dict.values()
    
    color_reverse_dict = {}
    for i, j in color_dict.iteritems():
        color_reverse_dict[tuple(j)] = i 
        
    km_color = KMeans(n_clusters=n_clusters)
    colors_labels =km_color.fit_predict(color_values)
    
    color_centroids = km_color.cluster_centers_
             
    cluster_label_dict = {}
    for i, j in enumerate(color_values):
        label = colors_labels[i]
        path = color_reverse_dict[tuple(j)]
        cluster_label_dict[path] = label
        
        if save_image:
            image = skimage.io.imread('wayfair/images/' + category + '/' + path)
            if domi_color:
                new_path = 'wayfair/images/' + category + '/domi_color/' + str(label) + '/' + path
            else:
                new_path = 'wayfair/images/' + category + '/color_dist/' + str(label) + '/' + path
            skimage.io.imsave(new_path, image)
    
    return cluster_label_dict, color_centroids, km_color



def clustering_with_feature(feature_dict, category, n_clusters=10, pca=False, save_image=True, edge=False):
    '''
    Cluster by features & save files to different folders according to labels.

    INPUT: 
        feature_dict: dictionary
            * key: path
            * value: features

    OUTPUT: 
        cluster_label_dict: dictionary
            * key: path
            * value: cluster label
        feature_centroids: list
            * index: label 
            * value: centroid
    '''

    feature_values = feature_dict.values()
    
    feature_reverse_dict = {}
    for i, j in feature_dict.iteritems():
        feature_reverse_dict[tuple(j)] = i 
        
    km_feature = KMeans(n_clusters=n_clusters)
    feature_labels = km_feature.fit_predict(feature_values)
    
    feature_centroids = km_feature.cluster_centers_
             
    cluster_label_dict = {}
    for i, j in enumerate(feature_values):
        label = feature_labels[i]
        path = feature_reverse_dict[tuple(j)]
        cluster_label_dict[path] = label
        
        if save_image:
            image = skimage.io.imread('wayfair/images/' + category + '/' + path)
            if pca:
                new_path = 'wayfair/images/' + category + '/features_pca/' + str(label) + '/' + path
            elif edge:
                new_path = 'wayfair/images/' + category + '/features_edge/' + str(label) + '/' + path
            else:
                new_path = 'wayfair/images/' + category + '/features/' + str(label) + '/' + path
            skimage.io.imsave(new_path, image)
    
    return cluster_label_dict, feature_centroids, km_feature


