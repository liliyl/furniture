import pandas as pd
import cPickle as pickle
import skimage
from skimage.io import imread
from recommender import recommender
from flask import Flask, render_template, request
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sofa_input')
def sofa_input():
    return render_template('input.html', cat='Sofa', msg='', form_action="/sofa_seeker#portfolio")

@app.route('/sofa_seeker', methods=['POST'])
def sofa_seeker():
    image_url = str(request.form['image_url'])
    description = str(unicode(request.form['description']).encode('ascii', 'ignore'))
    
    if len(image_url) > 0:
        try:
            image = imread(image_url)
        except IOError:
            return render_template('input.html', cat='sofa', msg='Oops! That was not a image url. ', form_action="/sofa_seeker#portfolio")
    else:
        image = None

    if len(description) == 0:
        description = None

    final_df = recommender(image=image, text=description, category='sofa', color=False, price_limit=600)
    base_path = '../static/img/wayfair/sofa/'

    return render_template('seeker.html', cat='Sofa', df=final_df, base_path=base_path, form_action="/sofa_seeker#portfolio")


# coffee_table_input
# dining_input
# desk_chair_input
# bookcase_input
# nightstand_input
# bed_input
# dresser_input

              #   <form action="/sofa_seeker" method='POST' >
              #     <input type="text" name="user_input" />
              #   <input type="submit" />
              # </form>


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
