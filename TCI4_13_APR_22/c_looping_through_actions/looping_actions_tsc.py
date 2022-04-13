import tableauserverclient as TSC
from pat import PAT_SECRET
import csv

SERVER_URL = 'https://10ax.online.tableau.com'
SITE_NAME = 'kjmdev797388'

PAT_NAME = 'Kyle'


def get_items_from_csv(csv_path):
    '''
    Read a csv file into a list of dictionaries
    '''

    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        return list(csv_reader)


def refresh_list_of_extracts_from_csv_tsc(csv_path):
    '''
    Read a CSV file to a list of dictionaries and send a refresh request for each
    '''

    extract_list = get_items_from_csv(csv_path)

    response_list = []

    for item in extract_list:

        tab_auth = TSC.PersonalAccessTokenAuth(
            PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
        server = TSC.Server(SERVER_URL, use_server_version=True)

        with server.auth.sign_in(tab_auth):

            if item['object_type'] == 'workbook':

                wb = server.workbooks.get_by_id(item['object_luid'])
                response_list.append(server.workbooks.refresh(wb._id))

            else:
                ds = server.datasources.get_by_id(item['object_luid'])
                response_list.append(server.datasources.refresh(ds._id))

    return response_list


def query_job_tsc(job_id):
    '''
    Query the status of a job (e.g. extract refresh)
    '''

    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tab_auth):
        job = server.jobs.get_by_id(job_id)

        return job.__dict__


# print(refresh_list_of_extracts_from_csv_tsc(
#     r"C:\DEV\Tableau\tableau_tci\TCI4_13_APR_22\c_looping_through_actions\extract_list.csv"))

print(query_job_tsc('0b7ba82e-71b7-4719-a374-3d7b39bdb319'))
