from http import server
import tableauserverclient as TSC
from pat import PAT_SECRET

SERVER_URL = 'https://10ax.online.tableau.com/'
SITE_NAME = 'kjmdev797388'

TAB_AUTH = TSC.PersonalAccessTokenAuth('Kyle', PAT_SECRET, site_id=SITE_NAME)
SERVER = TSC.Server(SERVER_URL, use_server_version=True)


with SERVER.auth.sign_in(TAB_AUTH):
    # Always returns a list
    workbooks = SERVER.workbooks.filter(name='30 Rock')

    # First result
    wb = workbooks[0]

    # Query Tableau Server for connections
    SERVER.workbooks.populate_connections(wb)

    print(wb.connections)
