from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, RifleModelName, RifleName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///rifles.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Rifles Store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
vrs_cat = session.query(RifleModelName).all()


# login
@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    vrs_cat = session.query(RifleModelName).all()
    vres = session.query(RifleName).all()
    return render_template('login.html',
                           STATE=state, vrs_cat=vrs_cat, vres=vres)
    # return render_template('myhome.html', STATE=state
    # vrs_cat=vrs_cat,vres=vres)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# It shows Home


@app.route('/')
@app.route('/home')
def home():
    vrs_cat = session.query(RifleModelName).all()
    return render_template('myhome.html', vrs_cat=vrs_cat)


# RifleStore Category for admins
@app.route('/RifleStore')
def RifleStore():
    try:
        if login_session['username']:
            name = login_session['username']
            vrs_cat = session.query(RifleModelName).all()
            vrs = session.query(RifleModelName).all()
            vres = session.query(RifleName).all()
            return render_template('myhome.html', vrs_cat=vrs_cat,
                                   vrs=vrs, vres=vres, uname=name)
    except:
        return redirect(url_for('showLogin'))


# Showing Rifles based on Rifle category
@app.route('/RifleStore/<int:vrid>/AllModels')
def showRifles(vrid):
    vrs_cat = session.query(RifleModelName).all()
    vrs = session.query(RifleModelName).filter_by(id=vrid).one()
    vres = session.query(RifleName).filter_by(riflemodelnameid=vrid).all()
    try:
        if login_session['username']:
            return render_template('showRifles.html', vrs_cat=vrs_cat,
                                   vrs=vrs, vres=vres,
                                   uname=login_session['username'])
    except:
        return render_template('showRifles.html',
                               vrs_cat=vrs_cat, vrs=vrs, vres=vres)


