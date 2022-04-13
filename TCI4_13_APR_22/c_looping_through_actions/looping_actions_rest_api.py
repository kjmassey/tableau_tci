from operator import truediv
import tableauserverclient as TSC
import requests
import csv
from sign_in import sign_in, get_site_luid_from_xml, get_token_from_xml, SERVER_URL

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


def get_request_body():
    '''
    Build the request body for refreshing a workbook/datasource -- which is empty!
    '''

    return '<tsRequest></tsRequest>'


def refrest_a_list_of_extracts_from_csv(csv_path):
    '''
    Read a CSV file to a list of dictionaries and send a refresh request for each
    '''

    extract_list = get_items_from_csv(csv_path)

    response_list = []

    for item in extract_list:

        auth = sign_in()
        token = get_token_from_xml(auth)

        headers = {
            'X-Tableau-Auth': token
        }

        item_type_endpoint = 'workbooks'

        if item['object_type'] == 'datasource':
            item_type_endpoint = 'datasources'

        resp = requests.post(
            f"{SERVER_URL}/api/3.14/sites/{item['site_luid']}/{item_type_endpoint}/{item['object_luid']}/refresh", data=get_request_body(), headers=headers)

        response_list.append(resp.content)

    return response_list


def query_job(job_id):
    '''
    Query the status of a job (e.g. extract refresh)
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"{SERVER_URL}/api/3.14/sites/{site_luid}/jobs/{job_id}", headers=headers)

    return resp.content


# print(refrest_a_list_of_extracts_from_csv(
#     r"C:\DEV\Tableau\tableau_tci\TCI4_13_APR_22\c_looping_through_actions\extract_list.csv"))

print(query_job('4da15222-ac20-4d7e-a948-336f32687c86'))
