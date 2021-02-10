import pdfgen
from flask import request
from flask_restful import Resource
from pychromepdf import ChromePDF
from requests_html import HTMLSession

PATH_TO_CHROME_EXE = '/usr/bin/google-chrome-stable'

class PDFGenerator(Resource):
  def get(self):
    print("PDF Generator")

    trackingNumber = request.args.get('number')
    url = "https://dispatch.yourwaytransport.com/uk/invoice?number={}".format(trackingNumber)

    pdfgen.sync.from_url(url, 'test1.pdf')

    # session = HTMLSession()
    # r = session.get(url)
    # r.html.render()

    # print(r.content)

    # resp = r.content.decode("utf-8")
    # print(resp)

    # with open('invoice.html', 'wb') as fd:
    #   fd.write(r.content)

    # pdfkit.from_url(url, 'out.pdf')

    # cpdf = ChromePDF(PATH_TO_CHROME_EXE)


    # with open('test2.pdf', 'wb') as fd:
    #   fd.write(r.content)
    # for chunk in r.iter_content(chunk_size):
    #     fd.write(chunk)

      # create a file and write the pdf to it
    # with open('test.pdf','w') as output_file:
    #   print(resp)
    #   if cpdf.html_to_pdf(resp,output_file):
    #       print("Successfully generated the pdf: {}".format(output_file.name))
    #   else:
    #       print("Error generating pdf")