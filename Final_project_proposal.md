Lili Yao (SF Cohort 8)  Sept.7th


## Final Proposal: Furniture seeker
### High level description:
There are a lot of times when people find a new piece of furniture online which they really like, and matches their home styles, but unfortunately out of their budget (beautiful furnitures can be really expensive!). At these times, a seeker/recommender with similar but more budget-friendly furnitures will come in handy. Thus in this project I aim to build such a recommender, using input from the user - photos & descriptions from a weblink, then searching data from budget-friendly furniture websites like Wayfair, Ikea, Amazon etc., and presenting similar items to the user.


### Web app/visualization:
User inputs a weblink of a furniture for sale online, then a recommended list of similar but more budget-friendly furnitures appears, with photos, prices and links for purchasing.


### Pros:
* Obvious business/customer value.
* Seems difficult (to me who haven't learned/done any neuron network for imaging processing), but should be doable since similar image processing/neural network projects has been done previously.


### Cons (Potential problems & how to overcome):
* Unsupervised machine learning which means difficult to cross-validate: Need to think about reasonable metrics to do some kind of validation.
* The colors will be easy to match, but the textures/design styles will be subtle and might be difficult for the algorithm to pick up: Look into deep-learning neural network algorithms to see if this can be done in the allotted time frame. Or try to extract the info from NLP.
* Need web-scraping to get the data set: Start to write and try web-scrapers early!
   

### Important features I can think of so far:
* item pictures
* item title
* item description
* item specs if available


### Data Pipeline:
For images:


* Collect -> Store -> Featurize -> Design neural network architecture -> Train neural network with featurized images

For title/description (natural language):


* Collect -> Store -> Featurize -> TFIDF -> Cluster/Similarity calculation


### Scoping: 
* Get 5000-50000 pieces of furnitures info in the database (images, title, description, price etc.)
* Start from ~10 categories of furnitures (e.g. sofa, coffee table, dining table, dressers, shelves, office desk, chair)


### Algorithms to use:
* NLP
* Clustering
* Neuron network for imaging processing


### Sources (Python libraries to be used):
* BeautifulSoup
* urllib
* numpy
* pandas
* matplotlib
* nltk
* sklearn
* Theano/Lasagne


### Data sources:
The dataset is not ready currently. It will be obtained from scraping the following website: 

* [Wayfair.com](http://www.wayfair.com/)
* [Overstock.com](http://www.overstock.com/)
* [Ikea.com](http://www.ikea.com/us/en/)
* [Amazon.com](http://www.amazon.com/furniture-decor-rugs-lamps-beds-tv-stands/b/ref=sd_allcat_fd?ie=UTF8&node=1057794)    


### Next steps:
* Learn about neuron network for imaging processing
* Write web scrapers & start scraping.