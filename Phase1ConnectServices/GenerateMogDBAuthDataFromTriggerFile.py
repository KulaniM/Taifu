import xlrd
from pymongo import MongoClient

# Workbook location
loc = ('/home/kulani/Projects/ImpTATester/ServiceWebScraping/Phase1ConnectServices/authxls/Copy of Filtered Trigger Services.xlsx')

# Open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
print('No of records: '+str(sheet.nrows))
###########################################################################
uri = 'mongodb://127.0.0.1:27017'
client = MongoClient(uri)
db = client['services']
collection = db.get_collection('authdetails')
#collection.remove({})
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
    triggertype = sheet.cell_value(i, 2)
    loginURL = sheet.cell_value(i, 7)
    username = sheet.cell_value(i,3)
    password = sheet.cell_value(i,4)
    domains = sheet.cell_value(i,5)
    connected = False
    print(loginURL)
    # ###########
    # ###########
    # if serviceID == 'tumblr' or serviceID== 'weebly' or serviceID=='wordpress' or serviceID=='inoreader'  or serviceID=='pinboard'or serviceID=='buffer'or serviceID=='airpatrol'or serviceID=='chatwork'or serviceID=='cisco_spark':
    #     connected = False
    #if username and password:
    print('serviceID: ' + serviceID + 'username: ' + username + ' password: ' + password)
    print(collection.find({'service_idnetifier': serviceID}).count())
    if collection.find({'service_idnetifier': serviceID}).count()==0:
        doc = {
            'service_idnetifier': serviceID,
            'loginurl': loginURL,
            'username': username,
            'password': password,
            'domains': domains,
            'connected': connected,
            'is_trigger_service': True,
            'is_action_service': False
        }
        #collection.update(doc, doc, upsert=True)
    else:
        for service in collection.find({'service_idnetifier': serviceID}):
            print('')
            #collection.update({'_id': service['_id']}, {'$set': {'is_trigger_service': True, 'connected': False, 'trigger_type': triggertype}})
            if serviceID not in ['wordpress','fitbit'] :
                collection.update({'_id': service['_id']},
                              {'$set': {'loginurl':loginURL,'username': username,'password': password,'domains': domains}})






