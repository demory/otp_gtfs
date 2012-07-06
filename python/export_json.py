import json, os

#from json import encoder
#encoder.FLOAT_REPR = lambda o: format(o, '.5f')

datadir = os.path.join(os.getcwd(), 'data')

alldata = [ ]
for fname in os.listdir(datadir):
    #zippath = os.path.join(datadir, fname, "feed.zip")
    polypath = os.path.join(datadir, fname, 'poly.json')
    if(os.path.exists(polypath)):

        infojsonfile = open(os.path.join(datadir, fname, 'info.json'))
        infojsondata = json.load(infojsonfile)

        geojsonfile = open(polypath)
        geojsondata = json.load(geojsonfile)
        
        feeddata = {'info': infojsondata, 'geom': geojsondata}
        alldata.append(feeddata)
        
        infojsonfile.close()
        geojsonfile.close()

f = open(os.path.join(os.getcwd(),'all.json'), 'w')
f.write(json.dumps(alldata) + "\n")
f.close()        
