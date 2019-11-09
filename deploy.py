#!/usr/bin/python
import os
import time
from ftplib import FTP


def senddir(path,dest,ftp):
  for root, dirs, files in os.walk(path):
    for file in files:
      source_filename = os.path.join(root, file)
      dest_filename = dest + source_filename.replace(path,'')
      dest_dir = os.path.dirname( dest_filename )
      
      list = dest_dir.split('/')
      
      ftp.cwd( "/" )
      partial_dir = ""
      for part in list:
        partial_dir += "/" + part
        partial_dir = partial_dir.replace('//','/')        
        if part != "" and not (part in ftp.nlst() ):      
          ftp.mkd( partial_dir )
          print "Created " + partial_dir + " on remote server"        
        ftp.cwd( partial_dir )
      
      ftp.cwd( "/" )
      
      ftp.storlines("STOR " + dest_filename, open(source_filename,"r"))
      print "Stored " + dest_filename  + " on remote server"
      

timestamp = str(int( time.time()))

# local directory
local_dir = "/home/test/work-repo"

# FTP server connection strings      
ftp_host = "ftp.example.com"
ftp_username = "user@example.com"
ftp_password = "password"

# remote server paths
dest_dir = "/home/production/.deploy-" + timestamp
backup_dir = "/home/production/archive/www-" + timestamp
production_dir = "/home/production/www"
  
if __name__ == '__main__':  
  
  print "Connecting to FTP host " + ftp_host
  ftp = FTP( ftp_host , ftp_username , ftp_password )
  
  print "Starting directory transfer of " + local_dir
  senddir( local_dir , dest_dir, ftp)
  
  print "Renaming " + production_dir + " to " + backup_dir
  ftp.rename( production_dir , backup_dir )
  
  print "Renaming " + dest_dir + " to " + production_dir
  ftp.rename( dest_dir , production_dir )
  
  print "Transfer complete"