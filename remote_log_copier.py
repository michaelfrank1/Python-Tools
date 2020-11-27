#!/usr/bin/bash

# Description: Script copies all files and directories from Poseidon to local laptop

# NOTE: (Ubuntu) Under "configurations" in "launch.json", set "sudo" to "True" so you
# don't have to keep logging in

import os
import paramiko
from scp import SCPClient
import shutil

def copyFiles():
  # Set default directory paths
  ip = ''
  home_dir = os.path.expanduser('~')
  local_path = ''

  # set ip address
  ip = input("Please enter robot's ip address: ")
  #ip = '10.0.0.239'

  # POSEIDON ROBOT DIRECTORY
  remote_path = '/home/robot/'

  # if os.name == 'nt':
  #   import win32api, win32con

    # Establish SSH connection
  ''' 
  To allow a connection without having to accept the host connection, we need to use this policy.
  '''
  policy = paramiko.client.AutoAddPolicy
  
  try:
    # create new directory
    new_dir = input("Destination log folder name? ")

    # set local_path variable
    local_path = home_dir + '/' + new_dir

    # create location to copy log files to
    os.mkdir(local_path)
    
  # if an exception occurs, then retry
  except(FileExistsError):
    try:
      # change to 'home' directory
      # os.chdir(home_dir)

      print("Directory already exists!")
      new_dir = input("Destination log folder name? ")

      # set local_path variable
      local_path = home_dir + '/' + new_dir
            
      # create location to copy log files to
      os.mkdir(local_path)

    # if another exception occurs, try a second time  
    except(FileExistsError):
      try:
        # change to 'home' directory
        os.chdir(home_dir)

        print("Directory already exists!")
        new_dir = input("Destination log folder name? ")

        # set local_path variable
        local_path = home_dir + '/' + new_dir

        # create location to copy log files to
        os.mkdir(local_path)

      # third time is the last time 
      except(FileExistsError):
        print("We exit on the 3rd try!! . . . Bye Bye!!")
        exit(0)

  # Making SSH2 connections with paramiko 
  with paramiko.SSHClient() as client:
    client.set_missing_host_key_policy(policy)
    try:
      # connect to Poseidon
      client.connect(ip, username='robot', password='#robot#', port=22)
      print("CONNECTION ESTABLISHED") 

      scp = SCPClient(client.get_transport())

      # copy directory from Poseidon to local machine
      print("Processing request . . . ")
      print("May take ~30 seconds or longer, depending on network speed and size of data.")
      scp.get(remote_path, local_path, recursive=True)

      # After copying the directory over to the local machine. Delete all files that start
      # with '.'
      roboPath = local_path + '/robot'
      roboPathFileList = os.listdir(local_path + '/robot')
      for f in roboPathFileList:
        if f.startswith('.'):
          try: 
            os.chdir(roboPath)
            localRoboPath = roboPath + '/' + f
            os.remove(localRoboPath)
          except OSError as err:
            shutil.rmtree(localRoboPath)
      
    except paramiko.ssh_exception.NoValidConnectionsError:
      print("Connection failed")

if __name__ == "__main__":
  copyFiles()
  print("COPY COMPLETED")

# CHOOSE WHETHER TO DELETE LOG FILES ON ROBOT IN ORDER TO MAKE SPACE . . . COMING SOON