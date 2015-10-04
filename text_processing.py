import numpy as np
import pandas as pd
import re
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords 
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from image_processing import get_paths


def clean_text_data(df, sofa=False):
    df['product_id'] = df['product_id'].apply(lambda x: x.strip())
    df['price'] = df['price'].apply(lambda x:float(x.strip('$').replace(',','').split()[0]))
    df['features'] = df['features'].apply(lambda x: '\n'.join(x) if type(x)==list else x)
    df['description'] = df['description'].apply(lambda x: '\n'.join(x) if type(x)==list else x)
    df['description'][df['description'].isnull()] = ''
    df['description_all'] = df['description'] + '\n' + df['features']
    if sofa:
        df = df.set_index('product_id')
    return df 


def my_tokenizer(doc):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenize and stem/lemmatize the document.
    '''   
    
    token = re.findall(r'\w+', doc.lower())
    
    sw = set(stopwords.words('english'))
    token_stop = [word for word in token if word not in sw]
    
    snowball = SnowballStemmer('english')
    sbs_ar = [snowball.stem(word) for word in token_stop]
    return sbs_ar 


def get_top_words_for_each_cluster(km_model, tfidf):
	cluster_top_words = []
    centroids = km_model.cluster_centers_
    centroid_top_10_index = [np.argsort(centroids, axis=1)[i][::-1][0:10] for i in xrange(centroids.shape[0])]
    feature_names = np.array(tfidf.get_feature_names())
    for i in range(len(centroid_top_10_index)):
        cluster_top_words.append(feature_names[centroid_top_10_index[i])
    return cluster_top_words


def visualize_text_clustering_result(km_model):
	text_clustering_result = collections.defaultdict(list)
    for i, label in enumerate(km_model.labels_):
        text_clustering_result[label].append(int(X.index[i]))

    paths = get_paths(category)
    for i in text_clustering_result:
        for j in text_clustering_result[i]:
            product_id = sofa_df.ix[j].product_id
            for path in paths:
                if product_id in path:
                    image = skimage.io.imread('wayfair/images/' + category + '/' + path)
                    new_path = 'wayfair/images/' + category + '/text_clustering/' + str(i) + '/' + path
                    skimage.io.imsave(new_path, image)


if __name__ == '__main__':
    categories = ['sofa', 'coffee_table', 'office', 'dining', 'bookcase', 'nightstand', 'bed', 'dresser']
    for category in categories:
        path = 'wayfair/' + category + '.json'
        df = pd.read_json(path)
        df = clean_text_data(df)
        df.to_json(path)

        X = df['description_all'][df['description_all'].notnull()]

        tfidf = TfidfVectorizer(strip_accents='unicode', stop_words='english', max_df=0.8, 
                        max_features=5000, ngram_range = (1,2))
        tfidf_matrix = tfidf.fit_transform(X).todense()

        tfidf2 = TfidfVectorizer(tokenizer=my_tokenizer, max_features=1000, max_df=0.8, ngram_range = (1,2))
        tfidf_matrix2 = tfidf2.fit_transform(X).todense()

        km_model = KMeans(n_clusters=10)
        km_model.fit(tfidf_matrix)
        cluster_top_words = get_top_words_for_each_cluster(km_model, tfidf)
        visualize_text_clustering_result(km_model)

        km_model2 = KMeans(n_clusters=10)
        km_model2.fit(tfidf_matrix2)
        cluster_top_words2 = get_top_words_for_each_cluster(km_model2, tfidf2)
        visualize_text_clustering_result(km_model2)
