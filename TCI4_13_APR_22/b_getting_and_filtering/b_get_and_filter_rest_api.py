import requests
from sign_in import sign_in, get_site_luid_from_xml, get_token_from_xml, SERVER_URL


def get_workbooks():
    '''
    Simple GET request to get all workbooks from site.

    Has no parameters, uses X-Tableau-Auth header
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"{SERVER_URL}/api/3.14/sites/{site_luid}/workbooks", headers=headers)

    return resp.content

# print(get_workbooks())


def get_workbook_by_luid(wb_luid):
    '''
    GET: Retrieve a workbook via its luid.

    Has no parameters, uses X-Tableau-Auth header
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"{SERVER_URL}/api/3.14/sites/{site_luid}/workbooks/{wb_luid}", headers=headers)

    return resp.content


# print(get_workbook_by_luid('2ec783f1-078b-4f5e-9673-dadd68539fd6'))


def filter_workbooks_by_name(wb_name):
    '''
    GET: Retrieve a filtered list of workbooks where name = wb_name
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"{SERVER_URL}/api/3.14/sites/{site_luid}/workbooks/?filter=name:eq:{wb_name}", headers=headers)

    return resp.content

# print(filter_workbooks_by_name('30 Rock'))


def filter_datasources_updated_before(date):
    '''
    GET: Retrieve a filtered list of datasources where 'last updated' <= date
    '''

    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    headers = {
        'X-Tableau-Auth': token
    }

    resp = requests.get(
        f"{SERVER_URL}/api/3.14/sites/{site_luid}/workbooks/?filter=updatedAt:lte:{date}", headers=headers)

    return resp.content

# print(filter_datasources_updated_before('2021-01-10T00:00:00Z'))
