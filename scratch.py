import tableauserverclient as TSC
from TCI3_30_MAR_22.pat_secret import PAT_SECRET


tab_auth = TSC.PersonalAccessTokenAuth(
    'Kyle', PAT_SECRET, site_id='kjmdev797388')
server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

with server.auth.sign_in(tab_auth):
    req_options = TSC.RequestOptions()
    req_options.filter.add(TSC.Filter(
        TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, 'Hats2'))

    views, paginator = server.views.get(req_options=req_options, usage=True)

    for view in views:
        print(f"{view.name}: {view._total_views}")
