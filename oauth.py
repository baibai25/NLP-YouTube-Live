import os
import httplib2
from oauth2client import tools
from oauth2client import client
from oauth2client.file import Storage

credentials_path = "credentials.json"
store = Storage(credentials_path)
credentials = store.get()

if credentials is None or credentials.invalid:
    f = "client.json"
    scope = "https://www.googleapis.com/auth/youtube.readonly"
    flow = client.flow_from_clientsecrets(f, scope)
    flow.user_agent = "YouTube Live Comment"
    credentials = tools.run_flow(flow, Storage(credentials_path))
