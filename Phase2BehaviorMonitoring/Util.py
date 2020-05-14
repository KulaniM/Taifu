import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import hashlib
import os
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue
from scrapy_selenium import SeleniumRequest
from scrapy.http.cookies import CookieJar
#from ServiceWebScraping.ActionMonitoring.tatester.tatester.spiders.ActionClientAuthentication import authentication
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy_splash import SplashRequest, SplashFormRequest,SlotPolicy
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from pymongo import MongoClient
import timeit
# from threading import Thread
import time
# # # api-endpoint
# # URL = "https://buffalo-android.ifttt.com/grizzly/me/diy/services/" + service_identifier
# #
# # sending get request and saving the response as response object
# token = 'c2436a9ef37d65910c1c05f6d137dbb7d79260d4' #  #1b004674987164ecf6ed87c30146aa90b4c21024
# header = {'Authorization': 'Token token="' + token + '"'}
# post_header = {'Authorization': 'Token token="' + token + '"', 'Content-Type':'application/json; charset=utf-8'}
# # r = requests.get(URL, headers=header)
# # js_dict = r.json()
#
# #////////// Setup Database ///////////////
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="root",
#   database="ta_tester"
# )
# mycursor = mydb.cursor()

# #///////////End database setup //////////////
#
#
# URL_for_trigger_data = "https://buffalo-android.ifttt.com/grizzly/me/services/diy/applets/106462720d"
# r = requests.get(URL_for_trigger_data, headers=header)
# js_dict = r.json()
# pprint(js_dict)
#
#
#
#
############################################## DATABASE CONNECTION #####################################################
uri = 'mongodb://127.0.0.1:27017'
client = MongoClient(uri)
db = client['services']
collection = db.get_collection('authdetails')
all_auth_details = collection.find({})
#######################
x = ['go', 'android_device', 'narro', 'diigo', 'google_docs', 'dropbox', 'wordpress', 'tumblr', 'office_365_calendar', 'pocket', 'bitly', 'google_calendar', 'amazonclouddrive', 'google_sheets', 'google_drive', 'cisco_spark', 'telegram', 'coqon', 'google_contacts', 'office_365_contacts', 'onedrive', 'particle', 'strava', 'email', 'maker_webhooks', 'github', 'fitbit', 'office_365_mail', 'deezer', 'musixmatch', 'ios_calendar', 'soundcloud', 'spotify', 'newsblur', 'ios_reminders', 'ios_photos', 'evernote', 'flickr', 'sms', 'stockimo', 'twitter', 'beeminder', 'toodledo', 'reddit', 'sina_weibo', 'todoist']

# for auth in collection.find({'is_action_service': True, 'connected': True}):
#
#     if auth['service_idnetifier'] in x:
#         print(auth['service_idnetifier'])
#         # print(auth['loginurl'])
#         # print(auth['domains'])
#         # print(auth['username'])
#         # print(auth['password'])
#         if auth['service_idnetifier'] == 'email':
#             collection.update({'_id': auth['_id']},
#                               {'$set': {
#                                   'domains': 'mail.googler.com', 'loginurl': auth['loginurl'], 'username': auth['username'], 'password': auth['password'] }})  #

#x = ['go', 'android_device', 'narro', 'diigo', 'google_docs', 'dropbox', 'wordpress', 'tumblr', 'office_365_calendar', 'pocket', 'bitly', 'google_calendar', 'amazonclouddrive', 'google_sheets', 'google_drive', 'cisco_spark', 'telegram', 'coqon', 'google_contacts', 'office_365_contacts', 'onedrive', 'particle', 'strava', 'email', 'maker_webhooks', 'github', 'fitbit', 'office_365_mail', 'deezer', 'musixmatch', 'ios_calendar', 'soundcloud', 'spotify', 'newsblur', 'ios_reminders', 'ios_photos', 'evernote', 'flickr', 'sms', 'stockimo', 'twitter', 'beeminder', 'toodledo', 'reddit', 'sina_weibo', 'todoist']
#print(x.__len__())
dbClient = client['applets']
appletcollection = dbClient.get_collection('appletcollection12')
action_service_list = []
for applet in appletcollection.find({}):
    action_service_list.append(applet['action_service'])
print(action_service_list)
print(action_service_list.__len__())

y = ['pocket', 'office_365_calendar', 'cisco_spark', 'email', 'musixmatch', 'flickr', 'reddit', 'blogger', 'diigo', 'narro', 'google_calendar', 'amazonclouddrive', 'google_docs', 'google_drive', 'google_sheets', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'office_365_mail', 'fitbit', 'strava', 'android_device', 'ios_calendar', 'deezer', 'spotify', 'evernote', 'sms', 'ios_photos', 'stockimo', 'twitter', 'todoist']
yy = ['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'google_docs', 'google_drive', 'google_sheets', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'fitbit', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist']
yyy=['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'dropbox', 'google_docs', 'google_drive', 'google_sheets', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'fitbit', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist', 'toodledo']
yyyy= ['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'google_docs', 'google_drive', 'google_sheets', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'fitbit', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist', 'toodledo']
yyyyy=['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'dropbox', 'google_docs', 'google_drive', 'google_sheets', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'fitbit', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist', 'toodledo']
yyyyyy=['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'dropbox', 'google_docs', 'google_drive', 'google_sheets', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist', 'toodledo']
y7 = ['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'dropbox', 'google_docs', 'google_drive', 'google_sheets', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'fitbit', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist', 'toodledo']
y8 =['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'dropbox', 'google_docs', 'google_drive', 'google_sheets', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist', 'toodledo']
y12 = ['blogger', 'diigo', 'narro', 'pocket', 'google_calendar', 'office_365_calendar', 'amazonclouddrive', 'dropbox', 'google_docs', 'google_drive', 'google_sheets', 'onedrive', 'cisco_spark', 'telegram', 'google_contacts', 'office_365_contacts', 'github', 'particle', 'email', 'office_365_mail', 'fitbit', 'strava', 'android_device', 'ios_calendar', 'deezer', 'musixmatch', 'spotify', 'evernote', 'sms', 'flickr', 'ios_photos', 'stockimo', 'reddit', 'twitter', 'todoist', 'toodledo']
dbClient = client['iftttmonitor12']
appletcollection = dbClient.get_collection('succeed')
action_service_list = []
for applet in appletcollection.find({}):
    try:
        action_service_list.append(applet['action_data']['action_service'])
    except KeyError:
        print('no key')
print(action_service_list)
print(action_service_list.__len__())