from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("api_key")
website_key = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
# website_url = browser.current_url
client_option = ClientOptions(api_key=api_key)
cap_monster_client = CapMonsterClient(options=client_option)


key = '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'

async def cap_monster_solver(site = "", key=key):
    recaptcha_req = RecaptchaV2ProxylessRequest(websiteUrl=site, websiteKey=key)
    result = await cap_monster_client.solve_captcha(recaptcha_req)
    return result['gRecaptchaResponse']



async def main():
    # api_key = "YOUR_CAPMONSTER_API_KEY"
    key = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"

    browser = webdriver.Chrome()
    browser.get("https://www.google.com/recaptcha/api2/demo")
    await asyncio.sleep(4)
    # Solve captcha
    response = await cap_monster_solver(key=key, site="https://www.google.com/recaptcha/api2/demo")
    print("Solved reCAPTCHA Token:", response)
    await asyncio.sleep(2)
    browser.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{response}";')
    await asyncio.sleep(2)

    print("# Response injected to secret input.")
    browser.find_element(By.ID,"recaptcha-demo-submit").click()
    print("cliked")
    await asyncio.sleep(200)
    return

# response = await cap_monster_solver(api_key=api_key, key=key, site='https://www.google.com/recaptcha/api2/demo')
# print("response", response)
asyncio.run(main())

print("# Form submitted.")