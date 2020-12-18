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

app = Flask(__name__)
api = Api(app)

# q = queue.Queue()
q = None
lock = threading.Lock()

class Track(Resource):
  def get(self):
    lock.acquire()
    trackingResponse = None

    try:
      awbCode = request.args.get('awbCode')
      awbNumber = request.args.get('awbNumber')
      
      print("Get call received to track number {}".format(awbNumber))
      # If this is the first time we are running this request,
      # set the value of when we acquire the first cooked.
      global cookieAcquired
      if cookieAcquired == 0:
        cookieAcquired = datetime.now()

      # A new cookie will be requested every 4 hours to ensure that
      # request don't get blocked
      timeNow = datetime.now()
      diff = timeNow - cookieAcquired

      if diff.total_seconds() >= (4*60*60):
        # 4 hours have passed, refresh page to get new cookie
        cookieAcquired = datetime.now()
        aaBot.refreshPage()

      threading.Thread(target=aaBot.track, args=(awbCode, awbNumber)).start()
      print("Bot run completed")

      # print("size of queue: ", q.qsize())
      # if q.qsize() > 0: 
      #   trackingResponse = q.get()
      # print('tracking response: ', trackingResponse)
      while trackingResponse == None:
        time.sleep(.1)
        print("size of queue: ", q.qsize())
        if q.qsize() > 0: 
          trackingResponse = q.get(block=True)
          print('tracking response: ', trackingResponse)
        # trackingResponse = q.get(block=True)

    finally:
      lock.release()

    response = json.loads(trackingResponse)
    if "status" in response:
      return Response(trackingResponse, status=response["status"], mimetype='application/json')

    return response

class TrackResponse(Resource):
  def post(self):
    print("Post request from bot: ", request.data)
    q.put(request.data)
    print("size of queue: ", q.qsize())

api.add_resource(Track, '/track' )
api.add_resource(TrackResponse, '/response')

# class Server():
#   app = Flask(__name__)
#   api = Api(app)

#   q = queue.Queue()
#   lock = threading.Lock()

#   api.add_resource(Track, '/track', resource_class_kwargs={'lock': lock, 'queue': q})
#   api.add_resource(TrackResponse, '/response', resource_class_kwargs={'queue': q})

#   def run(self, host):
#     self.app.run(host=host)

# if __name__ == "__main__": 
#   server = Server()
#   server.run('0.0.0.0')