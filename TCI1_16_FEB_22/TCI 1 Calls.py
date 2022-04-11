import tableauserverclient as TSC

SERVER_URL = 'https://10ax.online.tableau.com/'
PAT = 'wk01meshQA+/uINR2061GA==:XG4JKgQ7K2KouS0vvT0DWupBhluKrlUs'
SITE_NAME = 'kjmdev797388'

def sign_in():
    tab_auth = TSC.PersonalAccessTokenAuth('Kyle',PAT,site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL,use_server_version=True)

    with server.auth.sign_in(tab_auth):
        return server.auth_token

def get_site_workbooks():
    tab_auth = TSC.PersonalAccessTokenAuth('Kyle',PAT,site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL,use_server_version=True)

    with server.auth.sign_in(tab_auth):
        workbooks, paginator = server.workbooks.get()
        
        return workbooks

def get_site_workbooks_pager():
    tab_auth = TSC.PersonalAccessTokenAuth('Kyle',PAT,site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL,use_server_version=True)

    with server.auth.sign_in(tab_auth):
        return list(TSC.Pager(server.workbooks))


def filter_workbooks_req_options():
    tab_auth = TSC.PersonalAccessTokenAuth('Kyle',PAT,site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL,use_server_version=True)

    with server.auth.sign_in(tab_auth):
        req_options = TSC.RequestOptions()
        req_options.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,TSC.RequestOptions.Operator.Equals,'Regional Manager Performance'))

        workbooks, paginator = server.workbooks.get(req_options=req_options)

        return workbooks

def filter_workbooks_django_style():
    tab_auth = TSC.PersonalAccessTokenAuth('Kyle',PAT,site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL,use_server_version=True)

    with server.auth.sign_in(tab_auth):
        #workbooks.filter does NOT return a paginator, takes list()
        workbooks = list(server.workbooks.filter(name='Regional Manager Performance'))

        return workbooks

def filter_workbooks_python():
    tab_auth = TSC.PersonalAccessTokenAuth('Kyle',PAT,site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL,use_server_version=True)

    with server.auth.sign_in(tab_auth):
        all_workbooks = list(TSC.Pager(server.workbooks))

        filtered_workbooks = list(filter(lambda x: x.name == 'Regional Manager Performance', all_workbooks))

        return filtered_workbooks


print([wb.__dict__ for wb in filter_workbooks_python()])
