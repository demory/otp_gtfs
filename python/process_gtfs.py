import os, subprocess, json

datadir = os.path.join(os.getcwd(), 'data')
for fname in os.listdir(datadir):
    
    feedpath = os.path.join(datadir, fname, 'feed')
    if(os.path.exists(feedpath)):
        print feedpath
       
        # generate polygon file
        
        print " - generating polygon"
        
        stopsdir = os.path.join(datadir, fname, "stops")
        if(os.path.exists(stopsdir)):
            subprocess.call(["rm","-rf",stopsdir])
        
        os.makedirs(stopsdir)
        subprocess.call(["cp", os.path.join(feedpath, "stops.txt"), stopsdir])
        polyfile = os.path.join(datadir, fname, "poly.json")        
        subprocess.call(["java", "-classpath", "lib/osmtools/osmtools.jar", "osmtools.PolyGenJSON", stopsdir, polyfile])
        
        
        # determine calandar status and append to info.json
        
        print " - determining calendar status"
        
        infojsonfile = open(os.path.join(datadir, fname, 'info.json'))
        infojsondata = json.load(infojsonfile)
        infojsonfile.close()
        
        #if('days_to_expiration' in infojsondata):
        #    continue

        #print feedpath       
        
        result = subprocess.Popen(["java", "-jar", 'java/gtfsmetrics/target/gtfsmetrics.jar', feedpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        stdout = result.stdout.read()
        
        #print "stdout: "+stdout

        status = int(stdout)
        infojsondata['days_to_expiration'] = int(stdout)
        #print infojsondata

        if(status <= 60 and status >=0):
            print "expires soon"
        if(status < 0):
            print "expired"
         
        infojsonfile = open(os.path.join(datadir, fname, 'info.json'), "w")
        infojsonfile.write(json.dumps(infojsondata) + "\n")
        infojsonfile.close()            
        
        
