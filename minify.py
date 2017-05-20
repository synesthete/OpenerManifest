import sys
import subprocess
import re
import os
import shutil
import json
from collections import OrderedDict # http://stackoverflow.com/a/10982037

if len(sys.argv) < 2:
    print "No path specified"
    sys.exit()
    
path = sys.argv[1]

# Use the --prefer-script-v1 flag when use need the v2 format (includes only 'script', not 'script2')
preferredScriptName = 'script2'
stripNewField = False
if len(sys.argv) > 2:
    if sys.argv[2] == '--prefer-script-v1':
        preferredScriptName = 'script'
    elif sys.argv[2] == '--strip-new':
        stripNewField = True

data = json.loads(open(path).read(), object_pairs_hook=OrderedDict) # http://stackoverflow.com/a/6921760

# Strip unneeded keys from apps
appKeysToKeep = ["identifier", "displayName", "storeIdentifier", "scheme", "platform", "iconURL", "country"]
if not stripNewField:
    appKeysToKeep.append("new");
for appIndex,app in enumerate(data['apps']):
	appKeys = app.keys()
	for keyIndex,key in enumerate(appKeys):
		if not key in appKeysToKeep:
			print "Removing " + key + " from " + app["identifier"]
			app.pop(key, None)
			
# Strip unneeded keys from actions
for actionIndex,action in enumerate(data['actions']):
    actionKeys = action.keys()
    for keyIndex,key in enumerate(actionKeys):
        if not key in ["title", "regex", "includeHeaders", "formats"]:
            # print "Removing " + key + " from action"
            action.pop(key, None)

    # Strip unneeded keys from formats
    for format in action['formats']:
        formatKeys = format.keys()
        for keyIndex,key in enumerate(formatKeys):
            if not key in ["appIdentifier", "format", "script", "script2"]:
                # print "Removing " + key + " from format"
                format.pop(key, None)

        # Ensure only necessary script is included
        if not 'format' in formatKeys:
            if preferredScriptName == 'script2' and 'script2' in formatKeys:
                # print 'Removing v1 script from ' + format['appIdentifier']
                format.pop('script', None)
            elif preferredScriptName == 'script':
                if 'script' in formatKeys:
                    # print 'Removing v2 script from ' + format['appIdentifier']
                    format.pop('script2', None)
                else:
                    # print 'Removing format ' + format['appIdentifier'] + ' from ' + action['title']
                    action['formats'].remove(format)

    if len(action['formats']) == 0:
        # print 'Removing action ' + action['title']
        data['actions'].remove(action)

# Strip unneeded keys from browsers
browserKeysToKeep = ["identifier", "displayName", "storeIdentifier", "scheme", "platform", "iconURL", "regex", "format", "script", "script2"]
if not stripNewField:
    browserKeysToKeep.append("new");
if 'browsers' in data:
	for browserIndex,browser in enumerate(data['browsers']):
		browserKeys = browser.keys()
		for keyIndex,key in enumerate(browserKeys):
			if not key in browserKeysToKeep:
                # print "Removing " + key + " from browser"
				browser.pop(key, None)
    
        # Ensure only necessary script is included
		if not 'format' in browserKeys:
			if preferredScriptName == 'script2' and 'script2' in browserKeys:
                # print 'Removing v1 script from ' + browser['identifier']
				browser.pop('script', None)
			elif preferredScriptName == 'script':
				if 'script' in browserKeys:
                    # print 'Removing v2 script from ' + browser['identifier']
					browser.pop('script2', None)
				else:
                    # print 'Removing browser ' + browser['identifier']
					data['browsers'].remove(browser)

				
data = json.dumps(data, separators=(',',':'))
open(path.replace('.json', '-minified.json'), 'w').write(data)

# if v3
#     pop script if both exist
# else if v2
#     pop script2 if both exist
#     pop format if script1 doesn't exist