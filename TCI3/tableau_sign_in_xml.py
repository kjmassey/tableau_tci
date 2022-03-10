import requests
from pat_secret import PAT_SECRET

SERVER_URL = 'https://10ax.online.tableau.com/'
SITE_NAME = 'kjmdev797388'

PAT_NAME = 'Kyle'

def get_sign_in_xml():
    return f'''
        <tsRequest>
	        <credentials personalAccessTokenName="{PAT_NAME}" personalAccessTokenSecret="{PAT_SECRET}" >
  		        <site contentUrl="{SITE_NAME}" />
	        </credentials>
        </tsRequest>
    '''

def sign_in():
    resp = requests.post(f"{SERVER_URL}/api/3.14/auth/signin",data=get_sign_in_xml())

    return resp.content

print(sign_in())