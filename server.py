from datetime import datetime
import json
from flask import Flask, Response, request
from flask_restful import Resource, Api
from bot import Bot
import threading
import queue
import time
import os

aaBot = Bot()
cookieAcquired = 0

refreshInterval = os.environ.get('AABOT_BROWSER_REFRESH_INTERVAL')
if refreshInterval == None:
  refreshInterval = 15
else:
  refreshInterval = int(refreshInterval)

timeout = os.environ.get('AABOT_TIMEOUT')
if timeout == None:
  timeout = 5
else:
  timeout = int(timeout)

class Track(Resource):
  def __init__(self, lock, queue):
    self.lock = lock
    self.queue = queue

  def get(self):
    try:
      self.lock.acquire()
      print("[Server] Get request received")
      trackingResponse = None

      global cookieAcquired

      # If this is the first time we are running this request,
      # set the value of when we acquire the first cooked.
      if cookieAcquired == 0:
        aaBot.refreshPage()
        cookieAcquired = datetime.now()

      # A new cookie will be requested every 4 hours to ensure that
      # request don't get blocked
      timeNow = datetime.now()
      diff = timeNow - cookieAcquired

      if diff.total_seconds() >= refreshInterval:
        # If refresh interval has passed, efresh page to get new cookie
        cookieAcquired = datetime.now()
        aaBot.refreshPage()

      awbCode = request.args.get('awbCode')
      awbNumber = request.args.get('awbNumber')

      print("[Server] Fetching tracking information")
      threading.Thread(target=aaBot.track, args=(awbCode, awbNumber)).start()

      trackingResponse = self.queue.get(block=True, timeout=timeout)
      response = json.loads(trackingResponse)

      # If response contains status, the means most likely the quest failed and we should the appropriate HTTP error
      # code to return back to client
      if "status" in response:
        return Response(trackingResponse, status=response["status"], mimetype='application/json')

      # The queue should have only a single element in it a time. If after reading of the queue
      # there are still values in the queue, there might be stale date in the queue and it should be removed
      if self.queue.empty() is False:
        self.queue = queue.Queue()

      print("[Server] Request for {} completed".format(awbNumber))
      return response
    except queue.Empty:
      print("[Server] ERROR - Request for {} failed, make sure that developer tools is open to console tab and browser is on right page".format(awbNumber))
      return Response("server failed to handle request", status=500, mimetype='application/json')
    finally:
      self.lock.release()

class TrackResponse(Resource):
  def __init__(self, queue):
    self.queue = queue

  def post(self):
    print("[Server] Post request received")
    self.queue.put(request.data)

app = Flask(__name__)

class Server:
  api = Api(app)

  q = queue.Queue()
  lock = threading.Lock()

  api.add_resource(Track, '/track', resource_class_kwargs={'lock': lock, 'queue': q})
  api.add_resource(TrackResponse, '/response', resource_class_kwargs={'queue': q})