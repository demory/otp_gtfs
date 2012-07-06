# downloads all North American GTFS feeds into "data" directory

import json, os, urllib2, sys
from pprint import pprint
        
json_file=open('exchange.json')
data = json.load(json_file)

good = 0
nonzip = 0
broken = 0
total = 0
for entry in data['data']:
    if(entry['country'] == "United States" or entry['country'] == "Canada"):
        total += 1

        entrydir = os.path.join(os.getcwd(), 'data', entry['dataexchange_id'])
        os.makedirs(entrydir)
        f = open(os.path.join(entrydir,'info.json'), 'w')
        f.write(json.dumps(entry) + "\n")
        f.close()

        print "checking feed for %s from %s" % (entry['name'], entry['feed_baseurl'])
        try:
            url = urllib2.urlopen(entry['feed_baseurl'])
            type = url.info()['Content-Type']
            if(type == 'application/x-zip-compressed' or type == 'application/zip'):
                print " - downloading.."
                feedfile = open(os.path.join(entrydir,'feed.zip'), 'w')
                feedfile.write(url.read())
                feedfile.close()
                good += 1
            else:
                nonzip += 1
        except:
            print " - Error reading URL"
            broken += 1
        
        print " "

print "%s feeds downloaded" % good
print "%s links to non-zip files" % nonzip
print "%s broken links" % broken
print "%s total feeds" % total
    
json_file.close()


