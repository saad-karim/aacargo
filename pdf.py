import asyncio
import io
from pychromepdf import ChromePDF
from pyppeteer import launch
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

async def main():
  browser = await launch(headless=True, executablePath='/usr/bin/google-chrome-stable')
  page = await browser.newPage()
  
  url = "https://dispatch.yourwaytransport.com/uk/invoice?number={}".format("726215")
  print("URL: ", url)

  await page.goto(url)
  await page.waitFor(5000)
  cont = await page.content()

  PATH_TO_CHROME_EXE = '/usr/bin/google-chrome-stable'
  cpdf = ChromePDF(PATH_TO_CHROME_EXE)
  with open('test.pdf','w') as output_file:
      if cpdf.html_to_pdf(cont,output_file):
          print("Successfully generated the pdf: {}".format(output_file.name))
      else:
          print("Error generating pdf")

  packet = io.BytesIO()
  # create a new PDF with Reportlab
  can = canvas.Canvas(packet, pagesize=letter)
  can.drawString(10, 100, "Hello world")
  can.save()

  #move to the beginning of the StringIO buffer
  packet.seek(0)
  new_pdf = PdfFileReader(packet)
  # read your existing PDF
  existing_pdf = PdfFileReader(open("test.pdf", "rb"))
  output = PdfFileWriter()
  # add the "watermark" (which is the new pdf) on the existing page
  page = existing_pdf.getPage(0)
  page.mergePage(new_pdf.getPage(0))
  output.addPage(page)
  # finally, write "output" to a real file
  outputStream = open("test2.pdf", "wb")
  output.write(outputStream)
  outputStream.close()

  # pdfkit.from_string(cont, 'test2.pdf')

asyncio.get_event_loop().run_until_complete(main())