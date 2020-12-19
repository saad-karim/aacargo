## Setup Guide ##

Linux:

NOTE: You must install tkinter on Linux to use MouseInfo. Run the following: sudo apt-get install python3-tk python3-dev

Mac:


### Configuration ###

Supported Environment Variables:

`AABOT_BROWSER_REFRESH_INTERVAL` - This is the amount of time between browser refreshes. After a certain period
of time the cookies go stale and requests start to fail. By default, refreshes happend at every 15 seconds. This
can be adjusted using this environment variable. The interval is defined in seconds. For example, setting this
to 50 will trigger a browser refresh if the 50 seconds have passed the last refresh.

`AABOT_GUI_INTERVAL` - This is the amout of time intentional delay between major GUI input. This delay exists
to allow for the previous GUI action to have taken effect, otherwise the next GUI interaction might fail. By default,
this interval is set to 0.05 seconds. The interval is defined in seconds. This can adjusted to allow allow slower
machines more time process GUI events.

`AABOT_PRESERVE_CONSOLE_HISTORY` - If set to true, the console logs will not be deleted between request. This is
disabled by default to preven the console log from getting infinitely big, and consuming memory.

### Starting Server ###

1. Start server by running `gunicorn -w 1 --threads 20 -b 0.0.0.0:5000 wsgi:app`
2. Open a browser window, and navigate to www.aacargo.com/AACargo/tracking
3. Open developers tools to 'Console' tab, see image below:

![](docs/BrowserWindow.png)

## Notes ##

If the server takes a long time to respond, the connection will timeout based on the client's timeout settings.
By default, the client timesout after 30 seconds.
