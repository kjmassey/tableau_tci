import tableauserverclient as TSC
from pat import PAT_SECRET
import db_creds

PAT_NAME = 'Kyle'

SERVER_URL = 'https://10ax.online.tableau.com'
SITE_NAME = 'kjmdev797388'

WB_PATH = "C:\\DEV\\Tableau\\tableau_tci\\TCI4_13_APR_22\\e_build_a_project\\Extract workbook.twbx"

########
# Let's put it all together and build a very basic project with groups, permissions, initial content and a refresh!
########


def get_tab_auth_server():
    tab_auth = TSC.PersonalAccessTokenAuth(
        PAT_NAME, PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_URL, use_server_version=True)

    return tab_auth, server


def create_new_project():
    name = input('Enter New Project Name: ')

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        new_proj_item = TSC.ProjectItem(
            name=name, content_permissions='LockedToProject')

        new_proj = server.projects.create(new_proj_item)

        return new_proj.__dict__


def create_server_group():
    name = input('Enter New Group Name: ')

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        new_group_item = TSC.GroupItem(name=name)

        new_group = server.groups.create(new_group_item)

        return new_group.__dict__


def assign_group_permissions(group_luid, project_name):
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


def publish_initial_workbook(proj_luid, wb_path):
    wb_filename = wb_path.split('\\')[-1]
    wb_name = wb_filename.split('.')[0]

    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        new_wb = TSC.WorkbookItem(project_id=proj_luid, name=wb_name)

        creds = TSC.ConnectionCredentials(db_creds.USER, db_creds.PW)
        creds.embed = True

        published_wb = server.workbooks.publish(
            new_wb, wb_path, connection_credentials=creds, mode='Overwrite')

        return published_wb.__dict__


def refresh_workbook(wb_luid):
    tab_auth, server = get_tab_auth_server()

    with server.auth.sign_in(tab_auth):
        return server.workbooks.refresh(wb_luid).__dict__


def build_a_project_from_scratch():
    project = create_new_project()
    print(f"- Created project: {project['_name']}")

    group = create_server_group()
    print(f"- Created group: {group['_name']}")

    permissions = assign_group_permissions(group['_id'], project['_name'])
    print('- Applied permissions')

    users_to_group = add_user_to_group(group['_name'])
    print('- Added user to group')

    workbook = publish_initial_workbook(project['_id'], WB_PATH)
    print('- Published initial workbook')

    refresh = refresh_workbook(workbook['_id'])
    print('- Initiated extract refresh, job id: ', refresh['_id'])


build_a_project_from_scratch()
