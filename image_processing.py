
import numpy as np
from numpy.linalg import svd
from sklearn.cluster import KMeans

import skimage
from skimage import io
from skimage import transform, feature

from pyimage.pipeline import ImagePipeline



def get_domi_color(paths):
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
        category = '_'.join(path.split('_')[0:-2])
        image = skimage.io.imread('image_test/' + category + '/' + path)
        
        # If the picture is grayscale, discard it for now. Think about how to improve it later.
        
        if len(image.shape) == 2:
            print 'gray'
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
            if np.mean(color > white_color_arr) == 1:
                flag = True
            else:
                domi_color = color

        if not flag:    
            new_path = 'image_test_result/background/' + path
            skimage.io.imsave(new_path, image)
            domi_color_dict[path] = False 
        else:
            new_path = 'image_test_result/white/' + path
            skimage.io.imsave(new_path, image)
            domi_color_dict[path] = domi_color 
        
    return domi_color_dict


def vectorize_color_distribution(paths):
    
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
        #category = '_'.join(path.split('_')[0:-2])
        
        image = skimage.io.imread('image_test_result/' + 'white' + '/' + path)
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




def clustering_with_color(color_dict, category, n_clusters=6, save_image=True, domi_color=True):
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
            image = skimage.io.imread('image_test/' + category + '/' + path)
            if domi_color:
            	new_path = 'image_test_result/' + str(label) + '/' + path
            else:
            	new_path = 'image_test_result/color_dist/' + str(label) + '/' + path
            skimage.io.imsave(new_path, image)
    
    return cluster_label_dict, color_centroids



# def clustering_with_color_dist(color_dist_dict, category, n_clusters=6):
#     '''
#     INPUT: color_dist_dict:
#             * key: path
#             * value: color distribution vector
    
#     Cluster by color & save files to different folders according to labels.
    
#     OUTPUT: cluster_label_dict
#             * key: path
#             * value: cluster label
#             color_dist_centroids:
#             * index: label 
#             * value: centroid
#     '''
#     color_dist_values = color_dist_dict.values()
    
#     color_dist_reverse_dict = {}
#     for i, j in color_dist_dict.iteritems():
#         color_dist_reverse_dict[tuple(j)] = i 
        
#     km_color = KMeans(n_clusters=n_clusters)
#     color_dist_labels =km_color.fit_predict(color_dist_values)
    
#     color_dist_centroids = km_color.cluster_centers_
             
#     cluster_label_dict = {}
#     for i, j in enumerate(color_dist_values):
#         label = color_dist_labels[i]
#         path = color_dist_reverse_dict[tuple(j)]
#         cluster_label_dict[path] = label
        
#         image = skimage.io.imread('image_test/' + category + '/' + path)
#         new_path = 'image_test_result/color_dist/' + str(label) + '/' + path
#         skimage.io.imsave(new_path, image)
    
#     return cluster_label_dict, color_centroids


def image_featurizer(base_path, sub_dir, edge=False, svd=False):

    '''
    Taking image file path info and using ImagePipeline to vectorize images within the folder.

    INPUT:
        base_path: string
        sub_dir: string
        edge: boolean
        svd: boolean

    OUTPUT:
        feature_dict: dictionary
            key: path (filename)
            value: vectorized image
    '''

    image_pipe = ImagePipeline(base_path)
    image_pipe.read(sub_dirs=(sub_dir,))

    image_pipe.resize((150,150,3))
    image_pipe.transform(skimage.color.rgb2gray, {})
    if edge:
        image_pipe.transform(skimage.feature.canny, {})

    image_pipe.vectorize()
    features = image_pipe.features

    if svd:
    	U, sigma, VT = svd(features)
    	if edge:
    		features = U[:,:100]
    	else:
    		features = U[:,:20]

    paths = os.listdir(base_path + sub_dir)
    paths = [x for x in paths if x[0] != '.']

    feature_dict = {}
    for i in xrange(len(paths)):
        path = paths[i]
        feature = features[i]
        feature_dict[path] = feature

    return feature_dict


def clustering_with_feature(feature_dict, n_clusters=6, svd=False, save_image=True, edge=False):
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
            image = skimage.io.imread('image_test_result/same_angle/' + path)
            if svd:
                new_path = 'image_test_result/features_svd/' + str(label) + '/' + path
            elif edge:
                new_path = 'image_test_result/features_edge/' + str(label) + '/' + path
            else:
                new_path = 'image_test_result/features/' + str(label) + '/' + path
            skimage.io.imsave(new_path, image)
    
    return cluster_label_dict, feature_centroids



# ----------------------------------------------------------------------------
# Might be useless from here: 
# ----------------------------------------------------------------------------

def show_domi_color(image, n_clusters=3):
    nrow, ncol, depth = image.shape 
    lst_of_pixels = [image[irow][icol] for irow in range(nrow) for icol in range(ncol)]
    kmean = KMeans(n_clusters=n_clusters)
    kmean.fit_transform(lst_of_pixels)
    domi_colors = kmean.cluster_centers_ 
    domi_colors = domi_colors.reshape((1,n_clusters,3))
    skimage.io.imshow(domi_colors)
    return domi_colors