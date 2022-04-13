from sign_in import sign_in, get_token_from_xml, get_site_luid_from_xml
from multipart import make_multipart_req

import requests


SERVER_URL = 'https://10ax.online.tableau.com'
SITE_NAME = 'kjmdev797388'

WORKBOOK_PATH = "C:\\DEV\\Tableau\\tableau_tci\\TCI4_13_APR_22\\d_publishing\\Fairfield.twbx"

#######
# As we will see, building/managing the XML bodies for publishing workbooks/datasources can be cumbersome. This
# is only a basic example of the options available, refer to the matching sections in the REST API docs for more details:
#
# https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_publishing.htm
######


def get_req_body(wb_name, show_tabs, proj_luid):
    return f'''
    <tsRequest>
    <workbook name="{wb_name}" showTabs="{show_tabs}">
        <project id="{proj_luid}"/>
    </workbook>
    </tsRequest>
    '''


def publish_workbook(wb_path, show_tabs, proj_luid):
    auth = sign_in()
    token = get_token_from_xml(auth)
    site_luid = get_site_luid_from_xml(auth)

    wb_filename = wb_path.split('\\')[-1]
    wb_name = wb_filename.split('.')[0]

    wb_contents = open(wb_path, 'rb').read()

    req_body = get_req_body(wb_name, show_tabs, proj_luid)

    req_parts = {
        'request_payload': ('', req_body, 'text/xml'),
        'tableau_workbook': (wb_path, wb_contents, 'application/xml')
    }

    payload, content_type = make_multipart_req(req_parts)

    resp = requests.post(f"{SERVER_URL}/api/3.14/sites/{site_luid}/workbooks?overwrite=true",
                         data=payload, headers={'x-tableau-auth': token, 'content-type': content_type})

    return resp.content


print(publish_workbook(WORKBOOK_PATH, True,
      '830ab4f5-638a-4473-98ac-cbadb9c35f64'))
