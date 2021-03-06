#!/usr/bin/env python
#https://gist.github.com/virtix/1126917#using-selenium-with-remote-webdriver
# http://selenium-python.readthedocs.org/en/latest/api.html
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import selenium.webdriver.firefox.firefox_profile as firefox_profile

# Create a new instance of the Firefox driver
#driver = webdriver.Firefox()
#driver = webdriver.Chrome()

# enable settings in "about:config"
firefoxProfile = webdriver.FirefoxProfile(); # OSX ref ~/Library/Application Support/Firefox/Profiles/*/prefs.js
firefoxProfile.set_preference('canvas.capturestream.enabled', True);
firefoxProfile.set_preference('media.peerconnection.ice.tcp', True);
firefoxProfile.update_preferences()

#launch remote instance

# go to the google home page
opts = [ (0,0),(0,1),(1,0),(1,1)]

for i in range(len(opts)):
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX, browser_profile=firefoxProfile)
    url="http://g.umbocv.com:8000/kms-client-js/rtc.html?forceICETCP=%d&notrickle=%d" % opts[i]
    print(url)
    driver.get(url);
    timing = [];
    try:
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 30).until(EC.title_contains("Auto"))
        print driver.title

        while driver.execute_script("return document.getElementById('videoInput').error") ==None and \
                not driver.execute_script("return document.getElementById('videoInput').onend"):
            message= driver.find_element_by_id('message').text
            timing.append(map(float,message.split()[2].split(',')))

    finally:
        driver.quit()

    import numpy;
    numpy.array(timing).dump('timing%d.npz' %i);
