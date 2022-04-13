########
# This is a living copy/paste collection of various ways TSC has been used throughout the sessions.
# Some code might need to be refactored out of context, be sure to replace URLS, tokens, site names, etc.
########

import csv
import tableaudocumentapi as TDA
import tableauserverclient as TSC
from datetime import datetime, timezone


def get_workbooks():
    # There is no request body to sign in, it's handled here...
    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    #... and here
    with server.auth.sign_in(tab_auth):
        workbooks, paginator = server.workbooks.get()

        return workbooks


def get_workbook_by_luid(wb_luid):
    '''
    Get a workbook via it's LUID
    '''

    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    with server.auth.sign_in(tab_auth):
        workbook = server.workbooks.get_by_id(wb_luid)

        return workbook.__dict__


def filter_workbooks_by_name_req_options(wb_name):
    '''
    Retrieve a filtered list of workbooks where name = wb_name, using TSC.RequestOptions
    '''

    req_options = TSC.RequestOptions()
    req_options.filter.add(TSC.Filter(
        TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, wb_name))

    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    with server.auth.sign_in(tab_auth):
        workbooks, paginator = server.workbooks.get(req_options=req_options)

        return workbooks


def filter_workbooks_by_name_django_style(wb_name):
    '''
    Retrieve a filtered list of workbooks where name = wb_name, using django-style filtering -- YMMV, this method currently only filters the first page of results, be careful!
    '''

    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

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
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

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
            'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
        server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

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
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    with server.auth.sign_in(tab_auth):
        job = server.jobs.get_by_id(job_id)

        return job.__dict__


def publish_workbook_tsc(wb_path, show_tabs, proj_luid):
    '''
    Publish a workbook using TSC
    '''

    wb_filename = wb_path.split('\\')[-1]
    wb_name = wb_filename.split('.')[0]

    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')

    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    with server.auth.sign_in(tab_auth):
        new_wb = TSC.WorkbookItem(
            project_id=proj_luid, name=wb_name, show_tabs=show_tabs)

        publish_wb = server.workbooks.publish(
            workbook_item=new_wb, file=wb_path, mode='Overwrite')

        return publish_wb.__dict__


def publish_ds_with_connection_tsc(ds_path, proj_luid):
    '''
    Publish a datasource with a credential-ed connection using TSC
    '''

    ds_filename = ds_path.split('\\')[-1]
    ds_name = ds_filename.split('.')[0]

    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')

    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    with server.auth.sign_in(tab_auth):
        new_ds = TSC.DatasourceItem(proj_luid, ds_name)

        creds = TSC.ConnectionCredentials('user', 'pw')
        creds.embed = True

        published_ds = server.datasources.publish(
            new_ds, ds_path, mode='Overwrite', connection_credentials=creds)

        return published_ds.__dict__


def get_datasource_connections_tda(ds_path):
    '''
    List connections information from a datasource using Tableau Document API (TDA)
    '''
    ds = TDA.Datasource.from_file(ds_path)

    return [conn.__dict__ for conn in ds.connections]


def update_datasource_and_publish_tda(ds_path, new_server, proj_luid):
    '''
    Use TDA to update the 'server' value in a datasource and then publish it
    '''

    # UPDATE LOCAL FILE SERVER VALUE
    updated_file_path = ds_path.replace('.tdsx', '-updated.tdsx')
    ds_filename = updated_file_path.split('\\')[-1]
    ds_name = ds_filename.split('.')[0]

    ds = TDA.Datasource.from_file(ds_path)
    ds.connections[0].server = new_server

    ds.save_as(updated_file_path)

    # PUBLISH UPDATED FILE
    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')

    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    with server.auth.sign_in(tab_auth):
        new_ds = TSC.DatasourceItem(proj_luid, ds_name)

        creds = TSC.ConnectionCredentials('USER', 'PW')
        creds.embed = True

        published_ds = server.datasources.publish(
            new_ds, updated_file_path, mode='Overwrite', connection_credentials=creds)

        return published_ds.__dict__


def get_tab_auth_server():
    '''
    Extract tab_auth and sever for brevity in subsequent funcs
    '''

    tab_auth = TSC.PersonalAccessTokenAuth(
        'YOUR_PAT_NAME', 'YOUR_PAT_SECRET', site_id='YOUR_SITE_NAME')
    server = TSC.Server('YOUR_SERVER_URL', use_server_version=True)

    return tab_auth, server


def create_new_project():
    '''
    Create a new project using TSC, return the dictionary its properties
    '''

    name = input('Enter New Project Name: ')

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        new_proj_item = TSC.ProjectItem(
            name=name, content_permissions='LockedToProject')

        new_proj = server.projects.create(new_proj_item)

        return new_proj.__dict__


def create_server_group():
    '''
    Create a new (local) group on Tableau Server, return the dictionary of its properties
    '''

    name = input('Enter New Group Name: ')

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        new_group_item = TSC.GroupItem(name=name)

        new_group = server.groups.create(new_group_item)

        return new_group.__dict__


def assign_group_permissions(group_luid, project_name):
    '''
    Assign the default project-level permissions of a group, return the project's properties
    '''

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        projects = list(TSC.Pager(server.projects))
        project = list(filter(lambda x: x.name == project_name, projects))[0]

        groups = list(TSC.Pager(server.groups))
        group = list(filter(lambda x: x._id == group_luid, groups))[0]

        updated_project = server.projects.update_permissions(project, [TSC.PermissionsRule(
            grantee=group,
            capabilities={
                TSC.Permission.Capability.Read: TSC.Permission.Mode.Allow,
                TSC.Permission.Capability.Write: TSC.Permission.Mode.Deny
            }

        )])

        # Default workbook and datasource permissions can also be set here...

        return updated_project


def add_user_to_group(group_name):
    '''
    Add a user to a server group, return the updated group's properties dictionary
    '''

    user_email = input('Enter User\'s Email: ')

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        # I am mixing up filtering methods here on purpose! ;)
        users, paginator = server.users.get()
        user = list(filter(lambda x: x._name == user_email, users))[0]

        groups, paginator = server.groups.get()
        group = list(filter(lambda x: x.name == group_name, groups))[0]

        updated_group = server.groups.add_user(group, user._id)

        return updated_group.__dict__


def refresh_workbook(wb_luid):
    '''
    Create an extract refresh job, return its properties dictionary
    '''

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        return server.workbooks.refresh(wb_luid).__dict__


def build_a_project_from_scratch():
    '''
    Run several functions sequentially to create a project with permissions, users and refreshed content
    '''

    project = create_new_project()
    print(f"- Created project: {project['_name']}")

    group = create_server_group()
    print(f"- Created group: {group['_name']}")

    permissions = assign_group_permissions(group['_id'], project['_name'])
    print('- Applied permissions')

    users_to_group = add_user_to_group(group['_name'])
    print('- Added user to group')

    workbook = publish_workbook_tsc(project['_id'], 'WB_PATH')
    print('- Published initial workbook')

    refresh = refresh_workbook(workbook['_id'])
    print('- Initiated extract refresh, job id: ', refresh['_id'])
