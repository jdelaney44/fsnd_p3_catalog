import os


class Config:
    # !!!! If this is to be deployed publically the secret key
    # All development values for the various secret keys have been changed
    # should be set and an OS environment variable
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'somerandomnumberthatwasgeneratedbywhateverrandomnumbergeneratoryouwant'

    # Google Oauth parameters
    # http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
    GOOGLE_CLIENT_ID = 'Change This'
    GOOGLE_CLIENT_SECRET = 'Change This'
    GOOGLE_REDIRECT_URI = 'http://localhost:8000/gconnect'
    GOOGLE_AUTHORIZATION_URL = 'https://www.googleapis.com/oauth2/v4/token'
    GOOGLE_TOKEN_URL = "https://accounts.google.com/o/oauth2/v2/auth"

    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': 'Change This',
            'secret': 'Change This'
        },
        'twitter': {
            'id': 'Change This',
            'secret': 'Change This'
        },
        'google': {
            'id': 'Change This',
            'secret': 'Change This'
        }

    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://catalog01:Blue&pen@localhost:5432/catalog_app'

    # Getting a "password  authentication failed" error from sqlalchemy?
    # Comment out the above URI line and uncomment the URI line below if
    # you're development pgsql instance does not require a user name or password
    # NOTE:The user & password used above is NOT secure and should be used for
    # development purposes only and in a safe, non public,
    # or short lived environment

    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///catalog_app'


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig}
