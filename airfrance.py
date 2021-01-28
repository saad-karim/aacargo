from flask import request
from flask_restful import Resource
import requests

class AirFrance(Resource):
  def get(self):
    trackingNumber = request.args.get('trackingNumber')
    url = "https://www.afklcargo.com/mycargo/api/shipment/detail/{}".format(trackingNumber)

    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
      'Connection': "keep-alive",
      'Accept': 'application/json',
      'Accept-Encoding': "gzip, deflate, br",
      'Cache-Control': 'no-cache',
      'Host': 'www.afklcargo.com',
    }

    session = requests.Session()
    # r = session.get("https://www.afklcargo.com", headers=headers, verify=False, timeout=30)

    r = session.get(url, headers=headers)
    return r.json()