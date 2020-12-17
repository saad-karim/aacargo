NOTE: You must install tkinter on Linux to use MouseInfo. Run the following: sudo apt-get install python3-tk python3-dev

https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-2-install-gui/

ssh -i ~/.ssh/aacargo.pem ec2-user@ec2-54-226-37-95.compute-1.amazonaws.com

Use this one: ssh -i ~/.ssh/aacargo.pem -L 5901:localhost:5901 -i PEM_FILE ec2-user@54.226.37.95 

https://understandingdata.com/install-google-chrome-selenium-ec2-aws/

https://askubuntu.com/questions/508410/after-install-google-chrome-in-ec2-wont-open-from-ubuntu-server-14-04-lts-hvm
https://understandingdata.com/install-google-chrome-selenium-ec2-aws/
https://askubuntu.com/questions/1048723/google-chrome-can-not-start-under-vnc-ubuntu-18-04

google-chrome --no-sandbox

vncviewer


## Setup Guide ##

1. Open a browser window, and navigate to www.aacargo.com/AACargo/tracking
2. Open developers tools to 'Console' tab

![](docs/BrowserWindow.png)