from flask import Flask, render_template, request
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html', title='Hello!')

# @app.route('/more/')
# def more():
#     return render_template('index.html')


# My maps
@app.route('/map', methods=['POST'] )
def map():
    text = str(request.form['user_input'])


    

    # return render_template('locked_out.html', map_name = 'Rescue Lock In/Out', maplink = maplink)


    # return render_template('map.html', map_name = map_name, maplink = maplink)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
