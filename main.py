# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:49:13 2023

@author: HP
"""
import threading
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from interaction import SpotifyGenerator
from class_fichier import C_Fichier

import os
import asyncio

# from capmonstercloudclient import CapMonsterClient, ClientOptions
# from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest
from dotenv import load_dotenv

load_dotenv()
LINK = os.getenv("LINK")
USER = str(os.getenv("USER_PORXY"))
PASSWORD = str(os.getenv("PASSWORD"))
PROXY = str(os.getenv("PROXY"))
PORT = str(os.getenv("PORT"))
address = str(os.getenv("ADDRESS"))
print(USER, PASSWORD, PROXY, PORT)
# print(address)
# api_key = os.getenv("api_key")
# key = os.getenv("key")
def fill_address(driver, address):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="address"]'))
        )
    except:

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="plan-already-full-error-page"]'))
            )
        except:
            print("NOTE: No address field there, Check your invite link and try again (stop the program ctrl+c".upper())
        else:
            print("YOU LINK IS FULL, WILL TRY TO GET NEW LINK NEXT TIME...")
        # print("-------------------------------------------------------------------------------------")
        # print(driver.find_element("tag name", "body").text)
        # print("-------------------------------------------------------------------------------------")
        driver.quit()
        exit()
    else:
        driver.find_element(By.XPATH, '//*[@id="address"]').send_keys(address)
        print("address fieled")
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
        except:
            print("NOTE: No submit there")
        else:
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            print("form submitted")
            # time.sleep(1)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]'))
                )
            except:
                print("NOTE: No confirm there")
            else:
                while True:
                    actions = ActionChains(driver)
                    actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]')).pause(0.5).click().perform()
                    print("form confirmed")
                    try:
                        WebDriverWait(driver, 3).until(
                            EC.invisibility_of_element_located((By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]'))
                        )
                    except:
                        actions = ActionChains(driver)
                        actions.move_to_element(
                            driver.find_element(By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]')).pause(
                            0.5).click().perform()
                        print("form confirmed again")
                    else:
                        break


                # return
                # time.sleep(3000)
                # try:
                #     WebDriverWait(driver, 2).until(
                #         EC.element_to_be_clickable((By.XPATH, "//button[//text()[contains(., 'Confirm')]]"))
                #     )
                # except:
                #     print("NOTE: No confirm there")
                # else:
                #     driver.find_element(By.XPATH, "//button[//text()[contains(., 'Confirm')]]").click()
                #     print("form confirmed again")

# client_option = ClientOptions(api_key=api_key)
# cap_monster_client = CapMonsterClient(options=client_option)
#
# async def cap_monster_solver(api_key = api_key, site = "", key=key):
#     recaptcha_req = RecaptchaV2ProxylessRequest(websiteUrl=site, websiteKey=key)
#     result = await cap_monster_client.solve_captcha(recaptcha_req)
#     return result['gRecaptchaResponse']
def main():
    sp = SpotifyGenerator()
    playlist_links = [item.strip() for item in C_Fichier("playlists.txt").Fichier_to_Liste()]


    # sp.get_driver(user=USER, password=PASSWORD, proxy=PROXY, port=PORT)

    thread1 = threading.Thread(target=sp.get_driver, args=(USER, PASSWORD, PROXY, PORT))
    thread2 = threading.Thread(target=sp.get_Email_from_yopmail)
    # thread22 = threading.Thread(target=main)

    thread1.start()
    thread2.start()
    # thread22.start()

    thread1.join()
    thread2.join()



    # sp.get_driver()
    sp.get_site()
    # sp.get_Email_from_yopmail()
    #sp.go_to_signup()
    sp.fill_email_and_confrm()
    sp.remove_descrections()
    sp.fill_password()
    sp.fill_displayed_name()
    sp.fill_date_of_birth()
    sp.fill_gender()
    sp.submit_signup_button()
#     while True:
#         try:
#             WebDriverWait(sp.driver, 10).until(
#                 EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Terms')]"))
#             )
#         except:
#             print("still looping")
#         else:
#             break
#     time.sleep(10)
#     print("solving")
#     # time.sleep(30000)
#
#     response = await cap_monster_solver(api_key=api_key, key=key, site=sp.driver.current_url)
#     print("response", response)
#     time.sleep(2)
#     sp.driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{response}";')
#     # sp.driver.execute_script(f'document.getElementById("g-recaptcha-response").value ="{response}";')
#     time.sleep(2)
#     sp.driver.execute_script("""
#     var recaptchaResponse = document.getElementById("g-recaptcha-response");
#     recaptchaResponse.dispatchEvent(new Event("change", { bubbles: true }));
# """)
#     sp.driver.execute_script("""
#     window.grecaptcha = {
#         getResponse: function() { return arguments[0]; }
#     };
# """, response)
#     sp.driver.execute_script("""
#         var recaptchaCallback = document.createEvent('Event');
#         recaptchaCallback.initEvent('change', true, true);
#         document.getElementById("g-recaptcha-response").dispatchEvent(recaptchaCallback);
#     """)
#     print("check now")
#     time.sleep(3)
#     continue_btn = sp.driver.find_element(By.XPATH, "//button[span[text()='Continue']]")
#
#     actions = ActionChains(sp.driver)
#     actions.move_to_element(continue_btn).pause(0.5).click().perform()
#     # continue_btn.click()
#     print("continue clicked")
#
#
#
#     time.sleep(2000)
    # sp.check_capSolver()
    if sp.hit_continue():
        return

    sp.check_login_signup()

    # sp.get_site("https://www.spotify.com/ng/family/join/invite/0cby9X4YCzCc7XB/".replace("invite", "confirm"))
    sp.get_site(LINK.replace("invite", "address"))

    fill_address(driver=sp.driver, address=address)

    # sp.driver.save_screenshot('screenshot_filename2.png')

    # CHECK THING
    try:
        WebDriverWait(sp.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "https://open.spotify.com/")]'))
        )
        print("Spotify link found!")
    # except:
    #     print("Spotify link not found within timeout.")
    #
    # try:
    #     print("waiting for address to disappear...")
    #     WebDriverWait(sp.driver, 100).until(
    #         EC.invisibility_of_element_located(
    #             (By.XPATH, '//*[@id="address"]')
    #         ))
    except:
        print("something not working")
        print("-------------------------------------------------------------------------------------")
        print(sp.driver.find_element("tag name", "body").text)
        print("-------------------------------------------------------------------------------------")
        sp.driver.save_screenshot('screenshot_filename.png')
        sp.quit()
        exit()
    else:
        print("done")
        # time.sleep(3000)
        for link in playlist_links:
            sp.get_site(link)
            try:
                _ = WebDriverWait(sp.driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="add-button"]')))
            except Exception as e:
                print("Eroor:", link)
                print(e)
                continue
            else:
                button = sp.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="add-button"]')
                button.click()
                print("Done:", link)
                time.sleep(1)


        sp.quit()
        exit()

if __name__ == "__main__":
    # asyncio.run(main())
    # main()

    print("starting")
    n = int(input("Enter the number of threading: "))
    i = 0
    while True:
        if i != 0:
            print("Starting again in 2 seconds...")
            time.sleep(2)
        if i == 10:
            break
        i += 1
        if n == 1:
            main()
        elif n == 2:
            thread1 = threading.Thread(target=main)
            thread2 = threading.Thread(target=main)

            thread2.start()
            thread1.start()

            thread1.join()
            thread2.join()
        elif n == 3:
            thread1 = threading.Thread(target=main)
            thread2 = threading.Thread(target=main)
            thread22 = threading.Thread(target=main)

            thread2.start()
            thread1.start()
            thread22.start()

            thread1.join()
            thread2.join()
            thread22.join()
        elif n == 4:
            thread1 = threading.Thread(target=main)
            thread2 = threading.Thread(target=main)
            thread22 = threading.Thread(target=main)
            thread222 = threading.Thread(target=main)

            thread2.start()
            thread1.start()
            thread22.start()
            thread222.start()

            thread1.join()
            thread2.join()
            thread22.join()
            thread222.join()
        else:
            print("Try again (choose a number between 1 and 4")
            break
