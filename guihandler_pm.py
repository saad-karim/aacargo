import pyautogui
import pyperclip
import time
import threading
import queue
from datetime import datetime
import json
from flask import Flask, request
from flask_restful import Resource, Api

cookieAcquired = 0
q = queue.Queue()
r = ""
lock = threading.Lock()

def guibot(refreshPage, awbCode, awbNumber, q):
  lock.acquire()
  try:
    # Focus on browser by clicking on it. This should be adjusted
    # on a machine basis and resolution set
    pyautogui.click(2500, 300)

    # This is commented out, if the browser is left open and on aacargo.com/AAACargo/tracking
    # there is no need to run the code below. Not running this code everytime significantly
    # improves performance. If it can't be garaunteed that the browser wills stay on the page,
    # this code needs to be added back
    if refreshPage == True:
      pyautogui.hotkey("ctrl", "l")
      pyautogui.hotkey("delete")
      pyautogui.typewrite("aacargo.com/AACargo/tracking")
      pyautogui.hotkey("enter")
      time.sleep(.1)

    # Focus on console input box
    time.sleep(.1)
    pyautogui.hotkey("ctrl", "`")

    # If there is anything left in the console from a previous run, delete it
    # Ensuring a clear console is critial before running any console command
    time.sleep(.1)
    pyautogui.hotkey("ctrl", "a")

    time.sleep(.1)
    pyautogui.hotkey("delete")

    # Must faster to do copy and paste instead of relying on pyautogui's write method
    time.sleep(.1)
    url = 'fetch("https://www.aacargo.com/api/tracking/awbs/", {method: "post", headers: {"Content-Type": "application/json"}, body: \'{"airwayBills": [{"awbCode": "%s", "awbNumber": "%s", "awbId": "0"}]}\'}).then(response => response.json()).then((data) => {fetch("http://localhost:5000/response", {method: "post", mode: "no-cors", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)})})' % (awbCode, awbNumber)
    pyperclip.copy(url)
    pyautogui.hotkey("ctrl", "v")
    # pyautogui.write(url)

    time.sleep(.1)
    pyautogui.hotkey("enter")

    while r == "":
      time.sleep(.1)
      print(".1 second")

    q.put(r)
  finally:
    lock.release()

