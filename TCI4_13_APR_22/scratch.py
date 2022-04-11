import tableauserverclient as TSC
from pat import PAT_SECRET

SERVER_URL = 'https://10ax.online.tableau.com/'
SITE_NAME = 'kjmdev797388'

TAB_AUTH = TSC.PersonalAccessTokenAuth('Kyle', PAT_SECRET, site_id=SITE_NAME)
SERVER = TSC.Server(SERVER_URL, use_server_version=True)


with SERVER.auth.sign_in(TAB_AUTH):
    workbooks, paginator = SERVER.workbooks.get()

    print([wb.name for wb in workbooks])
