from framework import bottle
#from google.appengine.ext.webapp.util import run_wsgi_app
#from backend import *


app = application = bottle.Bottle()


@app.route('/')
def index():
    return bottle.template('templates/home', {'proj_name': "Positive Contact"})


@app.route('/create')
def create_contact():
    return ""


@app.route('/edit')
def edit_contact():
    return ""


@app.error(403)
def error403(code):
    return "Invalid code specified"


@app.error(404)
def error404(code):
    #return "That resource does not exist"
    return bottle.template('templates/404', {'proj_name': "Positive Contact"})


if __name__ == "__main__":
    bottle.run(server="gae", debug=True)
