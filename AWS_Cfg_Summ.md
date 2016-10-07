## FSND P7 : Linux Based Server Configuration

## Server Information

**IP Address** - 54.148.23.168

**URL** - http://ec2-54-148-23-168.us-west-2.compute.amazonaws.com

##Installed Software Summary

* Apache2 - For www serving
* libapache2-mod-wsgi - Python mod_wsgi layer for Apache
* git - For bringing down the application from Github
* libq-dev & python-dev - needed so the psycopg2 Python module works (needed before pip install requirements.txt is run)
* postgresql
* pip - Python installer

* Python packages defined in requirements.txt of the app:
  * Flask
  * Flask-Bootstrap
  * Flask-Login
  * Flask-SQLAlchemy
  * Flask-WTF
  * itsdangerous
  * Jinja2
  * MarkupSafe==0.23
  * psycopg2==2.6.1
  * rauth==0.7.2
  * requests==2.10.0
  * SQLAlchemy==0.9.3
  * Werkzeug==0.11.8
  * WTForms==2.1

* Unix Utilities
  * tree
 

## Configuration Summary
* Secure Shell Daemon - sshd - moved to port 2200 from 22
* Uncomplicated Fire Wall (UFW) configured as follows:
```
	To                         Action      From
	--                         ------      ----
	2200/tcp                   ALLOW IN    Anywhere
	80/tcp                     ALLOW IN    Anywhere
	123                        ALLOW IN    Anywhere
	2200/tcp (v6)              ALLOW IN    Anywhere (v6)
	80/tcp (v6)                ALLOW IN    Anywhere (v6)
	123 (v6)                   ALLOW IN    Anywhere (v6)
```

* Set timzone to UTC

* WSGI script location
  In `/etc/apache2/sites-enabled/000-default.conf` add the line

  `WSGIScriptAlias / /var/www/html/apps/fsnd_p3_catalog/catalog.wsgi`

  That is between the `<VirtualHost></VirtualHost>` tags

* PostgreSQL permissions
  
  * In /etc/postgresql/9.3/main/pg_hba.conf

    * Added
      ```
      local   catalog01       catalog01                       md5
      host    catalog_app     catalog01       127.0.0.1/32    password
      ```

    * Commented out

      ```
      # "local" is for Unix domain socket connections only
      # IPv4 local connections:
      # host    all             all             127.0.0.1/32            md5
      # IPv6 local connections:
      # host    all             all             ::1/128                 md5
      ```


* Application Mods

  * Added a file called catalog.wsgi containing:
  ```
		import sys
		sys.path.insert(0, '/var/www/html/apps/fsnd_p3_catalog')

		from curr_app import curr_app as application
  ```

  * Had to change a path reference in the application to a form that was not dependent on how mod_wsgi sees it's current working directory:
  ```
	Old code:

	photo_path = os.getcwd()
	photo_path = photo_path + '/curr_app/static/photos/'

	New code:

	basedir = os.path.abspath(os.path.dirname(__file__))
	photo_path = basedir
	photo_path = photo_path + '/static/photos/'
	```
	* Permission changes for photo upload:

	  ```sudo chmod 777 /var/www/html/apps/fsnd_p3_catalog/curr_app/static/photos```


##Users added & related user security settings 
  * jdelaney4401 (added to sudoers) - my account
  * grader (added to sudoers)
  * catalog01 (for app to login into postgreSQL)
  * postgres (auto added by postgreSQL install)
  * In the user files unders /etc/sudoers.d made the entry
  ```
    # This next line will turn on password for sudo  
    [user_name] ALL=(ALL) ALL 
    # This next line will turn off password for sudo
    # [user_name] ALL=NOPASSWD: ALL

  ```

  Passwords are set on all users. 
  Passwords have been needed to su  & sudo for grader & jdelaney4401 users
  Users postgres & catalog01 are not in sudoers.d

  * Disabled root login with `PermitRootLogin` entry in sshd_config:

  ```
    # Authentication:
    LoginGraceTime 120
    PermitRootLogin no  
    StrictModes yes
  ```
  Checked running services with `service --status-all` to make sure that FTP, Telnet, and SMTP are not running or anything else that looks like it would allow a user login, looks okay. 

##OAuth updates:
  * Google - 
    * Update the Authorized redirect URIs with - `http://ec2-54-148-23-168.us-west-2.compute.amazonaws.com/callback/google`

  * Facebook - 
    * Recreate the project and input the ID & Secret Key values in config.py


##Third Party Resources
  * Misc server setups

    https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-12-04

    https://forums.aws.amazon.com/thread.jspa?threadID=160352 

  * The Udacity course materials for this project

  * Firewall - https://help.ubuntu.com/community/UFW#Allow_Access

  * sshd - 

    https://www.howtoforge.com/community/threads/change-ssh-to-listen-on-two-ports.47365/

    http://askubuntu.com/questions/449364/what-does-without-password-mean-in-sshd-config-file

  * Time zone - http://askubuntu.com/questions/3375/how-to-change-time-zone-settings-from-the-command-line

  * Installing pip - http://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/

  * Python pyscopg2 requirements - http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi

  * mod-wsgi setup - http://flask.pocoo.org/docs/0.11/deploying/mod_wsgi/

  * mod_wsgi debugging path - https://gist.github.com/dAnjou/2874714

  * PostgreSQL security - https://www.postgresql.org/docs/9.0/static/user-manag.html

  * sudo password disabling - http://www.ducea.com/2006/06/18/linux-tips-password-usage-in-sudo-passwd-nopasswd/

  * sudo man page - https://www.sudo.ws/man/1.8.17/sudoers.man.html

  * Checking running services - http://askubuntu.com/questions/407075/how-to-read-service-status-all-results


