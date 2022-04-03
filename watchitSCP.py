#!/usr/bin/python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import json
import time

from paramiko import SSHClient
from scp import SCPClient

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        ## instantiation of the ssh client
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect('hostname',username='username',password='password')

        ## passing SSHClient Transport arguement to SCP Client
        scp = SCPClient(ssh.get_transport())


        for filename in os.listdir(folder_to_track):
            src = folder_to_track + "/" + filename
            ## This is for copying the objects Locallly
            #  new_destination = folder_destination + "/" + filename
            #  os.rename(src, new_destination)

            ## This is for copying the objects Remotely
            new_destination = folder_destination + "/" + filename
            scp.put(src, new_destination)

## For Copying the objects remotely

folder_to_track = "Folder to track path"
folder_destination = "Destination Path"
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
