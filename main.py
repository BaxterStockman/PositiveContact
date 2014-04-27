import beaker.middleware
import functools
import pprint
import re
import sys
import urllib
import urllib2
from forms import ContactForm, ContactSearchForm, LoginForm, PhotoForm, SignupForm
from framework import bottle
from google.appengine.api.images import get_serving_url
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from models import Address, Contact, User
from operator import itemgetter
from werkzeug.http import parse_options_header


'''
Thanks to user larsks for this handy way of dealing with
session variables.  Source:
http://stackoverflow.com/questions/13735333/bottle-py-session-with-beaker
'''

session_opts = {
    'session.type': 'ext:google',
    'session.cookie_expires': 10000,
    'session.auto': True,
}


# Set up middleware
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)


# Set up blobstore url
blobstore_url = blobstore.create_upload_url('/upload')


class UploadHander(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        image_data = ImageData(parent=image_key(image_name))
        image_data.name = self.postrequest.get('name')
        image_data.image = blob_info.key()
        image_data.put()

'''
Kudos to Aaron Moodle at Reliably Broken for cluing
me in to the ability to curry* functions using
functools.partial.  Source:
http://reliablybroken.com/b/2010/08/curried-bottle-views/

* Well, not exactly.  It's like returning a NEW curried function whose
arguments happen to be the same as the initial function.

The following code sets a default value for keywords
across all calls to bottle.template()
'''

bottle.template = functools.partial(bottle.template,
    app_name="Positive Contact"
)


@bottle.hook('before_request')
def setup_request():
    session = bottle.request.session = bottle.request.environ.get('beaker.session')
    bottle.BaseTemplate.defaults['session'] = session
    bottle.BaseTemplate.defaults['path'] = bottle.request.path


@bottle.get('/')
def index():
    refresh_contact_dict()
    if 'contacts' in bottle.request.session:
        contacts = bottle.request.session['contacts']
    elif 'user_key_str' in bottle.request.session:
        user_key = ndb.Key(urlsafe=bottle.request.session['user_key_str'])
        if user_key:
            contacts = map(contact_to_dict, Contact.query(Contact.user_key == user_key).fetch())
            bottle.request.session['contacts'] = contacts
        else:
            return bottle.template('templates/base')
    else:
        return bottle.template('templates/base')
    for contact in contacts:
        if 'photo_url' in contact:
            print(contact['photo_url'])
        else:
            print("Nope.")
    sorted_contacts = sorted(contacts, key=itemgetter('lname'))
    return bottle.template('templates/base', search=ContactSearchForm(), contacts=sorted_contacts)


@bottle.get('/login')
def login_form():
    form = LoginForm()
    return bottle.template('templates/base', {
        'action': "Login",
        'form': form
    })


@bottle.post('/login')
def login_submit():
    form = LoginForm(bottle.request.forms.decode())
    if form.validate():
        user_key_str = User.query(User.username ==
                                  form.username.data).get().key.urlsafe()
        #bottle.request.environ.get('beaker.session')['username'] = form.username.data
        bottle.request.session['user_key_str'] = user_key_str
        bottle.request.session['username'] = form.username.data
        bottle.redirect('/')
    else:
        return pprint.pformat(form.data)


@bottle.route('/logout')
def logout_submit():
    bottle.request.session.delete()
    bottle.redirect('/')


@bottle.get('/signup')
def signup_form():
    form = SignupForm()
    return bottle.template('templates/base', {
        'action': "Sign up",
        'form': form,
    })


@bottle.post('/signup')
def signup_submit():
    form = SignupForm(bottle.request.forms.decode())
    if form.validate():
        try:
            new_user = User(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
        except:
            print("Failed to create new user: {0}".format(sys.exc_info()[0]))
        new_user.put()
        bottle.redirect('/')
    else:
        return pprint.pformat(form.data)


@bottle.get('/add')
def add_form():
    form = ContactForm()
    blobstore.create_upload_url('/upload')
    return bottle.template('templates/base', {
        'action': "Add",
        'form': form,
    })


@bottle.post('/add')
def add_submit():
    #photo_file = bottle.request.files.get('photo')
    #return pprint.pformat(photo_file.content_type)
    form_data = bottle.request.forms

    '''
    Bottle keeps file data in a bottle.request.files and
    doesn't maintain any file info in bottle.request.forms,
    so we've got to manually append relevant info.  Here, we
    send the file's mimetype so that WTForms can check whether
    it is an image file.

    Later, we send the image file itself to the GAE blobstore.
    '''
    #form_data.append('photo', photo_file.content_type)
    form = ContactForm(form_data.decode())
    if form.validate():
        user_key_str = bottle.request.session['user_key_str']
        key = create_contact(form, user_key=ndb.Key(urlsafe=user_key_str))
        if 'contacts' in bottle.request.session:
            bottle.request.session['contacts'].append(contact_to_dict(key.get()))
        if form.add_photo.data == True:
            return get_photo(user_key_str)
        else:
            return refresh_path('/')
    else:
        return bottle.template('templates/base', {
            'action': "Add",
            'form': form,
        })


@bottle.get('/edit/<key_str>')
def get_contact(key_str):
    contact = ndb.Key(urlsafe=key_str).get()
    form = contact_to_form(contact)
    bottle.request.contact = contact
    return bottle.template('templates/base', {
        'action': "Edit",
        'form': form,
        'key_str': key_str,
    })


@bottle.post('/edit/<key_str>')
def edit_contact(key_str):
    form_data = bottle.request.forms
    form = ContactForm(form_data.decode())
    if form.validate():
        key = ndb.Key(urlsafe=key_str)
        key.delete()
        user_key_str = bottle.request.session['user_key_str']
        key = create_contact(form, user_key=ndb.Key(urlsafe=user_key_str))
        refresh_contact_dict()
        if form.add_photo.data == True:
            return get_photo(user_key_str)
        else:
            return refresh_path('/')
        return refresh_path('/')
    else:
        return bottle.template('templates/base', {
            'action': "Edit",
            'form': form,
            'key_str': key_str,
        })


@bottle.route('/delete/<key_str>')
def delete_contact(key_str):
    key = ndb.Key(urlsafe=key_str)
    key.delete()
    refresh_contact_dict()
    return refresh_path('/')


@bottle.get('/photo')
def get_photo_fake():
    upload_url = blobstore.create_upload_url("/photo")
    form = PhotoForm()
    return bottle.template('templates/base', {
        'action': "Upload",
        'form': form,
        'upload': upload_url,
    })


@bottle.post('/photo')
def submit_photo_fake():
    photo = bottle.request.files['photo']
    parsed_ct = parse_options_header(photo.content_type)
    blob_key = parsed_ct[1]['blob-key']
    #blob_key = re.search(r'blob-key="(.*?)"', photo.content_type).group(1)
    return blob_key


'''
ENDLESS THANKS to user Koffee at
http://stackoverflow.com/questions/18061264/serve-image-from-gae-datastore-with-flask-python
for hints on how to integrate the Blobstore with Python web
frameworks other than webapp2
'''
@bottle.get('/photo/<key_str>')
def get_photo(key_str):
    upload_url = blobstore.create_upload_url("/photo/" + key_str)
    form = PhotoForm()
    return bottle.template('templates/base', {
        'action': "Upload",
        'form': form,
        'upload': upload_url,
        #'key_str': key_str,
    })

@bottle.post('/photo/<key_str>')
def submit_photo(key_str):
    photo = bottle.request.files['photo']
    parsed_ct = parse_options_header(photo.content_type)
    blob_key = parsed_ct[1]['blob-key']
    ndb_contact = ndb.Key(urlsafe=key_str).get()
    ndb_contact.blob_key = blob_key
    ndb_contact.photo_url = get_serving_url(blob_key, size=32, crop=True)
    ndb_contact.put()
    print("***** blob-key: {0} ******".format(blob_key))
    print("***** photo url: {0} ******".format(ndb_contact.photo_url))
    refresh_contact_dict()
    redirect('/')
    refresh_path('/')


@bottle.error(403)
def error403(code):
    return "Invalid code specified"


@bottle.error(404)
def error404(code):
    return bottle.template('templates/404')


'''
Helper functions
'''


def refresh_contact_dict():
    if 'user_key_str' in bottle.request.session:
        user_key = ndb.Key(urlsafe=bottle.request.session['user_key_str'])
        if user_key:
            contacts = map(contact_to_dict, Contact.query(Contact.user_key == user_key).fetch())
            bottle.request.session['contacts'] = contacts
            return True
    return False


'''
Thanks to Mark Pilgrim's Dive Into Python for help
with regular expression ideas.  Source:
http://www.diveintopython.net/regular_expressions/phone_numbers.html
'''
def parse_phone_number(num):
    match = re.search(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*\d*', num)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None


def contact_to_dict(contact):
    address = contact.address
    return {
        'fname': contact.fname,
        'lname': contact.lname,
        'address': "{0} {1}".format(address.number, address.street),
        'city': address.city,
        'state': address.state,
        'phone': contact.phone,
        'email': contact.email,
        'key_str': contact.key.urlsafe(),
        'blob_key': contact.blob_key,
        'photo_url': contact.photo_url,
    }


def contact_to_form(contact):
    address = contact.address
    return ContactForm(
        fname=contact.fname,
        lname=contact.lname,
        street="{0} {1}".format(address.number, address.street),
        city=address.city,
        state=address.state,
        phone=contact.phone,
        email=contact.email,
    )

def create_contact(form, user_key=None):
    match = re.search(r'(\d+)\s+(.*)', form.street.data)

    try:
        new_address = Address(
            number=match.group(1),
            street=match.group(2),
            city=form.city.data,
            state=form.state.data,
        )
    except:
        print("Failed to create new address: {0}".format(sys.exc_info()[0]))

    try:
        new_contact = Contact(
            fname=form.fname.data,
            lname=form.lname.data,
            address=new_address,
            email=form.email.data,
            phone=form.phone.data,
            user_key=user_key
            #photo=photo_file,
        )
    except:
        print("Failed to create new contact: {0}".format(sys.exc_info()[0]))

    return new_contact.put()


def refresh_path(path, timeout=0):
    return '<meta http-equiv="REFRESH" content="{0};url={1}">'.format(timeout, path)
if __name__ == "__main__":
    bottle.run(server="gae", app=app, debug=True)
