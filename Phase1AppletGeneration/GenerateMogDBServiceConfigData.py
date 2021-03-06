import xlrd
from pymongo import MongoClient

# Workbook location
loc = ('/home/kulani/Projects/ImpTATester/ServiceWebScraping/Phase1AppletGeneration/servicexls/SERVICE_CONFIGURATION details.xls')

# Open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
print('No of records: '+str(sheet.nrows))
###########################################################################
uri = 'mongodb://127.0.0.1:27017'
client = MongoClient(uri)
db = client['services']
collection = db.get_collection('serviceconfigdetails')
collection.remove({})
#######################
# Set up Mongo DB Cloud
# client = MongoClient('mongodb+srv://ifttt:ifttt@cluster0-b5sb3.mongodb.net/test?retryWrites=true&w=majority')
# db = client.get_database('services')
# collection = db.get_collection('authdetails')
# c2 = db.get_collection('authdetails')
# c2.remove({})
###########################################################################
#  value(row no, column no)
for i in range(sheet.nrows):
    if i == 0:
        continue
    serviceID = sheet.cell_value(i,1)
    eventType = sheet.cell_value(i,2)
    eventName = sheet.cell_value(i,3)
    eventDesc = sheet.cell_value(i,4)
    doc = {
        'service_idnetifier': serviceID,
        'eventType': eventType,
        'eventName': eventName,
        'eventDesc': eventDesc
    }
    collection.update(doc, doc, upsert=True)





