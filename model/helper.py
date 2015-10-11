import os.path

def get_paths(category, image=True, white=False):
    '''
    INPUT:
        category: string
        image: boolean
        white: boolean
    OUTPUT:
        paths: list of strings
            paths of image files
    '''

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