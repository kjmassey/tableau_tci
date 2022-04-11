import tableauserverclient as TSC
from pat import PAT_SECRET

SERVER_URL = 'https://10ax.online.tableau.com/'
SITE_NAME = 'kjmdev797388'

tab_auth = TSC.PersonalAccessTokenAuth('Kyle', PAT_SECRET, site_id=SITE_NAME)
server = TSC.Server(SERVER_URL, use_server_version=True)

with server.auth.sign_in(tab_auth):
    new_ds = TSC.DatasourceItem(
        'f2520dd7-858d-4271-915a-375ee01b8794', name='Extract Datasource 2')

    server.datasources.publish(
        new_ds, r"C:\Users\kylem\Downloads\Extract datasource.tdsx", mode='Overwrite')
