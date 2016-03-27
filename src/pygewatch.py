#!/usr/bin/env python

""" pygewatch - Python Page Watcher
Look at web-pages and check if they have changes since last check.
Keeps a .json file with sha224 (hash) values, and change is detected by comparing the sha224 values."""

import json
from datetime import datetime
import urllib2
import hashlib

import ecmail

__author__ = "Martin Hvidberg"
__email__ = "martin@hvidberg.net"
__repo__ = "https://MartinHvidberg@bitbucket.org/MartinHvidberg/pygewatch"

# *** Read json file
fil_json = open('pygewatch.json')
jsn_config = json.load(fil_json)
fil_json.close()
bol_json_chenged = False

# *** Process
str_news = "" 
for urli in jsn_config["urls"]:
    str_url = urli["url"]
    str_sum_old = urli["sum"]
    print str_url + "\n\told\t" + str_sum_old
    str_html = None
    try:
        str_html = urllib2.urlopen(str_url).read()
    except:
        print "Problem accessing url: "+str_url
    if str_html:
        str_sum_new = hashlib.sha224(str_html).hexdigest()
        bol_unchanged = str_sum_old == str_sum_new
        print "\tnew\t"+str_sum_new + " " + str(bol_unchanged)
        
        # ** If a difference is found ...
        if not bol_unchanged:
            str_observed_time = str(datetime.now()).split('.')[0]
            str_change = "\n"+str_observed_time+" Changed "+str_url
            # * Write to log
            with open(jsn_config["logfile"], 'a') as file:
                file.write(str_change)
            # * Update json info
            urli['sum'] = str_sum_new
            urli['date'] = str_observed_time
            bol_json_chenged = True
            # * Add to News
            str_news += str_change

# *** Write updated json file
if bol_json_chenged:
    fil_json = open('pygewatch.json', 'w')
    fil_json.write(json.dumps(jsn_config))
    fil_json.close()
    
# *** Send e-mail
if str_news != "": # If there are any news, then report them ...
    ecmail.email_simple("New PygeWatch report", str_news, 'martin@hvidberg.net')
