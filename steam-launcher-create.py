#!/usr/bin/python3
import vdf
import binascii
import glob
import os, sys
from os.path import exists
from stat import *
parent_dir = "Steam Controller Configs"
IS_STEAM_DIR = 0
IS_FLAT_DIR = 1

def get_latest(dirLook, dirtype):
    x = []
    y = []
    for f in os.scandir(dirLook):
        if f.is_dir():
            if (dirtype == IS_FLAT_DIR):
               filepath=os.path.join(dirLook, f)
            else:
               filepath=os.path.join(dirLook, f)
            if os.path.isdir(filepath):
               y.append(os.path.getmtime(filepath))
               y.append(filepath)
               x.append(y)
            y=[]
    timefiles = sorted(x, reverse=True)
    return timefiles[0][1]

def get_appid(data):
   appid = binascii.crc32(data.encode('utf8')) | 0x80000000
   return appid

def get_bigappid(appid):
   bigpic_appid = (appid <<32) | 0x02000000

def make_controller_mappings(mappath, mapsourcepath):
   try:
      os.makedirs(mappath)
   except FileExistsError:
      print("Controller map directory already exists.")
   
   for item in os.scandir(mapsourcepath):
      try:
         os.symlink(os.path.join(mapsourcepath, item.name), os.path.join(mappath, item.name))
      except FileExistsError:
         print("Controller map file already exists.")

def make_app_artwork(artwork_number, artwork_appid, flatdir, steamdir):
      trest = steamdir + "grid"
      if not exists(steamdir + "grid") or not os.path.isdir(steamdir + 'grid'):
         os.makedirs(steamdir + 'grid')

      # p is designated to grids for some reason
      artwork_sections= ["", "_logo", "p", "_hero"]
      file_types=[".jpg", ".png"]
      for i in artwork_sections:
         for t in file_types:
            if (glob.glob(flatdir + str(artwork_number) + i + t)):
               try:
                  os.symlink(flatdir + str(artwork_number) + i + t,
                           steamdir + "grid/" + str(artwork_appid) + i + t)
               except FileNotFoundError:
                  print (str(artwork_number) + i + t + " not found")
               except FileExistsError:
                  print (str(artwork_number) + i + t + " already exits")

def main():
   steamuserdir=get_latest(os.environ['HOME'] + '/.steam/steam/userdata/', IS_STEAM_DIR) + '/config/'
   userid=os.path.basename(os.path.dirname(steamuserdir))
   flatdir=get_latest(os.environ['HOME'] + '/.local/share/flatpak/app/', IS_FLAT_DIR) + '/current/active/files/share/steamlauncher/'
   if not exists(flatdir):
      print ("No launcher data directory found")
      return
   try:
      t = vdf.load(open(flatdir + 'launcher.vdf'))
   except FileNotFoundError:
      print ("No launcher file found")
      return
   
   if (os.path.isfile(steamuserdir + 'shortcuts.vdf') == False):
      open(steamuserdir + 'shortcuts.vdf', mode='x')
   d = vdf.binary_load(open(steamuserdir + 'shortcuts.vdf', mode='br'))
   if ('shortcuts' not in d):
      d = {'shortcuts': {}}

   for idx, item in enumerate(t.values()):
      print (str(idx), '\n')
      item['appid']=get_appid(''.join([item['Exe'], item['AppName']]))
      if exists(flatdir+str(idx)+'_icon.ico'):
         item['icon']=flatdir+str(idx)+'_icon.ico'
      if exists(flatdir+str(idx)+'_icon.png'):
         item['icon']=flatdir+str(idx)+'_icon.png'
      d['shortcuts'][str(len(d['shortcuts']))]=item
      print ("Created launcher" + " for " + item['AppName'])
      make_app_artwork(idx, item['appid'], flatdir, steamuserdir)
      print ("Applied launcher artwork" + " for " + item['AppName'])
      map_path=os.environ['HOME'] + '/.steam/steam/steamapps/common/Steam Controller Configs/' + userid + '/config/' + item['AppName']
      #make_controller_mappings(map_path, flatdir + '/controller_configs')

   b=vdf.binary_dump(d, open(steamuserdir + 'shortcuts.vdf', mode='bw'))

if __name__ == "__main__":
   main();