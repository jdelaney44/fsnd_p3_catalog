### Udacity Full Stack Nano Degree (FSND) Project 4 - Catalog 
#### aka: Lovely Catalogs
**_Prior to sometime after 25 April 2016 this was FSND Project 3_**

#### Most current update: 01 October 2016

This repo is work in process for demonstration & education purposes ONLY. It is NOT intended to be a production ready app. It is not maintained. The Oauth functionality, in particular, may have changed. More on this below.

The following information is for a local installation. For additional summary information on an Amazon Web Services EC2 installation see the AWS_Cfg_Summ.md file in this repository.

### A prototype Python & PostgreSQL(psql) backend & admin porgarm for a catalog system. 
Summary of features: 
* Oauth authentication with Google, Facebook, & Twitter
* mod_wsgi integration for use with Apache
* Multiple catalogs
* Item Categories
* Multiple items within each catalog
* Cross Site Request Forgery protection with Flask-WTF, WTForms and underlying modules
* SQL injection attack protection with SQL Alchemy, Psycopg2, and underlying modules

**System Requirements:**
* Python 2.7
* PostgreSQL
* The virtual machine of your choice or OS that will run Python & PostgreSQL

**Required Python Modules:**

See the file ```requirements.txt```. 

To see if you have all the requirements installed, run ```pip list``` at the command line of your environment. Then compare the output to ```requirements.txt```.

You can run ```pip install -r requirements.txt``` at the ```.../fsnd_p3_catalog/``` directory to install these packages. Depending on your local security (VM or OS) you may need to use ```sudo pip ...```. 

Note: Some functions are used that are unique to psql. They can likely be worked around pretty easily as long as your db engine is exposed to Python via psycopg2. I would set it up, run the test .sql data set up file below and debug from there. 

**Installation & Testing:**

Just fork this project to your git hub account and / or clone it to the working directory where your VM is runninng and where you can start the Python and psql consoles. If you are not using a VM then clone it to your normal working directory.

If you are not using Git then download the ZIP file from Github (look for the button up and to the right from this readme as displayed on Github). Then unzip it to your working directory.

**Data Base Set Up & Initialization:**
  * Install Python, PostgreSQL, and the required Python modules*
  * Fork & clone (or copy) the files as mentioned above
  * You'll want two terminal / shell windows open; one for Python, one for psql
  * Start psql in one of the shells
  * In the shell running psql type '\i tournament.sql'
  * You should see the following output (below):

*The app assumes there is db user(role) named "postgres" and that user/role has a password of 12345. If this is not the case, you will need to change the value for ```SQLALCHEMY_DATABASE_URI``` in ```config.py```. If your db is configured for a public anonymous user/role then the follow string should work:

```SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///catalog_app'```

Thanks to my Udacity reviewer for that string. This simpler string omits the user name, password, host address, & port number of the pgsql engine that go between the 2nd and 3rd slashes. This is a very common local development set up. 

Both URI lines are in ```config.py```, un-comment the one that works for you and comment out the other.

If the URI is not correct you may get an error like "password authentication failed for user "postgress" 

If you are using a different user/role name and password, then you will need to change the value for ```SQLALCHEMY_DATABASE_URI``` in ```config.py``` accordingly. Generically that looks like:

```SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://[psql user/role name]:[password]@[host_name]:[sql_port]/[data_base_name]```

Values inside the brackets ```[]``` are to be replaced with the real values you are using. 

SQL console output:

```
You are now connected to database "postgres" as user "postgres".
DROP DATABASE
CREATE DATABASE
You are now connected to database "catalog_app" as user "postgres".
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
INSERT 0 1
.
.
.
INSERT 0 1
 id | name  | social_id | nickname |        email         | password 
----+-------+-----------+----------+----------------------+----------
  1 | John  | 1         |          | jdelaney01@gmail.com | 12345
  2 | Joe   | 2         |          | jdelaney02@gmail.com | 12345
  3 | Julie | 3         |          | jdelaney03@gmail.com | 12345
  4 | Jane  | 4         |          | jdelaney04@gmail.com | 12345
  5 | Jill  | 5         |          | jdelaney05@gmail.com | 12345
(5 rows)

 catalog_id |     catalog_name      | catalog_description | catalog_owner_id 
------------+-----------------------+---------------------+------------------
          1 | Winter 2016           |                     |                1
          2 | Spring 2016           |                     |                1
          3 | Summer 2016 - Outdoor |                     |                1
          4 | Summer 2016 - Cooking |                     |                1
          5 | Fall 2016 - Clothing  |                     |                1
(5 rows)

 category_id | category_name | category_description | category_owner_id 
-------------+---------------+----------------------+-------------------
           1 | Packs         |                      |                 1
           2 | Tents         |                      |                 1
           3 | Clothing      |                      |                 1
           4 | Foot wear     |                      |                 1
           5 | Appliances    |                      |                 1
           6 | Main Course   |                      |                 1
           7 | Appetizers    |                      |                 1
           8 | Desert        |                      |                 1
           9 | Beverages     |                      |                 1
          10 | Beer & Wine   |                      |                 1
(10 rows)

 item_id | item_name  | item_description | item_price | item_owner_id | item_category_id | item_catalog_id | item_photo_file_name 
---------+------------+------------------+------------+---------------+------------------+-----------------+----------------------
       1 | Blue tent  |                  |     100.96 |             1 |                2 |               3 | 
       2 | Green pack |                  |     125.65 |             1 |                1 |               3 | 
(2 rows)
```

