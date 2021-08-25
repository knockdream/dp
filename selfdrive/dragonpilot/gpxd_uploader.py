import requests
from xml.etree import ElementTree
from selfdrive.loggerd.xattr_cache import getxattr, setxattr
import os
import glob

UPLOAD_ATTR_NAME = 'user.upload'
UPLOAD_ATTR_VALUE = b'1'
LOG_PATH = '/data/media/0/gpx_logs/'

# CLIENT_ID = 'HQqln0zhuGhrNcIan3t9wnD2PLhxJpiMgU9pU6ShRyg'
# CLIENT_SECRET = 'PiTTk4p4LuYyRkBrDVEvxK-9hASzWS2Dm4wEip8wNyY'

# AUTH_URL = 'https://www.openstreetmap.org/oauth2/authorize'
# TOKEN_URL = 'https://www.openstreetmap.org/oauth2/token'
# REDIRECT_URL = 'urn:ietf:wg:oauth:2.0:oob'
#
# auth = AUTH_URL + "?response_type=code&client_id=" + CLIENT_ID + "&redirect_uri=" + REDIRECT_URL + "&scope=write_gpx"
# token_data = {
#     'grant_type': 'authorization_code',
#     'code': 'Pe7FyB_CP7WqDSf87UUCy-a6oszMYMI0NHfTEPjI0GA',
#     'redirect_uri': REDIRECT_URL
# }
#
# def auth():
#   print(auth) # open in url, then change the code in token_data
#   r = requests.post(TOKEN_URL, data=token_data, verify=False, allow_redirects=False, auth=(CLIENT_ID, CLIENT_SECRET))
#   print(r.json())

API_HEADER = {'Authorization': 'Bearer hP-9KYISopPxfMMyfaER1jOuyRtTCK4RPjSaZiwyWA8'}
VERSION_URL = 'https://api.openstreetmap.org/api/versions'
UPLOAD_URL = 'https://api.openstreetmap.org/api/0.6/gpx/create'
ROUTE_META_URL = 'https://api.openstreetmap.org/api/0.6/gpx/%s/details'


def get_is_uploaded(filename):
  return getxattr(filename, UPLOAD_ATTR_NAME) is not None

def set_is_uploaded(filename):
  setxattr(filename, UPLOAD_ATTR_NAME, UPLOAD_ATTR_VALUE)

def get_files():
  return sorted( filter( os.path.isfile, glob.glob(LOG_PATH + '*') ) )

def get_files_to_be_uploaded():
  files = get_files()
  files_to_be_uploaded = []
  for file in files:
    if not get_is_uploaded(file):
      files_to_be_uploaded.append(file)
  return files_to_be_uploaded

def is_online():
  r = requests.get(VERSION_URL, headers=API_HEADER)
  return r.status_code == 200

def get_uploaded_route(route_id=3785992):
  route = ROUTE_META_URL % route_id
  print(route)
  r = requests.get(route, headers=API_HEADER)
  print(r.content)


def do_upload(filename):
  fn = os.path.basename(filename)
  data = {
    'description': 'Routes from dragonpilot.',
    'public': 1,
    'visibility': 'public'
  }
  files = {
    "file": (fn, open(filename, 'rb'))
  }
  r = requests.post(UPLOAD_URL, files=files, data=data, headers=API_HEADER)
  return r.status_code == 200
  print(r.status_code)
  print(r.content)
  exit()


def main():
  get_uploaded_route()
  exit()
  while True:
    files = get_files_to_be_uploaded()
    if len(files) > 0:
      for file in files:
        do_upload(file)

    else:
      time.sleep(60)


  # print(files)


  # if is_online():
  #   files = get_files()
  #   for file in files:
  #     if not get_is_uploaded(file):
  # else:


  # r1 = requests.get(VERSION_URL, headers=API_HEADER)
  # if r1.status_code == 200:
  #   data = {
  #     'file': open('/sdcard/gpxd_logs/tmp/', 'r'),
  #     'description': 'Routes from dragonpilot.',
  #     'public': 1,
  #     'visibility': 'public'
  #   }
  #   r2 = requests.post(UPLOAD_URL, data=data)
  #   if r2.status_code == 200:
  #     # lets delete the file here.
  #     pass


  # xml = ElementTree.fromstring(r.content).getroot()
  # print(xml)




if __name__ == "__main__":
    main()
