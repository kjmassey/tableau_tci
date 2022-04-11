from TCI4_13_APR_22.a_introducing_tsc.pat import PAT_SECRET
import tableauserverclient as TSC
import csv

tab_auth = TSC.PersonalAccessTokenAuth(
    'Kyle', PAT_SECRET, site_id='kjmdev797388')
server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

with server.auth.sign_in(tab_auth):
    workbooks = list(filter(lambda x: 'Extract' in x.name,
                     list(TSC.Pager(server.workbooks))))
    datasources = list(filter(lambda x: 'Extract' in x.name,
                       list(TSC.Pager(server.datasources))))

    wb_map = list(map(lambda x: x.__dict__, workbooks))

    with open('out.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, wb_map[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(wb_map)

    ds_map = list(map(lambda x: x.__dict__, datasources))

    with open('out2.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, ds_map[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(ds_map)
