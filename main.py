# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:49:13 2023

@author: HP
"""

import time
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from interaction import SpotifyGenerator
from class_fichier import C_Fichier

def fill_address(driver, address):
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="address"]'))
        )
    except:
        print("NOTE: No address there")
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
            time.sleep(1)
            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[//text()[contains(., 'Confirm')]]"))
                )
            except:
                print("NOTE: No confirm there")
            else:
                actions = ActionChains(driver)
                actions.move_to_element(driver.find_element(By.CSS_SELECTOR, 'button[data-encore-id="buttonPrimary"]')).pause(0.5).click().perform()
                print("form confirmed")
                # try:
                #     WebDriverWait(driver, 2).until(
                #         EC.element_to_be_clickable((By.XPATH, "//button[//text()[contains(., 'Confirm')]]"))
                #     )
                # except:
                #     print("NOTE: No confirm there")
                # else:
                #     driver.find_element(By.XPATH, "//button[//text()[contains(., 'Confirm')]]").click()
                #     print("form confirmed again")



def main():
    sp = SpotifyGenerator()
    playlist_links = [item.strip() for item in C_Fichier("playlists.txt").Fichier_to_Liste()]


    sp.get_driver(user="kheYdSdd", password="LGsFYFAY", proxy="45.199.205.7", port='64848')
    sp.get_site()
    sp.get_Email_from_yopmail()
    #sp.go_to_signup()
    sp.fill_email_and_confrm()
    sp.remove_descrections()
    sp.fill_password()
    # time.sleep(100)
    sp.fill_displayed_name()
    sp.fill_date_of_birth()
    sp.fill_gender()
    sp.submit_signup_button()
    # sp.check_capSolver()
    sp.hit_continue()
    sp.check_login_signup()

    # sp.get_site("https://www.spotify.com/ng/family/join/invite/0cby9X4YCzCc7XB/".replace("invite", "confirm"))
    sp.get_site("https://www.spotify.com/ng/family/join/invite/0cby9X4YCzCc7XB/".replace("invite", "address"))
    address = "121 Apapa Rd, Ebute Metta, Lagos 101245, Lagos, Nigeria"
    fill_address(driver=sp.driver, address=address)

    # CHECK THING
    try:
        WebDriverWait(sp.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Welcome to Spotify Family')]")
            ))
    except:
        print("something not working")
        sp.quit()
    else:


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

        print("sleeping2000")
        time.sleep(20000)
        sp.quit()
        # sp.cc_premium_activator()
        # L = sp.export_data()
        # L.append(date.today())
        #
        #
        # #file.creer_fichier_1()
        # file.Liste_to_str_to_Fichier(L)
    return

if __name__ == "__main__":
    # main()
    import threading
    print("starting")
    thread1 = threading.Thread(target=main)
    thread2 = threading.Thread(target=main)

    thread2.start()
    thread1.start()

    thread1.join()
    thread2.join()
