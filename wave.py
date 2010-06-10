from waveapi import events
from waveapi import robot
from waveapi import appengine_robot_runner
import logging

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
import datetime
import simplejson

def OnWaveletSelfAdded(event, wavelet):
  """Invoked when the robot has been added."""
  import urllib
  logging.info("OnWaveletSelfAdded called")
  wavelet.reply("""
  Put robot:""" + wavelet.wave_id + """ in the title of the wave that you want this wave to be a robot for.
  Also add clstff#userobot@appspot.com the wave you want this to wave to be a robot for.
  """)

def OnBlipSubmitted(event, wavelet):
  logging.info("blip submitted")
  if wavelet.creator != "drewalex@googlewave.com":
    return false
  if event.blip != wavelet.root_blip:
    return false
    
  code = event.blip.text
  wavelet_id = wavelet.wave_id
  key_name = wavelet_id
  def txn():
    key = datastore.Key.from_path("wavelet", key_name)
    try:
      ent = datastore.Get(key)
    except datastore_errors.EntityNotFoundError:
      ent = datastore.Entity(kind="wavelet", name=key_name)
    ent['code'] = code
    datastore.Put(ent)
  datastore.RunInTransaction(txn)
  #query = datastore.Query("wavelets") you could do it this way
            

if __name__ == '__main__':
  myRobot = robot.Robot('gae-run', 
      image_url='http://a3.twimg.com/profile_images/250985893/twitter_pic_bigger.jpg',
      profile_url='http://clstff.appspot.com/')
  myRobot.register_handler(events.WaveletSelfAdded, OnWaveletSelfAdded)
  myRobot.register_handler(events.BlipSubmitted, OnBlipSubmitted)
  
  appengine_robot_runner.run(myRobot)