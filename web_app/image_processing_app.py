import numpy as np
from skimage import transform
from sklearn.cluster import KMeans

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

    # Get the non-white dominant color:
    white_color_arr = np.array([0.90, 0.90, 0.90])
    domi_color = None
    if np.mean(domi_colors[0] > white_color_arr) != 1:
        domi_color = domi_colors[0]
    else:
        domi_color = domi_colors[1]
        
    return domi_color
