import os
from flask import render_template, flash, request, url_for, redirect
from flask.json import jsonify
from flask.ext.login import LoginManager, current_user, login_user, \
    logout_user, login_required
from werkzeug import secure_filename

from . import curr_app, forms, db, photo_path
from db_models import User, Catalog, Category, Item
from oauth import OAuthSignIn


''' While not a module some code is being used from this Oauth demo
http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask'''

##############################################################################
# Module globals, setups, helpers ###########################################
# Set up LoginManager requirements ###########################################
login_manager = LoginManager(curr_app)
login_manager.login_view = 'curr_app_login'  # route we use for login

# File extensions allowed for file uploads
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@curr_app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Helper functions & filters ################################################


def get_catalogs():
    catalogs = db.session.query(Catalog).all()
    return catalogs


def get_a_catalog(catalog_id):
    catalog = db.session.query(Catalog).filter_by(catalog_id=catalog_id).one()
    return catalog


def get_an_item(item_catalog_id, item_id):
    item = db.session.query(Item).filter_by(item_catalog_id=item_catalog_id,
                                            item_id=item_id).one()
    return item


def get_a_category(category_id):
    category = db.session.query(Category).filter_by(
        category_id=category_id).one()
    return category


def get_items(catalog_id):
    items = db.session.query(Item).filter_by(item_catalog_id=catalog_id)
    return items


def form_invalid_message(form):
    flash("Form Invalid")
    flash("Validation returned - " + str(form.validate_on_submit()))
    for a in form:
        print str(a)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Authentication & authorization routes ######################################


@curr_app.route('/curr_app_login/', methods=['GET', 'POST'])
def curr_app_login():
    return redirect(url_for('catalogs'))


@curr_app.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('catalogs'))


