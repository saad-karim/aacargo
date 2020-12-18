from datetime import datetime
import json
from flask import Flask, Response, request
from flask_restful import Resource, Api
from bot import Bot
import threading
import queue
import time

aaBot = Bot()
cookieAcquired = 0

class Track(Resource):
  def __init__(self, lock, queue):
    self.lock = lock
    self.queue = queue

  def get(self):
    try:
      self.lock.acquire()
      print("Get request received: ")
      trackingResponse = None

      global cookieAcquired

      # If this is the first time we are running this request,
      # set the value of when we acquire the first cooked.
      if cookieAcquired == 0:
        cookieAcquired = datetime.now()

      # A new cookie will be requested every 4 hours to ensure that
      # request don't get blocked
      timeNow = datetime.now()
      diff = timeNow - cookieAcquired

      # if diff.total_seconds() >= (4*60*60):
      if diff.total_seconds() >= (15):
        # 4 hours have passed, refresh page to get new cookie
        cookieAcquired = datetime.now()
        aaBot.refreshPage()

      awbCode = request.args.get('awbCode')
      awbNumber = request.args.get('awbNumber')
      threading.Thread(target=aaBot.track, args=(awbCode, awbNumber)).start()

      trackingResponse = self.queue.get()
      while trackingResponse == "":
        time.sleep(.1)
        trackingResponse = self.queue.get()
    finally:
      self.lock.release()

    response = json.loads(trackingResponse)
    if "status" in response:
      return Response(trackingResponse, status=response["status"], mimetype='application/json')

    return response

class TrackResponse(Resource):
  def __init__(self, queue):
    self.queue = queue

  def post(self):
    print("Post request received: ", request.data)
    self.queue.put(request.data)

app = Flask(__name__)

class Server:
  api = Api(app)

  q = queue.Queue()
  lock = threading.Lock()

  api.add_resource(Track, '/track', resource_class_kwargs={'lock': lock, 'queue': q})
  api.add_resource(TrackResponse, '/response', resource_class_kwargs={'queue': q})