import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("famous-mission-99102-8567a038b529.json", scopes) #access the json key you downloaded earlier
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("AMH_TestFile")  #open sheet
sheet = sheet.sheet1  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

all_cells = sheet.range('A1:C3')

for cell in all_cells:
	print(cell.value)