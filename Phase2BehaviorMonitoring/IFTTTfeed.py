import requests
from pprint import pprint
import itertools
import json
import urllib.parse
from pymongo import MongoClient
import timeit
#from BehaviorMonitoring_NoiseTemplates_Gen.tatester.tatester.spiders.MonitoringJavaScriptAction import monitoring
# facebook 3
# dropbox  4
# onedrive 5 # fitbit 6
URL_for_apple_execution_history = "https://buffalo-android.ifttt.com/grizzly/me/feed/"
token = '0dfb5edac5e2201a9ece7b3908dcfd04d57522b6' #  #1b004674987164ecf6ed87c30146aa90b4c21024 #0dfb5edac5e2201a9ece7b3908dcfd04d57522b6 #c2436a9ef37d65910c1c05f6d137dbb7d79260d4
header = {'Authorization': 'Token token="' + token + '"'}
post_header = {'Authorization': 'Token token="' + token + '"', 'Content-Type':'application/json; charset=utf-8'}
########################################################################################################################
############################################## DATABASE CONNECTION #####################################################
uri = 'mongodb://127.0.0.1:27017'
client = MongoClient(uri)
###############################################
db = client['iftttmonitor14']
scollection = db.get_collection('succeed')
fcollection = db.get_collection('failed')
###############################################
dbClient = client['applets']
appletcollection = dbClient.get_collection('appletcollection14')
###############################################
########################################################################################################################
def updateAppletExecutionHistory(feed, successCol, failedCol):
    succeed = []
    for item in feed:
        results = {}
        context_text = None
        applet_result = None
        applet_id = None
        trigger_data = None
        applet_status_data = None
        location = None
        for ik, iv in item.items():
            if ik == 'grizzly':
                trigger_data = iv
                for ak, av in iv.items():
                    if ak == 'applet_id':
                        applet_id = av
                    if ak == 'content_text':
                        context_text = av
            if ik == 'item_type':
                applet_result = iv
            if ik == 'location':
                location = iv
            if ik == 'ife':
                applet_status_data = iv

        results['applet_id'] = applet_id
        results['context_text'] = context_text
        results['trigger_data'] = trigger_data
        results['applet_status_data'] = applet_status_data
        results['location'] = location
        if applet_result == 'success':
            data = successCol.find({'applet_id': applet_id,'context_text':context_text})
            if data.count() > 0:
                for record in data:
                    if not record['monitored']:
                        results['monitored'] = False
                        results['analyzed'] = False  # scrapped?
                        results['action_data'] = {}
                        results['applet_knowledge'] = {}
                        succeed.append(applet_id)
                        successCol.update(record, results, upsert=True)
            else:
                results['monitored'] = False
                results['analyzed'] = False  # scrapped?
                results['action_data'] = {}
                results['applet_knowledge'] = {}
                succeed.append(applet_id)
                successCol.update(results, results, upsert=True)
        elif applet_result == 'error':
            failedCol.update(results, results, upsert=True)
    return succeed

########################################################################################################################
r = requests.get(URL_for_apple_execution_history, headers=header)
js_dict = r.json()
feed = js_dict['feed']
pprint(feed)
appletsToMonitor = updateAppletExecutionHistory(feed,scollection,fcollection)
##################################################################################
## 1)
##################################################################################
actions_to_monitor = []
#### Next find the action services to monitor by quering the applets database
for appletID in appletsToMonitor:
    applet_details = appletcollection.find({'applet_id': appletID})
    for adetaisl in applet_details:
        adata = {}
        adata['applet'] = appletID
        adata['action_service'] = adetaisl['action_service']
        adata['action'] = adetaisl['action']
        adata['action_desc'] = adetaisl['action_desc']
        actions_to_monitor.append(adata)
print(actions_to_monitor)
##################################################################################
##################################################################################
## 2) IFT 1 didnt work due to the removal of feed by the server
##################################################################################
# actions_to_monitor2 = []
# for succApplets in scollection.find({}):
#     applet_details = appletcollection.find({'applet_id': succApplets['applet_id']})
#     for adetaisl in applet_details:
#         adata = {}
#         adata['applet'] =  succApplets['applet_id']
#         adata['action_service'] = adetaisl['action_service']
#         adata['action'] = adetaisl['action']
#         adata['action_desc'] = adetaisl['action_desc']
#         actions_to_monitor2.append(adata)
# print(actions_to_monitor2)

##################################################################################
##################################################################################
# ### Next call the action monitoring module
# headless_can_use = []
# list_need_headless_false = []
# headlessFalse = ['dropbox','pocket','office_365_mail','office_365_contacts','deezer','twitter','evernote','wordpress','amazonclouddrive','musixmatch','cisco_spark','email']
#
# for action in actions_to_monitor:
#     if action in headlessFalse:
#         list_need_headless_false.append(action['action_service'])
#     else:
#         headless_can_use.append(action['action_service'])
# print('headless_can_use')
# print(headless_can_use)
####################################################################################
# ### Next call the action monitoring module
successList = ['diigo', 'google_docs', 'cisco_spark', 'fitbit', 'narro', 'google_calendar', 'wordpress', 'pocket', 'email', 'particle', 'strava', 'google_sheets', 'twitter']

for action in actions_to_monitor:
    print(action)
    action_service = action['action_service']
    action_name = action['action']
    action_desc = action['action_desc']
    appletID = action['applet']

    default_start_no = 1
    default_end_no = 2
    action_services_to_monitor = [action_service]
    #monitoring(default_start_no, default_end_no, action_services_to_monitor)
    print('monitoring done: ' + str(action_service))

    ######## after monitored update iftttmonitor db
    data = scollection.find({'applet_id': appletID})
    print(data)
    if data.count() > 0:
        for record in data:
            print('here')
            # oldrecord = record
            # record['monitored'] = True
            ### THIS STEP SHOULD BE SUCCESSFULL FOR THE ANALYSEDMONITORED PAGES TO BE CONINTIED...
            scollection.update({'_id': record['_id']},  {'$set': {"monitored":True, 'action_data': {'action_service':action_service}}})
############
# first crawling of moniotring just after the
############