# Adds New Rifle
@app.route('/RifleStore/addRifleModel', methods=['POST', 'GET'])
def addRifleModel():
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        model = RifleModelName(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(model)
        session.commit()
        return redirect(url_for('RifleStore'))
    else:
        return render_template('addRifleModel.html', vrs_cat=vrs_cat)


# It is For Edit Rifle Category
@app.route('/RifleStore/<int:vrid>/edit', methods=['POST', 'GET'])
def editRifleCategory(vrid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    editedRifle = session.query(RifleModelName).filter_by(id=vrid).one()
    creator = getUserInfo(editedRifle.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Rifle Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('RifleStore'))
    if request.method == "POST":
        if request.form['name']:
            editedRifle.name = request.form['name']
        session.add(editedRifle)
        session.commit()
        flash("Rifle Category Edited Successfully")
        return redirect(url_for('RifleStore'))
    else:
        # vrs_cat is global variable we can them in entire application
        return render_template('editRifleCategory.html',
                               vr=editedRifle, vrs_cat=vrs_cat)


# It is for Delete Rifle Category
@app.route('/RifleStore/<int:vrid>/delete', methods=['POST', 'GET'])
def deleteRifleCategory(vrid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    vr = session.query(RifleModelName).filter_by(id=vrid).one()
    creator = getUserInfo(vr.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Rifle Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('RifleStore'))
    if request.method == "POST":
        session.delete(vr)
        session.commit()
        flash("Rifle Category Deleted Successfully")
        return redirect(url_for('RifleStore'))
    else:
        return render_template(
            'deleteRifleCategory.html', vr=vr, vrs_cat=vrs_cat)


# Add New Rifle Details
@app.route('/RifleStore/addModel/addRifleDetails/<string:vrname>/add',
           methods=['GET', 'POST'])
def addRifleDetails(vrname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    vrs = session.query(RifleModelName).filter_by(name=vrname).one()
    # See if the logged in user is not the owner of rifle
    creator = getUserInfo(vrs.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new rifle"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showRifles', vrid=vrs.id))
    if request.method == 'POST':
        name = request.form['name']
        ammo = request.form['ammo']
        capacity = request.form['capacity']
        power = request.form['power']
        range = request.form['range']
        stability = request.form['stability']
        rlink = request.form['rlink']
        rifledetails = RifleName(name=name,
                                 ammo=ammo,
                                 capacity=capacity, power=power,
                                 range=range,
                                 stability=stability,
                                 rlink=rlink,
                                 date=datetime.datetime.now(),
                                 riflemodelnameid=vrs.id,
                                 user_id=login_session['user_id'])
        session.add(rifledetails)
        session.commit()
        return redirect(url_for('showRifles', vrid=vrs.id))
    else:
        return render_template('addRifleDetails.html',
                               vrname=vrs.name, vrs_cat=vrs_cat)


# Edit Rifle details
@app.route('/RifleStore/<int:vrid>/<string:vrename>/edit',
           methods=['GET', 'POST'])
def editRifle(vrid, vrename):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    vr = session.query(RifleModelName).filter_by(id=vrid).one()
    rifledetails = session.query(RifleName).filter_by(name=vrename).one()
    # See if the logged in user is not the owner of rifle
    creator = getUserInfo(vr.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this rifle"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showRifles', vrid=vr.id))
    # POST methods
    if request.method == 'POST':
        rifledetails.name = request.form['name']
        rifledetails.ammo = request.form['ammo']
        rifledetails.capacity = request.form['capacity']
        rifledetails.power = request.form['power']
        rifledetails.range = request.form['range']
        rifledetails.stability = request.form['stability']
        rifledetails.rlink = request.form['rlink']
        rifledetails.date = datetime.datetime.now()
        session.add(rifledetails)
        session.commit()
        flash("Rifle Edited Successfully")
        return redirect(url_for('showRifles', vrid=vrid))
    else:
        return render_template('editRifle.html',
                               vrid=vrid, rifledetails=rifledetails,
                               vrs_cat=vrs_cat)


# Delte Rifle Details
@app.route('/RifleStore/<int:vrid>/<string:vrename>/delete',
           methods=['GET', 'POST'])
def deleteRifle(vrid, vrename):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    vr = session.query(RifleModelName).filter_by(id=vrid).one()
    rifledetails = session.query(RifleName).filter_by(name=vrename).one()
    # See if the logged in user is not the owner of rifle
    creator = getUserInfo(vr.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this rifle"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showRifles', vrid=vr.id))
    if request.method == "POST":
        session.delete(rifledetails)
        session.commit()
        flash("Deleted Rifle Successfully")
        return redirect(url_for('showRifles', vrid=vrid))
    else:
        return render_template('deleteRifle.html',
                               vrid=vrid, rifledetails=rifledetails,
                               vrs_cat=vrs_cat)


# Logout from user
@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type':
                           'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Json
# Displays all the details that we have
@app.route('/RifleStore/JSON')
def allRiflesJSON():
    riflecategories = session.query(RifleModelName).all()
    category_dict = [c.serialize for c in riflecategories]
    for c in range(len(category_dict)):
        rifles = [i.serialize for i in session.query(
                 RifleName).filter_by(riflemodelnameid=category_dict[c]["id"]
                                      ).all()]
        if rifles:
            category_dict[c]["rifle"] = rifles
    return jsonify(RifleModelName=category_dict)

# Displays the Rifle Catagories


@app.route('/rifleStore/rifleCategories/JSON')
def categoriesJSON():
    rifles = session.query(RifleModelName).all()
    return jsonify(rifleCategories=[c.serialize for c in rifles])

# Displays all Rifle Details in Rifle catagories


@app.route('/rifleStore/rifles/JSON')
def itemsJSON():
    items = session.query(RifleName).all()
    return jsonify(rifles=[i.serialize for i in items])

# Displays details of rifle


@app.route('/rifleStore/<path:rifle_name>/rifles/JSON')
def categoryItemsJSON(rifle_name):
    rifleCategory = session.query(RifleModelName).filter_by(name=rifle_name
                                                            ).one()
    rifles = session.query(RifleName).filter_by(riflemodelname=rifleCategory
                                                ).all()
    return jsonify(rifleEdtion=[i.serialize for i in rifles])

# Displays the details of a given rifle


@app.route('/rifleStore/<path:rifle_name>/<path:edition_name>/JSON')
def ItemJSON(rifle_name, edition_name):
    rifleCategory = session.query(RifleModelName).filter_by(name=rifle_name
                                                            ).one()
    rifleEdition = session.query(RifleName).filter_by(
           name=edition_name, riflemodelname=rifleCategory).one()
    return jsonify(rifleEdition=[rifleEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
