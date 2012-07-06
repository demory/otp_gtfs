import os, subprocess, json

datadir = os.path.join(os.getcwd(), 'data')
for fname in os.listdir(datadir):
    
    zippath = os.path.join(datadir, fname, "feed.zip")
    if(os.path.exists(zippath)):
        print zippath
        
        # unzip gtfs feed
        
        unzippath = os.path.join(datadir, fname, "feed")
        if(os.path.exists(unzippath)):
            subprocess.call(["rm","-rf",unzippath])
        
        subprocess.call(["unzip", "-d", unzippath, zippath])
        
