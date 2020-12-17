import pyautogui
import pyperclip
import time

class Bot():
  def refreshPage(self):
    print("Refreshing page...")

    # Focus on browser by clicking on it. This should be adjusted
    # on a machine basis and resolution set. The browser should be
    # maximized mode
    x, _ = pyautogui.size()
    pyautogui.click(x/2, 0)

    pyautogui.hotkey("ctrl", "l")
    pyautogui.hotkey("delete")
    pyautogui.typewrite("aacargo.com/AACargo/tracking")
    pyautogui.hotkey("enter")

  def track(self, awbCode, awbNumber):
    print("Tracking number {}".format(awbNumber))

    # Focus on browser by clicking on it. This should be adjusted
    # on a machine basis and resolution set. The browser should be
    # maximized mode
    x, _ = pyautogui.size()
    pyautogui.click(x/2, 0)

    # Focus on console input box
    time.sleep(.05)
    pyautogui.hotkey("ctrl", "`")

    # If there is anything left in the console from a previous run, delete it
    # Ensuring a clear console is critial before running any console command
    time.sleep(.05)
    pyautogui.hotkey("ctrl", "a")

    time.sleep(.05)
    pyautogui.hotkey("delete")

    # Must faster to do copy and paste instead of relying on pyautogui's write method
    time.sleep(.05)
    url = 'fetch("https://www.aacargo.com/api/tracking/awbs/", {method: "post", headers: {"Content-Type": "application/json"}, body: \'{"airwayBills": [{"awbCode": "%s", "awbNumber": "%s", "awbId": "0"}]}\'}).then(response => response.json()).then((data) => {fetch("http://localhost:5000/response", {method: "post", mode: "no-cors", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)})})' % (awbCode, awbNumber)
    pyperclip.copy(url)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")