#!/usr/bin/env python3.8
import subprocess
import os
import json

FILE = '/sdcard/appd/appd.json'

class Appd():

  def __init__(self):
    self.started = False

    if os.path.exists(FILE):
      with open(FILE) as f:
        self.app_data = json.load(f)
    else:
      self.app_data = None

  def update(self, started):
    if self.app_data is not None:
      if started:
        if not self.started:
          self.started = True
          self.onroad()
      else:
        if self.started:
          self.started = False
          self.offroad()

  def onroad(self):
    for app in self.app_data:
      if not self.installed(app['app']) and os.path.exists(app['apk']):
        self.system("pm install -r %s" % app['apk'])
      for cmd in app['onroad_cmd']:
        self.system(cmd)

  def offroad(self):
    for app in self.app_data:
      if self.installed(app['app']):
        for cmd in app['offroad_cmd']:
          self.system(cmd)

  def installed(self, app_name):
    try:
      result = subprocess.check_output(["dumpsys", "package", app_name, "|", "grep", "versionName"], encoding='utf8')
      if len(result) > 12:
        return True
    except:
      pass
    return False

  def system(self, cmd):
    try:
      subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except:
      pass