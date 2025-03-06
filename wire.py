
from seleniumwire import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
import time
## Define Your Proxy Endpoints
proxy_options = {
    'proxy': {
        'http': 'http://kheYdSdd:LGsFYFAY@45.199.205.7:64848',
        'https': 'http://kheYdSdd:LGsFYFAY@45.199.205.7:64848',
        'no_proxy': 'localhost:127.0.0.1'
    }
}

## Set Up Selenium Chrome driver
driver = webdriver.Chrome(seleniumwire_options=proxy_options)

## Send Request Using Proxy
driver.get('https://whatismyipaddress.com/')
time.sleep(200)

