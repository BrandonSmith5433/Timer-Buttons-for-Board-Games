import pygsheets
from google.oauth2.credentials import Credentials
import TimerButtons

SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
my_credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
gc = pygsheets.authorize(custom_credentials=my_credentials)
cell_list = []
spreadsheet_key= '13boRyfm3qdod6Xvst1DqpUU4sgStL9cO_mrVLL26C4A'

sh = gc.open_by_key(spreadsheet_key)

wks = sh[0] 

def updateCell(total_time, index):
    wks.update_value('B' + str(index + 2), total_time)
