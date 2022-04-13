import tableauserverclient as TSC
from pat import PAT_SECRET

SERVER_URL = 'https://10ax.online.tableau.com'
SITE_NAME = 'kjmdev797388'

PAT_NAME = 'Kyle'


def get_workbooks():
    # There is no request body to sign in, it's handled here...
    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL, use_server_version=True)

    #... and here
    with server.auth.sign_in(tab_auth):
        workbooks, paginator = server.workbooks.get()

        return workbooks


print(get_workbooks())
