import sys
import os
from curr_app import curr_app

sys.path.append(os.getcwd())

if __name__ == '__main__':
    # ''' !!! Remove the next line for prod, it disables SSL !!! '''
    # # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    curr_app.debug = True
    curr_app.run(
        host='0.0.0.0', port=8000, use_debugger=True, passthrough_errors=True)
