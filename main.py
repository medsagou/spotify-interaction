# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:49:13 2023

@author: HP
"""
import threading
import concurrent.futures

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from interaction import SpotifyGenerator
from class_fichier import C_Fichier

import os
# import asyncio

# from capmonstercloudclient import CapMonsterClient, ClientOptions
# from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest



# USER = str(os.getenv("USER_PORXY"))
# PASSWORD = str(os.getenv("PASSWORD"))
# PROXY = str(os.getenv("PROXY"))
# PORT = str(os.getenv("PORT"))

stop_event = threading.Event()
done_counter = 0
counter_lock = threading.Lock()

if input("use env? (y/n)").strip().lower() == "y":
    from dotenv import load_dotenv

    load_dotenv()
    try:
        PROXY, PORT, USER, PASSWORD = os.getenv("PROXY").strip().split(":")
        LINK = os.getenv("LINK")
        address = str(os.getenv("ADDRESS"))
    except:
        print("Env not working, check your .env file and try again or:")
        PROXY, PORT, USER, PASSWORD = input("Enter your proxy (ip:port:user:pass): ").strip().split(":")
else:
    PROXY, PORT, USER, PASSWORD = input("Enter your proxy (ip:port:user:pass): ").strip().split(":")
    LINK = input("Enter your family joining link: ")
    address = input("Enter your address joining : ")
account_num = int(input("How many accounts you want to create: "))
print("The Link is :", LINK)
print("Address :", address)
print('Proxy: ',USER, PASSWORD, PROXY, PORT)
# print(address)
# api_key = os.getenv("api_key")
# key = os.getenv("key")
def fill_address(driver, address):
    global stop_event
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
            stop_event.set()
            print("YOU LINK IS FULL, WILL TRY TO GET NEW LINK NEXT TIME...")
            # print("-------------------------------------------------------------------------------------")
            # print(driver.find_element("tag name", "body").text)
            # print("-------------------------------------------------------------------------------------")
            total_bytes = sum(len(request.response.body) for request in driver.requests if request.response)

            # Convert bytes to MB
            total_mb = total_bytes / (1024 * 1024)

            print(f"Total Data Transferred: {total_mb:.2f} MB")
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
                driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
                print("form submitted again")
            else:
                while True:
                    actions = ActionChains(driver)
                    actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]')).pause(0.5).click().perform()
                    print("form confirmed")
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.invisibility_of_element_located((By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]'))
                        )
                    except Exception as e:
                        print('line 116 main', e)
                        # actions = ActionChains(driver)
                        # actions.move_to_element(
                        #     driver.find_element(By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]')).pause(
                        #     0.5).click().perform()
                        try:
                            driver.find_element(By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]').click()
                        except Exception as e:
                            print('line 124 main,', e)
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
    global done_counter
    sp = SpotifyGenerator()
    playlist_links = [item.strip() for item in C_Fichier("playlists.txt").Fichier_to_Liste()]


    # sp.get_driver(user=USER, password=PASSWORD, proxy=PROXY, port=PORT)

    thread1 = threading.Thread(target=sp.get_driver, args=(USER, PASSWORD, PROXY, PORT))
    # thread1 = threading.Thread(target=sp.get_driver)
    thread2 = threading.Thread(target=sp.get_Email_from_yopmail)
    # thread22 = threading.Thread(target=main)

    thread1.start()
    thread2.start()
    # thread22.start()

    thread1.join()
    thread2.join()



    # sp.get_driver()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.get_site()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    # sp.get_Email_from_yopmail()
    #sp.go_to_signup()
    sp.fill_email_and_confrm()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.remove_descrections()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.fill_password()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.fill_displayed_name()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.fill_date_of_birth()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.fill_gender()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.submit_signup_button()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    if sp.hit_continue():
        return
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    sp.check_login_signup()
    # saving the account
    sp.save_data()
    print(sp.email, sp.password)

    sp.remove_descrections()
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    # sp.get_site("https://www.spotify.com/ng/family/join/invite/0cby9X4YCzCc7XB/".replace("invite", "confirm"))
    sp.get_site(LINK.replace("invite", "address"))
    if stop_event.is_set():
        sp.quit()
        print("ENOUGH ACCOUNT QUITING...")
        return
    fill_address(driver=sp.driver, address=address)
    # print('sleeping...120')
    # time.sleep(120)


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
        sp.calculate_usage()
        sp.quit()
        exit()
    else:
        with counter_lock:
            done_counter += 1
            print(f"done ({done_counter}/{account_num})")

            if done_counter >= account_num:
                stop_event.set()
        sp.save_data(file_name="premium_data.txt")
        # time.sleep(3000)
        if len(playlist_links) != 0:
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
        else:
            print("No links to add")
        sp.calculate_usage()
        sp.quit()

        exit()

def run_threads(num_threads):
    """Runs 'num_threads' in parallel and waits for all to complete."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(main) for _ in range(num_threads)}
        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
        print("All threads completed.")


if __name__ == "__main__":
    print("Starting...")
    # main()
    # exit()
    n = int(input("Enter the number of threads : "))
    # f = input("full (y/n) : ")

    if n < 1 :
        print("Invalid number")
    else:
        if n == account_num:
            while True:
                if done_counter == account_num:
                    print("Finished")
                    exit()
                else:
                    print("Runing Threads...")
                    run_threads(account_num-done_counter)



                # Check if we should stop before restarting
                # if stop_event.is_set():
                #     break
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
                futures = {executor.submit(main) for _ in range(n)}

                while not stop_event.is_set():
                    done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                    print(f"Active Threads: {len(futures)}")
                    for future in done:
                        futures.remove(future)

                        if stop_event.is_set():
                            break

                        futures.add(executor.submit(main))

                    time.sleep(2)

            print("All threads stopped. Exiting program.")
# if __name__ == "__main__":
#     # asyncio.run(main())
#     # main()
#
#     print("starting")
#     n = int(input("Enter the number of threading: "))
#     i = 0
#     while True:
#         if i != 0:
#             print("Starting again in 2 seconds...")
#             time.sleep(2)
#         if i == 10:
#             break
#         i += 1
#         if n == 1:
#             main()
#         elif n == 2:
#             thread1 = threading.Thread(target=main)
#             thread2 = threading.Thread(target=main)
#
#             thread2.start()
#             thread1.start()
#
#             thread1.join()
#             thread2.join()
#         elif n == 3:
#             thread1 = threading.Thread(target=main)
#             thread2 = threading.Thread(target=main)
#             thread22 = threading.Thread(target=main)
#
#             thread2.start()
#             thread1.start()
#             thread22.start()
#
#             thread1.join()
#             thread2.join()
#             thread22.join()
#         elif n == 4:
#             thread1 = threading.Thread(target=main)
#             thread2 = threading.Thread(target=main)
#             thread22 = threading.Thread(target=main)
#             thread222 = threading.Thread(target=main)
#
#             thread2.start()
#             thread1.start()
#             thread22.start()
#             thread222.start()
#
#             thread1.join()
#             thread2.join()
#             thread22.join()
#             thread222.join()
#         else:
#             print("Try again (choose a number between 1 and 4")
#             break
