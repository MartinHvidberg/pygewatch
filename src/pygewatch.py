#!/usr/bin/env python

""" pygewatch - Python Page Watcher
Look at web-pages and check if they have changes since last check.
Keeps a .json file with sha224 (hash) values, and change is detected by comparing the sha224 values."""

import json
from datetime import datetime
import urllib2
import hashlib
import difflib

import ecmail

__author__ = "Martin Hvidberg"
__email__ = "martin@hvidberg.net"
__repo__ = "https://MartinHvidberg@bitbucket.org/MartinHvidberg/pygewatch"

def resave_local(str_html, str_local_filename):
    fil_local = open(str_local_filename, 'w')
    fil_local.write(str_html)
    fil_local.close()

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
    str_loc_fil = urli["local_file"]
    print str_url + "\n\told\t" + str_sum_old
    str_html = None # Empty the variable between loops
    try:
        str_html = urllib2.urlopen(str_url).read()
    except:
        print "Problem accessing url: "+str_url
    if str_html: # if the url was read successfully
        str_sum_new = hashlib.sha224(str_html).hexdigest()
        bol_unchanged = str_sum_old == str_sum_new
        print "\tnew\t"+str_sum_new + " " + str(bol_unchanged)

        # ** If a 'hash' difference is found ...
        if not bol_unchanged:
            # ** If a saved local file exist, then do detailed comparison
            if str_loc_fil != "":
                html_local = None
                try:
                    fil_local = open(str_loc_fil)
                    html_local = fil_local.read()
                except:
                    print "\tProblem opening local file: "+str_loc_fil
                if html_local:
                    print "\tComparing to saved file ..."
                    expected=html_local.splitlines(1)
                    actual=str_html.splitlines(1)
                    diff=difflib.unified_diff(expected, actual)
                    str_diff = ''.join(diff)
                    if len(str_diff) > 0:
                        print "\tDiff:\n"+str_diff
                    else:
                        # This is only suppose to happen during debugging ...
                        print "\tThough the 'hash' was different, the html seems identical..."
                        bol_unchanged = True
                else:
                    print "\tTrying to save new copy..."
                    try:
                        resave_local(str_html, str_loc_fil)
                        print "\tSaved new copy :-)"
                    except:
                        print "\tProblem saving new local file: "+str_loc_fil

        # ** If there are still a valid diff, after all analysis
        if not bol_unchanged:
            str_observed_time = str(datetime.now()).split('.')[0]
            str_change = "\n"+str_observed_time+" Changed "+str_url
            # * Write to log
            with open(jsn_config["logfile"], 'a') as file:
                file.write(str_change)
            # * Update json info and local file
            urli['sum'] = str_sum_new
            urli['date'] = str_observed_time
            resave_local(str_html, str_loc_fil)
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

# *** Clean and close


with open("run.log", "a") as fil_run_log:
    fil_run_log.write("Run successfully: %s\n" % datetime.now().isoformat().split('.')[0] )
    