import os
from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

# declare & set up globals ###################################################
# photo_path = os.getcwd()
basedir = os.path.abspath(os.path.dirname(__file__))
photo_path = basedir
# photo_path = photo_path + '/curr_app/static/photos/'
photo_path = photo_path + '/static/photos/'

# instantiate the application object with configs
config_name = 'development'
curr_app = Flask('curr_app')
curr_app.config.from_object(config[config_name])

# instantiate the data base object
db = SQLAlchemy(curr_app)

# bootstrap = Bootstrap(curr_app)
Bootstrap(curr_app)

# the db definitions come with routes
import routes

# Set up data base support. If the db already exists it is not affected
db.create_all()


# Define Jinja2 filters for html page generation using  templates
def debug01(text):
    '''Print debug info to the app console

    This debug filter will print a string from an html template
    to the app console. Usage in the template is like this:

      {{"Reached end of the template"|debug01}}

    Typically a line like the one above would be placed in the template
    at an arbitrary position. This is  so you can see that processing
    reached that point in the template. Can be useful when a page is not
    rendering things. Allows you to see that the template was at least
    rendered by Jinja2 or frameworks using Jinja2.
    '''

    print "\n" + text + "\n"
    return ''

# add the filter to the collection of filters
curr_app.jinja_env.filters['debug01'] = debug01


def format_currency(value):
    '''
    Format numbers as currency, US Dollars

    format_currency applies a dollar sign to the front of of a number,
    inserts commas appropriately and forces two digits after the decimal
    even if the number is not fractional.

    IE: 9999 will be displayed as $9,999.00
    '''

    return "${:,.2f}".format(value)

# add the filter to the collection of filters
curr_app.jinja_env.filters['format_currency'] = format_currency


def image_tag(image_file):
    '''
    Adds the photos/ directory to the path for the supplied file name.
    Jinja assumes /static/ is the path for content. With url_for this
    substitutes the complete path so the  path in HTML
    will be /static/photos/{filename}

    :param image_file: name of the image file. This is from the data base.
    table: items, column: item_photo_file_name. It is set in various view
    functions in routes.py. IE: edit_Item

    :return: Returns the path /static/photos/{filename}
    '''
    return url_for('static', filename='photos/{}'.format(image_file))
curr_app.jinja_env.filters['image_tag'] = image_tag

# assign the jinja filters to an application level object
curr_filters = curr_app.jinja_env.filters
