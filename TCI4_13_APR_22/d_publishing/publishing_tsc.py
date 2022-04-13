import tableauserverclient as TSC
import tableaudocumentapi as TDA
from db_creds import DB_SERVER, DATABASE, USER, PW, PORT
from pat import PAT_SECRET

PAT_NAME = 'Kyle'

SERVER_URL = 'https://10ax.online.tableau.com'
SITE_NAME = 'kjmdev797388'

WORKBOOK_PATH = "C:\\DEV\\Tableau\\tableau_tci\\TCI4_13_APR_22\\d_publishing\\Fairfield.twbx"
DS_W_CONN_PATH = "C:\\DEV\\Tableau\\tableau_tci\\TCI4_13_APR_22\\d_publishing\\Live Datasource.tdsx"


######
# As we know, TSC eliminates the need to build request bodies and offers a more intuitive way to interact with Tableau's API methods -
# compare how relative simple the process is below!
######

def publish_workbook_tsc(wb_path, show_tabs, proj_luid):
    wb_filename = wb_path.split('\\')[-1]
    wb_name = wb_filename.split('.')[0]

    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)

    server = TSC.Server(SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tab_auth):
        new_wb = TSC.WorkbookItem(
            project_id=proj_luid, name=wb_name, show_tabs=show_tabs)

        publish_wb = server.workbooks.publish(
            workbook_item=new_wb, file=wb_path, mode='Overwrite')

        return publish_wb.__dict__


# print(publish_workbook_tsc(WORKBOOK_PATH, True,
#       '830ab4f5-638a-4473-98ac-cbadb9c35f64'))


def publish_ds_with_connection_tsc(ds_path, proj_luid):
    ds_filename = ds_path.split('\\')[-1]
    ds_name = ds_filename.split('.')[0]

    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)

    server = TSC.Server(SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tab_auth):
        new_ds = TSC.DatasourceItem(proj_luid, ds_name)

        creds = TSC.ConnectionCredentials(USER, PW)
        creds.embed = True

        published_ds = server.datasources.publish(
            new_ds, ds_path, mode='Overwrite', connection_credentials=creds)

        return published_ds.__dict__


# print(publish_ds_with_connection_tsc(
#     DS_W_CONN_PATH, '830ab4f5-638a-4473-98ac-cbadb9c35f64'))

def get_datasource_connections_tda(ds_path):
    ds = TDA.Datasource.from_file(ds_path)

    return [conn.__dict__ for conn in ds.connections]


# print(get_datasource_connections_tda(DS_W_CONN_PATH))

def update_datasource_and_publish_tda(ds_path, new_server, proj_luid):
    # UPDATE LOCAL FILE SERVER VALUE
    updated_file_path = ds_path.replace('.tdsx', '-updated.tdsx')
    ds_filename = updated_file_path.split('\\')[-1]
    ds_name = ds_filename.split('.')[0]

    ds = TDA.Datasource.from_file(ds_path)
    ds.connections[0].server = new_server

    ds.save_as(updated_file_path)

    # PUBLISH UPDATED FILE
    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)

    server = TSC.Server(SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tab_auth):
        new_ds = TSC.DatasourceItem(proj_luid, ds_name)

        creds = TSC.ConnectionCredentials(USER, PW)
        creds.embed = True

        published_ds = server.datasources.publish(
            new_ds, updated_file_path, mode='Overwrite', connection_credentials=creds)

        return published_ds.__dict__


print(update_datasource_and_publish_tda(DS_W_CONN_PATH,
      'google.com', '830ab4f5-638a-4473-98ac-cbadb9c35f64'))
