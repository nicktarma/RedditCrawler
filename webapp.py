
from flask import Flask, request, render_template
app = Flask(__name__)
 
 
# @app.route('/success/<name>')
# def success(name):
#     return 'welcome %s' % name
 
 
@app.route('/', methods=['GET'])
def searchpage():
    return(render_template('searcharea.html'))

@app.route('/results', methods=['POST'])
def results():
    query = request.form['query']

    return(render_template('results.html', query = query))
 
 
if __name__ == '__main__':
    app.run(debug=True)