@curr_app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('catalogs'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@curr_app.route('/callback/<provider>')
def oauth_callback(provider):
    # One arg comes back from Facebook
    if not current_user.is_anonymous:
        return redirect(url_for('catalogs'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('catalogs'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('catalogs'))


###############################################################################
# Catalog routes #############################################################
# View all the catalogs #####################################################


@curr_app.route('/', methods=['GET', 'POST'])
def catalogs():
    catalogs = Catalog.query.all()
    return render_template("/catalogs/catalogs.html", catalogs=catalogs)

# Add a new catalog ########################################################


@curr_app.route('/catalogs/add-catalog/',
                methods=['GET', 'POST'])
@login_required
def add_catalog():
    form = forms.CatalogForm()
    if request.method == 'GET':
        return render_template("/catalogs/addcatalog.html", catalog_form=form)
    else:
        if form.validate_on_submit():
            new_catalog = Catalog()
            new_catalog.catalog_name = request.form["catalog_name"]
            new_catalog.catalog_description = request.form[
                "catalog_description"]
            new_catalog.catalog_owner_id = current_user.id
            db.session.add(new_catalog)
            db.session.commit()
            flash(
                "A new catalog, " + new_catalog.catalog_name +
                ", has been added.")
            return redirect(url_for("catalogs"))
        else:
            flash(
                'Form validation failed, ' + form.errors +
                ', data not saved')
            print 'Validation Failed'
            print form.errors
            return redirect(url_for("catalog_items",
                                    catalog_id=item_catalog_id))

# Edit a catalog ###########################################################


@curr_app.route('/catalogs/edit-catalog/<int:catalog_id>/',
                methods=['GET', 'POST'])
@login_required
def edit_catalog(catalog_id):
    form = forms.CatalogForm()
    catalog = get_a_catalog(catalog_id)

    '''Set up the form to pass to the session'''
    if request.method == 'GET':
        form.catalog_id.data = catalog.catalog_id
        form.catalog_name.data = catalog.catalog_name
        form.catalog_description.data = catalog.catalog_description
        return render_template("/catalogs/editcatalog.html", catalog_form=form)
    else:
        if form.validate_on_submit():
            catalog.catalog_name = str(request.form["catalog_name"])
            catalog.catalog_description = \
                str(request.form["catalog_description"])
            db.session.commit()

            flash(
                "The catalog, " + catalog.catalog_name + ", has been updated!")

            return redirect(url_for("catalogs"))
        else:
            flash(
                'Form validation failed, ' + form.errors + ', data not saved')
            print 'Validation Failed'
            print form.errors
            return redirect(url_for("catalog_items", catalog_form=form))

# Delete a catalog ##########################################################


@curr_app.route('/catalogs/delete-catalog/<int:catalog_id>/',
                methods=['GET', 'POST'])
@login_required
def delete_catalog(catalog_id):
    '''Deletes an entire catalog and it's contents, CAREFUL!'''
    catalog = get_a_catalog(catalog_id)

    if request.method == 'GET':
        return render_template("/catalogs/deletecatalog.html", catalog=catalog)

    else:
        if request.form["delete_catalog"] == "Delete":
            db.session.delete(catalog)
            db.session.commit()
            flash(
                "The catalog, " + catalog.catalog_name +
                ",  has been deleted.")
            return redirect(url_for("catalogs"))


# Add Edit Delete Items ######################################################
# View the item list for a catalog ##########################################


@curr_app.route('/catalogs/catalog/<int:catalog_id>/', methods=['GET', 'POST'])
@login_required
def catalog_items(catalog_id):
    '''List the items in a catalog'''
    form = forms.ItemForm()
    form.item_catalog_id = catalog_id
    catalog = get_a_catalog(catalog_id)
    items = db.session.query(Item).filter_by(item_catalog_id=catalog_id)
    categories = db.session.query(Category).all()
    form.item_categories.choices = [(ca.category_id, ca.category_name)
                                    for ca
                                    in Category.query.order_by(
                                        'category_name')]

    if request.method == 'GET':
        if items.count() == 0:
            flash("No catalog items have been created yet")
            form.item_id = 0
            form.item_catalog_id = catalog_id

        return render_template("/catalogs/catalog_items.html",
                               item_form=form,
                               catalog=catalog,
                               categories=categories,
                               items=items)
    else:
        return redirect(url_for("catalog_items", catalog_id=catalog_id))

# Add Item ##################################################################
# need to just pass the catalog item & query the form to get the values


@curr_app.route('/catalogs/add-item/<int:item_catalog_id>/',
                methods=['GET', 'POST'])
@login_required
def add_item(item_catalog_id):
    '''
    Adds a new item to a catalog

    Images are saved here for a new catalog item. The path is
    in the variable photo_path which is set in __init__.py. This is
    current around line 9. Similar logic is used below. The
    photo_path is built up of the current working directory of
    this server side app and the string '/curr_app/static/photos/'

    '''
    form = forms.ItemForm()
    catalog = get_a_catalog(item_catalog_id)

    form.item_id.data = 999
    form.item_categories.choices = [(c.category_id, c.category_name)
                                    for c in db.session.query(Category).all()]
    form.item_catalog_id.data = item_catalog_id
    form.item_catalog_name.data = catalog.catalog_name

    if request.method == 'GET':
        return render_template("/items/additem.html",
                               item_form=form)
    else:
        try:
            if form.validate_on_submit():
                new_item = Item()
                new_item.item_name = form.item_name.data
                new_item.item_description = form.item_description.data
                new_item.item_price = form.item_price.data
                new_item.item_category_id = form.item_categories.data
                new_item.item_catalog_id = form.item_catalog_id.data

                db.session.add(new_item)
                db.session.commit()

                flash("A new item, " + new_item.item_name +
                      ", ID = " + str(new_item.item_id) +
                      ",  has been added!")

                # If we have a photo, save the photo file name to the db
                # and save the photo file to the file system

                if form.item_photo.data.filename != '':
                    filename = secure_filename(form.item_photo.data.filename)
                    if allowed_file(filename):
                        filename = str(new_item.item_id) + '_' + filename

                        # Save photo file name to the db
                        new_item.item_photo_file_name = filename
                        db.session.commit()

                        # Save the photo file to the file system
                        filename = photo_path + filename
                        form.item_photo.data.save(filename)

                        flash("The photo , " + new_item.item_photo_file_name +
                              ",  has been saved!")

                    else:
                        flash("The photo , " + filename +
                              " is not an allowed file type " +
                              "and has not been saved")

                return redirect(url_for("catalog_items",
                                        catalog_id=item_catalog_id))

            else:
                for err in form.errors.values():
                    flash(
                        'Form validation failed, ' + str(err[0]) +
                        ', data not saved')
                    print err[0]

                return redirect(url_for("catalog_items",
                                        catalog_id=item_catalog_id))

        except Exception, e:
            print "Exception while handling POST in function add_item" + \
                  str(e)


# Edit Item #################################################################
@curr_app.route('/catalogs/edit-item/<int:item_catalog_id>/<int:item_id>/',
                methods=['GET', 'POST'])
@login_required
def edit_item(item_catalog_id, item_id):
    '''Edits an existing item in a catalog'''
    catalog = get_a_catalog(item_catalog_id)
    item = get_an_item(item_catalog_id, item_id)
    old_photo_file_name = item.item_photo_file_name

    if request.method == 'GET':
        try:
            form = forms.ItemForm()
            form.item_id.data = item.item_id
            form.item_name.data = item.item_name
            form.item_description.data = item.item_description
            form.item_categories.data = item.item_category_id
            form.item_price.data = item.item_price
            form.item_catalog_id.data = item_catalog_id
            form.item_catalog_name.data = catalog.catalog_name
            form.item_categories.choices = \
                [(c.category_id, c.category_name)
                    for c in db.session.query(Category).all()]
            form.item_photo.data = item.item_photo_file_name

            return render_template("/items/edititem.html",
                                   item_form=form)
        except Exception, e:
            print "Exception while handling GET in function edit_item - " + \
                  str(e)
    else:
        try:
            form = forms.ItemForm()
            form.item_categories.choices = [
                (c.category_id, c.category_name)
                for c in db.session.query(Category).all()]

            if form.validate_on_submit():
                item.item_name = form.item_name.data
                item.item_description = form.item_description.data
                item.item_category_id = form.item_categories.data
                item.item_price = form.item_price.data

                # save photo if a new file has been chosen
                if form.item_photo.data.filename != old_photo_file_name and \
                        form.item_photo.data.filename != '':

                    # first delete the old photo if there is a new one and
                    # there is one to delete
                    if (form.item_photo.data.filename != '' and
                        old_photo_file_name != '') and \
                            old_photo_file_name is not None:
                        old_photo_path = photo_path + old_photo_file_name
                        os.system('rm ' + old_photo_path)

                    # Set filename, save file to filesystem and filename to db
                    filename = secure_filename(form.item_photo.data.filename)
                    if allowed_file(filename):
                        filename = str(item.item_id) + "_" + filename
                        form.item_photo.data.save(photo_path + filename)
                        item.item_photo_file_name = filename
                    else:
                        flash("The photo , " + filename +
                              " is not an allowed file type and " +
                              "has not been saved")

                db.session.commit()
                flash("The item, " + item.item_name + ", has been updated!")
                return redirect(url_for("catalog_items",
                                        catalog_id=item_catalog_id))
            else:
                print 'Validation Failed'
                for err in form.errors.values():
                    flash(
                        'Form validation failed, ' + str(err[0]) +
                        ', data not saved')
                    print err[0]
                return redirect(url_for("catalog_items",
                                        catalog_id=item_catalog_id))

        except Exception, e:
            print "Catalog App Exception while handling POST" + \
                "in function routes.edit_item : " + \
                str(e)


# Delete Item ###############################################################


@curr_app.route('/catalogs/delete-item/<int:item_catalog_id>/<int:item_id>',
                methods=['GET', 'POST'])
@login_required
def delete_item(item_catalog_id, item_id):
    '''Deletes an item from a catalog'''
    catalog = get_a_catalog(item_catalog_id)
    item = get_an_item(item_catalog_id, item_id)

    if request.method == 'GET':
        return render_template("/items/deleteitem.html",
                               catalog=catalog,
                               item=item)
    else:
        if request.form["delete_catalog_item"] == "Delete":
            if item.item_photo_file_name != '' and \
                    item.item_photo_file_name is not None:
                old_photo_path = photo_path + item.item_photo_file_name
                os.system('rm ' + old_photo_path)

            db.session.delete(item)
            db.session.commit()
            flash("The item, " + item.item_name + ", has been deleted.")
            return redirect(url_for("catalog_items",
                                    catalog_id=item_catalog_id))

###############################################################################
# Category routes ############################################################
# View all the categories


@curr_app.route('/categories/', methods=['GET'])
def categories():
    categories = Category.query.all()
    return render_template("/categories/categories.html",
                           categories=categories)

# Add a new category #####################################################


@curr_app.route('/categories/add-category/',
                methods=['GET', 'POST'])
@login_required
def add_category():
    form = forms.CategoryForm()
    if request.method == 'GET':
        return render_template("/categories/addcategory.html",
                               category_form=form)
    else:
        if form.validate_on_submit():
            new_category = Category()
            new_category.category_name = request.form["category_name"]
            new_category.category_description = request.form[
                "category_description"]
            new_category.category_owner_id = current_user.id
            db.session.add(new_category)
            db.session.commit()
            flash(
                "A new category, " + new_category.category_name +
                ", has been added.")
            return redirect(url_for("categories"))
        else:
            flash(
                'Form validation failed, ' + form.errors + ', data not saved')
            print 'Validation Failed'
            print form.errors
            return redirect(url_for("category_items",
                                    category_id=item_category_id))

# Edit a category ###########################################################


@curr_app.route('/categories/edit-category/<int:category_id>/',
                methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = forms.CategoryForm()
    category = get_a_category(category_id)

    '''Set up the form to pass to the session'''
    '''xxxxxxxxx'''

    if request.method == 'GET':
        form.category_id.data = category.category_id
        form.category_name.data = category.category_name
        form.category_description.data = category.category_description
        return render_template("/categories/editcategory.html",
                               category_form=form)
    else:
        if form.validate_on_submit():
            category.category_name = str(request.form["category_name"])
            category.category_description = \
                str(request.form["category_description"])
            db.session.commit()

            flash(
                "The category, " + category.category_name +
                ", has been updated!")

            return redirect(url_for("categories"))
        else:
            flash(
                'Form validation failed, ' + form.errors +
                ', data not saved')
            print 'Validation Failed'
            print form.errors
            return redirect(url_for("category_items", category_form=form))

# Delete a category ########################################################


@curr_app.route('/categories/delete-category/<int:category_id>/',
                methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    '''Deletes an entire category and it's contents, CAREFUL!'''
    category = get_a_category(category_id)

    if request.method == 'GET':
        return render_template("/categories/deletecategory.html",
                               category=category)

    else:
        if request.form["delete_category"] == "Delete":
            db.session.delete(category)
            db.session.commit()
            flash(
                "The category, " + category.category_name +
                ",  has been deleted.")
            return redirect(url_for("categories"))

##############################################################################
# JSON endpoints here #######################################################


@curr_app.route('/catalogs/JSON/')
@login_required
def catalogsJSON():
    catalogs = get_catalogs()
    return jsonify(Catalogs=[catalog.serialize for catalog in catalogs])


@curr_app.route('/catalog/<int:catalog_id>/JSON/')
@login_required
def catlogJSON(catalog_id):
    items = get_items(catalog_id)
    return jsonify(Items=[i.serialize for i in items])


@curr_app.route('/catalog/<int:catalog_id>/item/<int:item_id>/JSON/')
def catalogItemJSON(catalog_id, item_id):
    item = get_an_item(catalog_id, item_id)
    return jsonify(Item=[item.serialize])

# End Of File ################################################################