class Track(Resource):
  def get(self):
    global cookieAcquired
    # If this is the first time we are running this request,
    # set the value of when we acquire the first cooked. A new
    # cookied will be requested every 4 hours to ensure that
    # request don't get blocked
    if cookieAcquired == 0:
      cookieAcquired = datetime.now()

    timeNow = datetime.now()
    diff = timeNow - cookieAcquired
    print('time diff: ', diff.total_seconds())
    refreshPage = False
    # if diff.total_seconds() >= (4*60*60):
    if diff.total_seconds() >= (10):
      refreshPage = True

    awbCode = request.args.get('awbCode')
    awbNumber = request.args.get('awbNumber')
    # response = guibot(refreshPage, awbCode, awbNumber)
    threading.Thread(target=guibot, args=(refreshPage, awbCode, awbNumber, q)).start()
    response = q.get()
    # print('Sending response >>> ', response)
    # response = '[{"airWayBillID":null,"airWaybillNumber":"43615434","airwayBillStatus":null,"sabreAirlineCode":"001","origin":"Philadelphia","destination":"Tyler","originAirportCode":"PHL","destinationAirportCode":"TYR","aaDestinationAirportCode":"TYR","airWayBillDate":"21Oct20","airWaybillUpdateDate":"22Oct,0553","airportCityRouting":"DFW","shipperName":"YOURWAY TRANSPORT INC","numberOfPieces":1,"grossWeight":"26.0","grossWeightUnit":"L","volume":"N/A ","volumeUnit":"","serviceLevel":"PPS","customsStatus":null,"customsTacmNumber":null,"consigneeName":null,"charges":null,"totalVolWeight":null,"totalVolWeightUnit":null,"chargeableWeight":null,"chargeableWeightUnit":null,"description":null,"descriptions":null,"pieces":null,"containerType":null,"latestStatus":"Delivered","latestStatusTimeStamp":null,"latestStatusDate":1604250360000,"showTrace":false,"splitExist":false,"flightNumber":0,"keyChangedEvent":false,"hiddenOriginalAirWaybillNumber":null,"originalAirWaybillNumber":null,"totalOnHandPieceCountAtDest":0,"totalArrivedPieceCountAtDest":0,"barHighlightSegment":3,"barCssColorCode":2,"firstBarSegDisplayText":"Received","lastBarSegDisplayText":"Delivered","error":false,"dimensions":[],"showCustomsTab":false,"bookedFlightDetailsList":[{"departureDate":null,"flightNumber":"792","departureStationCode":"PHL","scheduledArrivalAirport":"DFW","scheduledArrivalDate":"10/22/2020 09:36 AM","scheduledArrivalTime":null,"scheduledDepartureDate":"10/22/2020 07:00 AM","scheduledDepartureTime":null,"differenceOfDaysBasedOnLocales":"","airlineIATACode":"AA","bookingStatus":"C","splitId":0,"rankId":0,"isInternationalLeg":false,"uniqueFlight":{"departureDate":null,"flightNumber":"792","departureStationCode":"PHL"}},{"departureDate":null,"flightNumber":"3405","departureStationCode":"DFW","scheduledArrivalAirport":"TYR","scheduledArrivalDate":"10/22/2020 11:26 AM","scheduledArrivalTime":null,"scheduledDepartureDate":"10/22/2020 10:35 AM","scheduledDepartureTime":null,"differenceOfDaysBasedOnLocales":"","airlineIATACode":"AA","bookingStatus":"C","splitId":0,"rankId":0,"isInternationalLeg":false,"uniqueFlight":{"departureDate":null,"flightNumber":"3405","departureStationCode":"DFW"}}],"airWayBillTrackingHistoryDtos":[{"status":"Delivered","timeStampString":null,"timeStampDate":"01-Nov-2020 17:06:00","localTimeStampDate":null,"pieces":"1","container":null,"skip":false,"differenceOfDaysBasedOnLocales":null,"details":"IBS","departureAirport":"TYR","arrivalAirport":"TYR","fltNum":"","scheduledDepartureAirport":null,"scheduledArrivalAirport":null,"scheduledArrivalDate":null,"scheduledArrivalTime":null,"scheduledDepartureDate":null,"scheduledDepartureTime":null,"scheduledDepartureGmtDateTime":null,"departedGateDate":"N/A","departedGateTime":"N/A","gateInDate":null,"gateInTime":null,"statusDate":"10/22/2020 12:06 PM","statusTime":null,"airlineName":"AA","nameOfPersonWhoSignedOff":"JOSE FLORES","refusalReason":null,"onHandPostingDate":null,"barHighlightSegment":0,"barCssColorCode":0,"containerType":null,"pieceContainerList":null,"bookedFlightDetailsList":null,"statusCode":"DLV","ctnLocation":"TYR","rank":0},{"status":"Ready for pick up","timeStampString":null,"timeStampDate":"27-Oct-2020 16:53:17","localTimeStampDate":null,"pieces":"1","container":null,"skip":false,"differenceOfDaysBasedOnLocales":null,"details":"IBS","departureAirport":"TYR","arrivalAirport":"TYR","fltNum":"3405","scheduledDepartureAirport":null,"scheduledArrivalAirport":null,"scheduledArrivalDate":null,"scheduledArrivalTime":null,"scheduledDepartureDate":null,"scheduledDepartureTime":null,"scheduledDepartureGmtDateTime":null,"departedGateDate":"N/A","departedGateTime":"N/A","gateInDate":null,"gateInTime":null,"statusDate":"10/22/2020 11:53 AM","statusTime":null,"airlineName":"AA","nameOfPersonWhoSignedOff":null,"refusalReason":null,"onHandPostingDate":null,"barHighlightSegment":0,"barCssColorCode":0,"containerType":null,"pieceContainerList":null,"bookedFlightDetailsList":null,"statusCode":"NFD","ctnLocation":"TYR","rank":0},{"status":"Prepared for loading","timeStampString":null,"timeStampDate":"22-Oct-2020 09:54:01","localTimeStampDate":null,"pieces":"1","container":null,"skip":false,"differenceOfDaysBasedOnLocales":"","details":"IBS","departureAirport":"PHL","arrivalAirport":"DFW","fltNum":"792","scheduledDepartureAirport":null,"scheduledArrivalAirport":null,"scheduledArrivalDate":"10/22/2020 09:27 AM","scheduledArrivalTime":null,"scheduledDepartureDate":"10/22/2020 07:00 AM","scheduledDepartureTime":null,"scheduledDepartureGmtDateTime":null,"departedGateDate":"N/A","departedGateTime":"N/A","gateInDate":null,"gateInTime":null,"statusDate":"10/22/2020 05:54 AM","statusTime":null,"airlineName":"AA","nameOfPersonWhoSignedOff":null,"refusalReason":null,"onHandPostingDate":null,"barHighlightSegment":0,"barCssColorCode":0,"containerType":null,"pieceContainerList":[{"pieces":"1","container":"PHLP0792"}],"bookedFlightDetailsList":null,"statusCode":"PRE","ctnLocation":"PHL","rank":0},{"status":"Accepted","timeStampString":null,"timeStampDate":"22-Oct-2020 09:53:31","localTimeStampDate":null,"pieces":"1","container":null,"skip":false,"differenceOfDaysBasedOnLocales":null,"details":"IBS","departureAirport":"PHL","arrivalAirport":"TYR","fltNum":"792","scheduledDepartureAirport":null,"scheduledArrivalAirport":null,"scheduledArrivalDate":null,"scheduledArrivalTime":null,"scheduledDepartureDate":"10/22/2020 07:00 AM","scheduledDepartureTime":null,"scheduledDepartureGmtDateTime":null,"departedGateDate":"N/A","departedGateTime":"N/A","gateInDate":null,"gateInTime":null,"statusDate":"10/22/2020 05:53 AM","statusTime":null,"airlineName":"AA","nameOfPersonWhoSignedOff":null,"refusalReason":null,"onHandPostingDate":null,"barHighlightSegment":0,"barCssColorCode":0,"containerType":null,"pieceContainerList":null,"bookedFlightDetailsList":null,"statusCode":"RCS","ctnLocation":"PHL","rank":0},{"status":"Booked","timeStampString":null,"timeStampDate":"21-Oct-2020 23:47:08","localTimeStampDate":null,"pieces":"1","container":null,"skip":false,"differenceOfDaysBasedOnLocales":null,"details":"IBS","departureAirport":"DFW","arrivalAirport":"TYR","fltNum":"792","scheduledDepartureAirport":null,"scheduledArrivalAirport":null,"scheduledArrivalDate":null,"scheduledArrivalTime":null,"scheduledDepartureDate":"10/22/2020 10:35 AM","scheduledDepartureTime":null,"scheduledDepartureGmtDateTime":null,"departedGateDate":"N/A","departedGateTime":"N/A","gateInDate":null,"gateInTime":null,"statusDate":"10/21/2020 06:47 PM","statusTime":null,"airlineName":"AA","nameOfPersonWhoSignedOff":null,"refusalReason":null,"onHandPostingDate":null,"barHighlightSegment":0,"barCssColorCode":0,"containerType":null,"pieceContainerList":null,"bookedFlightDetailsList":null,"statusCode":"BKD","ctnLocation":"DFW","rank":0}],"ppsError":false,"ppsErrorCode":null,"noLocateOrReceivedActive":false,"customHoldActive":false,"deliveredToClaims":false,"noLocateOrReceivedActiveAtOrigin":false,"inTransitPlanned":false,"routeItinerary":false}]'
    j = json.loads(response)
    global r
    r = ""
    return j

class Response(Resource):
  def post(self):
    # print('posting response >>> ', request.get_data())
    global r
    r = request.data

class Server:
  app = Flask(__name__)
  api = Api(app)

  api.add_resource(Track, '/track')
  api.add_resource(Response, '/response')

  def run(self, host):
    self.app.run(host=host)

if __name__ == "__main__": 
  server = Server()
  server.run('0.0.0.0')
      