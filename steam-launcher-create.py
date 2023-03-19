#!/usr/bin/python3
import vdf
import binascii
import os
import glob
parent_dir = "Steam Controller Configs"

def getappid(data):
   appid = binascii.crc32(data.encode('utf8')) | 0x80000000
   return appid

def getbigappid(appid):
   bigpic_appid = (appid <<32) | 0x02000000

def makeControllerMappings(map_path, map_name):
   try:
      os.makedirs(map_path)
   except FileExistsError:
      print("controller map directory already exists")
   try:
      os.symlink(os.getcwd() + '/FXAA234076FA.vdf', str(map_path) + "/" +  str(map_name))
   except FileExistsError:
      print("controller map file already exists")

def makeAppArtwork(artwork_number, artwork_appid):
      artwork_sections= ["logo", "grid", "hero", "icon"]
      file_types=[".jpg", ".png", ".ico"]
      for i in artwork_sections:
         for t in file_types:
            if (glob.glob(i + '_' + str(artwork_number) + t)):
               try:
                  os.symlink(i + "_" + str(artwork_number) + t,
                           str(artwork_appid) + "_" + i + t)
               except FileNotFoundError:
                  print (i + "_" + str(artwork_number) + t + " not found")
               except FileExistsError:
                  print (i + "_" + str(artwork_number) + t + " already exits")

if (os.path.isfile('shortcuts.vdf') == False):
   open('shortcuts.vdf', mode='x')

t = vdf.load(open('placeholder.vdf'))
d = vdf.binary_load(open('shortcuts.vdf', mode='br'))

if ('shortcuts' not in d):
   d = {'shortcuts': {}}

for idx, item in enumerate(t.values()):
   print (str(idx), '\n')
   item['appid']=getappid(''.join([item['Exe'], item['AppName']]))
   d['shortcuts'][str(len(d['shortcuts']))]=item
   makeAppArtwork(idx, item['appid'])
   map_path=os.path.join(parent_dir, str(item['appid']), "config", str(item['AppName']))
   makeControllerMappings(map_path, item['appid'])

b=vdf.binary_dump(d, open('shortcuts.vdf', mode='bw'))