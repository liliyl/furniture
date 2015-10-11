import numpy as np
import os.path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import skimage
from skimage import transform
from pyimage.pipeline import ImagePipeline

# ----------------------------------------------------------------------------
# Main image processing functions: 
# ----------------------------------------------------------------------------

def get_domi_color(paths, category):
    '''
    For all images in paths, select those with a white background, 
    save them to the 'white' folder and get the dominant color 
    for the furniture in each image.
    For the rest images (without a white background), save them 
    into the 'non-white' folder.

    INPUT:
        paths: list of strings
            paths of image files
        category: string
    OUTPUT:
        domi_color_dict: dictionary
            key: path 
            value: dominant color of the image.
    '''

    domi_color_dict = {}
    grayscale = 0

    for path in paths:
        image = skimage.io.imread('wayfair/images/' + category + '/' + path)
        
        # Check if the picture is grayscale:
        if len(image.shape) == 2:
            grayscale += 1
            continue
            
        image = transform.resize(image, (300,300,3))

        # Flatten the image matrix:
        nrow, ncol, depth = image.shape 
        lst_of_pixels = [image[irow][icol] for irow in range(nrow) for icol in range(ncol)]

        # Clustering the colors of each pixel:
        kmean1 = KMeans(n_clusters=2)
        kmean1.fit_transform(lst_of_pixels)
        domi_colors_all = kmean1.cluster_centers_

        # Select images with a white background:
            # If one of the two dominant color is perfectly white, 
            # then the image has a clean white background and flag=True.
        white_color_arr = np.array([0.98, 0.98, 0.98])
        flag = False
        for color in domi_colors_all:
            if flag:
                domi_color = color
            elif np.mean(color > white_color_arr) == 1:
                flag = True
            else:
                domi_color = color

        # Save images to different folders depend on their backgrounds:
        if not flag:    
            new_path = 'wayfair/images/' + category + '/non-white/' + path
            skimage.io.imsave(new_path, image)
        else:
            new_path = 'wayfair/images/' + category + '/white/' + path
            skimage.io.imsave(new_path, image)
            domi_color_dict[path] = domi_color 

    print '# of grayscaled photos: ', grayscale
    return domi_color_dict


def image_featurizer(category, sub_dir='white', edge=False, pca=True):
    '''
    Vectorize images (with white backgrounds) within the category.

    INPUT:
        category: string
        sub_dir: string
        edge: boolean
        pca: boolean

    OUTPUT:
        feature_dict: dictionary
            key: path (filename)
            value: vectorized image
        scaler: trained StandardScaler
        pca_model: trained PCA model
    '''

    # Use ImagePipeline to read and transform the images:
    base_path = 'wayfair/images/' + category + '/'
    image_pipe = ImagePipeline(base_path)
    image_pipe.read(sub_dirs=(sub_dir,))

    image_pipe.resize((150,150,3))
    image_pipe.transform(skimage.color.rgb2gray, {})
    if edge:
        image_pipe.transform(skimage.feature.canny, {})

    image_pipe.vectorize()
    features = image_pipe.features

    # Do PCA if pca is passed in as true:
    if pca:
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        pca_model = PCA(n_components=100)
        pca_data = pca_model.fit_transform(features_scaled)
        features = pca_data

    # Organize vectorized images into the dictionary (feature_dict):
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
    '''
    INPUT:
        image: numpy array
        n_clusters: integer

    OUTPUT:
        domi_color: numpy array
    '''
    
    if len(image.shape) == 3:
        image = transform.resize(image, (300,300,3))
    else:
        return -1

    # Flatten the image matrix:
    nrow, ncol, depth = image.shape 
    lst_of_pixels = [image[irow][icol] for irow in range(nrow) for icol in range(ncol)]

    # Clustering the colors of each pixel:
    kmean = KMeans(n_clusters=n_clusters)
    kmean.fit_transform(lst_of_pixels)
    domi_colors = kmean.cluster_centers_

    # Get the dominant color of the furniture (darker than the background):
    if np.mean(domi_colors[0]) < np.mean(domi_colors[1]):
        domi_color = domi_colors[0]
    else:
        domi_color = domi_colors[1]
    return domi_color


# ----------------------------------------------------------------------------
# For trying out color distribution vectorizaiton: 
# ----------------------------------------------------------------------------

def vectorize_color_distribution(paths, category):
    '''
    INPUT:
        paths: list of strings
            paths of image files
        category: string
    OUTPUT:
        color_dist_dict: dictionary 
            key: path 
            value: vectorized color distribution (a 1*30 numpy array representing
                     RBG intensities, 10 numbers for each color)
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
# For testing/visualizing vectorizing results by clustering: 
# ----------------------------------------------------------------------------

def clustering_with_color(color_dict, category, n_clusters=10, save_image=True, domi_color=True):
    '''
    Cluster by colors & save files to different folders according to labels.

    INPUT: 
        color_dict: dictionary
            key: path
            value: dominant color or color distribution vector
        category: string
        n_clusters: integer
        save_image: boolean
        domi_color: boolean
      
    OUTPUT: 
        cluster_label_dict: dictionary
            key: path
            value: cluster label
        color_centroids: list
            index: label 
            value: centroid
        km_color: trained KMeans model
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


def clustering_with_feature(feature_dict, category, n_clusters=10, save_image=True, pca=False, edge=False):
    '''
    Cluster by features & save files to different folders according to labels.

    INPUT: 
        feature_dict: dictionary
            key: path
            value: features
        category: string
        n_clusters: integer
        save_image: boolean
        pca: boolean
        edge: boolean

    OUTPUT: 
        cluster_label_dict: dictionary
            key: path
            value: cluster label
        feature_centroids: list
            index: label 
            value: centroid
        km_feature: trained KMeans model
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

