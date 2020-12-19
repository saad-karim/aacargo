import pyautogui
import pyperclip
import time
import os

guiInputInterval = os.environ.get('AABOT_GUI_INTERVAL')
if guiInputInterval == None:
  guiInputInterval = 0.05
else:
  guiInputInterval = float(guiInputInterval)

preserveConsoleLog = os.environ.get('AABOT_PRESERVE_CONSOLE_HISTORY')

class Bot():
  def refreshPage(self):
    print("Refreshing page...")

    # Focus on browser by clicking on it. This should be adjusted
    # on a machine basis and resolution set. The browser should be
    # maximized mode
    x, _ = pyautogui.size()
    pyautogui.click(x/2, 0)

    pyautogui.hotkey("shift", "f6") # Moves focus out of developer tools to chrome page
    pyautogui.hotkey("ctrl", "l") # Shortcut to URL input
    pyautogui.hotkey("delete")
    pyautogui.typewrite("aacargo.com/AACargo/tracking")
    pyautogui.hotkey("enter")
    time.sleep(guiInputInterval)

  def track(self, awbCode, awbNumber):
    print("[Automation] Tracking number {}".format(awbNumber))

    # Focus on browser by clicking on it. This should be adjusted
    # on a machine basis and resolution set. The browser should be
    # maximized mode
    x, _ = pyautogui.size()
    pyautogui.click(x/2, 0)

    # Focus on console input box
    time.sleep(guiInputInterval)
    pyautogui.hotkey("ctrl", "`")

    if preserveConsoleLog not in ['true', 'TRUE', 'True']: 
      time.sleep(guiInputInterval)
      pyautogui.hotkey("ctrl", "l")

    # If there is anything left in the console from a previous run, delete it
    # Ensuring a clear console is critial before running any console command
    time.sleep(guiInputInterval)
    pyautogui.hotkey("ctrl", "a")

    time.sleep(guiInputInterval)
    pyautogui.hotkey("delete")

    # Much faster to do copy and paste instead of relying on pyautogui's write method
    time.sleep(guiInputInterval)
    url = 'fetch("https://www.aacargo.com/api/tracking/awbs/", {method: "post", headers: {"Content-Type": "application/json"}, body: \'{"airwayBills": [{"awbCode": "%s", "awbNumber": "%s", "awbId": "0"}]}\'}).then(response => response.json()).then((data) => {fetch("http://localhost:5000/response", {method: "post", mode: "no-cors", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)})})' % (awbCode, awbNumber)
    pyperclip.copy(url)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    print("[Automation] Task completed for number {}".format(awbNumber))