If that succeeded then the basic data base it set up with some test data for you to play around with. To start the application
go to the other shell then
type in:

```
python catalog.py
```
Then the console should show a message like this:

```
 * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 203-261-452

```
Note: the Debugger pin code may be different, I don't have enough experience moving this around to know for sure

That's it! If all those messages appeared then it should be working. 

### Use
 
To use the application do this:
* Open a web browser like Google Chrome.
* Enter the web address ```localhost:8000``` .
* Login using one of the icons at the top for either Facebook, Twitter, or Google+. 
* If you want to test this from a mobile device, only Twitter authentication is working. This is because Google & Facebook don't support remote access to ```localhost:``` or at least not easily.
* You will need an account at one of these services to use this app.

**_The Summer 2016 catalog should have two items in it._**

Hopefully the functionality is fairly self evident from there.

### Image handling

The catalog items can have images. For your convenience there are some images in the ```/test_photos``` sub directroy for you to upload. You may move this folder anywhere. You may also upload files from any other directory.

NOTE: The photos, once uploaded are stored in:

``` [the apps current working dir]/curr_app/static/photos/ ```

If you delete files from the upload directory manually, you will get application errors.

**How image handling works here (briefly)**

This app uses several tools to handle images:
* The modules Flask-WTF, Flask, WT Forms, Jinja2, & Werkzeug and all that they bring in
* Forms as defined in forms.py
* The various HTML templates
* The ```item_photo_file_name``` field for persisting the name of the file
* The ```/static/photos/``` directory under the apps working directory
* The various functions in routes.py
* A Jinja2 "filter function" called ```image_tag``` that is defined in ```__init__.py``` and used in the HTML templates that show images.**

** This is a short, but key function. It allows the pure file name to be stored in the data base and allows us to decouple the file name from the path. The application specific path is built when the HTML is generated & sent to the client browser. While not done here, it would provide for the image path to be a user configurable value -vs- a hard coded value. It also allows the data to be independant of a particular file system structure assumption. 

When the user is creating or editing a catalog item there is a button supplied by the Werkzueg module & wrapped in the WT Forms form object that invokes a file system browsing window. The user can select a file normally.

When the user saves the catalog item or item edit either the add_item or edit_item function handles the POST request. The file name is checked to see if it is for an allowed file types. If the POST os for an edit, we check for existing files, and handle deletion of old files as needed. The data base is updated with the new file name is needed and the file is stored as mentioned above. 

### Notes about Oauth
First, thanks to everyone out there who has posted something on Oauth. I've lifted something from three or four other examples & projects to get this to work.

One thing I found during this project is that the Oauth implementations out there are inconsistent and are changing a little more often than one might like. Of course, the documentation is awful. That's from Google, Facebook, Twitter, and the framework / module projects. 

The Google documentation is particularly problematic as they are working from their Oauth libraries. They don't really deal with more generic approaches. They are also GAE oriented. Perfectly understandable, but, it doesn't make our jobs any easier.

Since Google is different than Twitter which is different than Facebook, and so on, you are really facing down a seperate implementation for each Oauth provider you wish to accomodate. This is compounded by the reality that they will all change on completely different release calendars. Here I have examples of at least three. 

So, don't be shocked if this or any other Oauth implementation doesn't make sense at first. 


## WARNINGS:
If you elect to deploy this on a public server, for some reason, look in the config.py and catalog.py files. There are notes regarding things that need to be either configured or disabled to make that safe(er) to do. 

Again, this is not ready for prime time. The security is pretty good, but it still needs some beefing up. For instance, there are no user roles and there is not any way to protect one user's records from another user. 
