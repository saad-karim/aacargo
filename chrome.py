import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local"
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    # 'download.default_directory': 'C:\\Users\\Oli\\Google Drive',
    # "download.directory_upgrade": True
}

profile = {
  'printing.print_preview_sticky_settings.appState': json.dumps(appState),
  # 'download.default_directory': 'C:\\Users\\Oli\\Google Drive',
  # 'download.directory_upgrade': True
  }

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', profile)
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument('--headless')

# driver = webdriver.Chrome(executable_path="/usr/bin/google-chrome-stable", chrome_options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get('https://www.google.com/')
driver.execute_script('window.print();')