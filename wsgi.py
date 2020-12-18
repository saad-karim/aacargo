from server import app, q
import queue

if __name__ == "__main__":
  q = queue.Queue
  app.run()

  # q = queue.Queue()
  # lock = threading.Lock()

  # api.add_resource(Track, '/track', resource_class_kwargs={'lock': lock, 'queue': q})
  # api.add_resource(TrackResponse, '/response', resource_class_kwargs={'queue': q})