from time import strftime, timezone
import tableauserverclient as TSC
from pat import PAT_SECRET
from datetime import datetime, timezone

SERVER_URL = 'https://10ax.online.tableau.com'
SITE_NAME = 'kjmdev797388'

PAT_NAME = 'Kyle'


def get_workbooks():
    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tab_auth):
        workbooks, paginator = server.workbooks.get()

        return workbooks


# print(get_workbooks())

def filter_workbooks_by_name_req_options(wb_name):
    '''
    Retrieve a filtered list of workbooks where name = wb_name, using TSC.RequestOptions
    '''

    req_options = TSC.RequestOptions()
    req_options.filter.add(TSC.Filter(
        TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, wb_name))

    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tab_auth):
        workbooks, paginator = server.workbooks.get(req_options=req_options)

        return workbooks


# print([wb.name for wb in filter_workbooks_by_name_req_options('30 Rock')])

def filter_workbooks_by_name_django_style(wb_name):
    '''
    Retrieve a filtered list of workbooks where name = wb_name, using django-style filtering -- YMMV, this method currently only filters the first page of results, be careful!
    '''

    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL, use_server_version=True)

    with server.auth.sign_in(tab_auth):
        workbooks = server.workbooks.filter(name=wb_name)

        # Django-style filtering returns a Query from Tableau Server.
        # This means we have to iterate through it to get the actual items
        # Line #59 is an example of 'list comprehension' in Python, which is basically a condensed For loop
        return [wb for wb in workbooks]


# print([wb.name for wb in filter_workbooks_by_name_django_style('30 Rock')])

def filter_datasources_update_before_python_filter(date):
    '''
    GET: Retrieve a filtered list of datasources where 'last updated' <= date using native Python filtering
    '''

    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL, use_server_version=True)

    # Use the datetime library to parse string date
    dt = datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

    with server.auth.sign_in(tab_auth):
        # Using TSC.Pager, we can retrieve all items of a certain class, with no pagination
        # This is extremely handy when you need a large number of results or position/page can't be known in advance
        # The results should be cast to a list
        # POTENTIAL PERFORMANCE IMPACTS

        all_datasources = list(TSC.Pager(server.datasources))

        # 'Lambda' functions in Python are basically a syntax for adhoc operations
        # Filter() takes a lambda for each item in an iterable/list, and the iterable/list

        datasources = list(
            filter(lambda x: x.updated_at <= dt, all_datasources))

        return datasources


print([ds for ds in filter_datasources_update_before_python_filter('2022-06-01')])
