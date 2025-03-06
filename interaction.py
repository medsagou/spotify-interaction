# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:49:39 2023

@author: HP
"""

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time

# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select

import undetected_chromedriver as uc

from Module_cc import CC_Class
from class_fichier import C_Fichier
import os
curr_dir = os.getcwd()
class SpotifyGenerator:
    def __init__(self, password="yourPassword"):
        self.driver = ""
        self.email = ""
        self.password = password
        # self.extenstion = "xk-en"
        self.cc_file_name = "cc.txt"
        self.regected_cc_file_name = "cc_regected.txt"
        self.data_file = "data.txt"
        self.extenstion = "xk-en"
        self.address_file_name = "address.txt"

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--load-extension={0}".format(curr_dir + "/CapSolver"))
        options.add_argument("--lang=en")
        # options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        proxy_options = {
            'proxy': {
                'http': 'http://kheYdSdd:LGsFYFAY@45.199.205.7:64848',
                'https': 'http://kheYdSdd:LGsFYFAY@45.199.205.7:64848',
                'no_proxy': 'localhost:127.0.0.1'
            }
        }

        ## Set Up Selenium Chrome driver
        # driver = webdriver.Chrome(seleniumwire_options=proxy_options)
        driver = webdriver.Chrome(options=options)

        self.driver = driver
        self.driver.maximize_window()
        # self.driver.get("https://www.google.com/recaptcha/api2/demo")
        # self.check_capSolver()
        # self.driver.get("https://nowsecure.nl")
        # self.driver.get("https://bot.sannysoft.com/")
        # time.sleep(600)

        self.driver.get(f"https://www.spotify.com/signup")
        # time.sleep(300)
        # print("NOTE: DRIVER CONNECTED")
        # print("here")
        # driver = webdxriver.Chrome()
        print("NOTE: DRIVER CONNECTED")
        return

    def check_capSolver(self):
        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Terms')]"))
                )
            except:
                print("still looping")
            else:
                break
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="capsolver-solver-tip-button"]'))
            )
            print("Recaptcha found.")
            print("solving...")
            try:
                WebDriverWait(self.driver, 100).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Captcha solved!')]"))
                )
                print("Captcha solved!")
                return True
            except:
                print("no text found")
                return False
        except:
            print("no text found")
            return False


    def hit_continue(self):
        if self.check_capSolver():
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[span[text()='Continue']]"))
                )
            except:
                print("no Continue text found")
            else:
                continue_btn = self.driver.find_element(By.XPATH,"//button[span[text()='Continue']]")
                continue_btn.click()
                print("continue clicked")
                while True:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.invisibility_of_element_located((By.XPATH, "//button[span[text()='Continue']]"))
                        )
                    except:
                        continue_btn = self.driver.find_element(By.XPATH, "//button[span[text()='Continue']]")
                        continue_btn.click()
                    else:
                        print("we've finished!!")
                        break

        else:
            print("no captcha so no continue")
    def get_Email_from_yopmail(self):
        yopmail_url = "https://yopmail.com/email-generator"
        response = requests.get(yopmail_url)
        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")

        email_element_container = soup.find(id="geny")
        self.email = email_element_container.get_text()
        print("NOTE: GETTING EMAIL DONE, THE EMAIL IS;", self.email)
        return

    def go_to_signup(self):
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".Button-sc-1dqy6lx-0.jjtmnk.sibxBMlr_oxWTfBrEz2G",
                    )
                )
            )
        finally:
            go_signup = self.driver.find_elements(
                By.CSS_SELECTOR, ".Button-sc-1dqy6lx-0.jjtmnk.sibxBMlr_oxWTfBrEz2G"
            )
            if len(go_signup) != 0:
                go_signup[0].click()

        return

    def remove_descrections(self):
        policy_close_button = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon",
        )
        if len(policy_close_button) != 0:
            policy_close_button[0].click()
            print("NOTE: REMOVED POLICY")

        try:
            cookies_button = self.driver.find_element(
                By.ID, "onetrust-accept-btn-handler"
            )
        except:
            print("NOTE: No cookies there")
        else:
            cookies_button.click()
            print("REMOVE COOKIES")

        return

    def submit(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-testid="submit"]'))
            )
        except:
            print("NOTE: No submit there")
        else:

            submit = self.driver.find_element(By.XPATH, '//*[@data-testid="submit"]')
            # print('working')
            time.sleep(1)

            submit.click()
        return

    def fill_displayed_name(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "displayName"))
            )
        except:
            print("NOTE: No name there")
        else:
            display_name_field = self.driver.find_element(By.ID, "displayName")
            display_name_field.send_keys("your name")
        return

    def fill_password(self):

        passwordtext = "yourPassword88"
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "new-password"))
            )
        except:
            print("NOTE: No password there")

        else:
            password = self.driver.find_element(By.ID, "new-password")
            password.send_keys(passwordtext)

        self.submit()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "new-password"))
            )
        except:
            self.submit()


        return

    def fill_date_of_birth(self):
        day_field = self.driver.find_element(By.ID, "day")
        day_field.send_keys("01")

        year_field = self.driver.find_element(By.ID, "year")
        year_field.send_keys("1990")

        month_dropdown = Select(self.driver.find_element(By.ID, "month"))
        month_dropdown.select_by_index(2)
        # time.sleep(100)
        return

    def fill_email_and_confrm(self):
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            print("we didn't find email field")
        else:
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(self.email)
            self.submit()

        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.ID, "username"))
                )
            except:
                self.submit()
            else:
                print("email field finished")
                break


        # time.sleep(2)
        # self.submit()
        # print("submit 2")
        return

    def fill_gender(self):
        gender_radiobutton = self.driver.find_elements(
            By.CSS_SELECTOR, ".Indicator-sc-hjfusp-0"
        )
        if len(gender_radiobutton) != 0:
            gender_radiobutton[0].click()
        else:
            gender_radiobutton2 = self.driver.find_elements(
                By.CSS_SELECTOR, ".Indicator-sc-hjfusp-0.dFGMcY"
            )
            gender_radiobutton2[0].click()
        self.submit()

    def submit_signup_button(self):
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sign up')]"))
            )
            print("Sign up text found")
            self.submit()
        except:
            print("Sign up text not found")
        # print('sleeping')
        # time.sleep(200)
        return

    def submit_form(self):
        # submit the form
        submit_button = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".ButtonInner-sc-14ud5tc-0.dqLIWu.encore-bright-accent-set.SignupButton___StyledButtonPrimary-cjcq5h-1.jazsmO",
        )
        submit_button[0].click()
        print("NOTE: FORM SUBMITED")
        # time.sleep(5)
        # try:
        #     iframe_recaPTCHA = WebDriverWait(self.driver, 100).until(
        #         EC.presence_of_element_located(
        #             (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')
        #         )
        #     )
        # except:
        #     print("NOTE: RECAPTCHA NOT REQUIRED")
        # finally:
        #     print("NOTE: PRESENCE OF RECAPTCHA")
        #     self.driver.switch_to.frame(iframe_recaPTCHA)
        #     print("NOTE: SWITCH TO IFRAME PAYMENT")
        #     click_checkbox = self.driver.find_elements(
        #         By.CSS_SELECTOR, ".recaptcha-checkbox-border"
        #     )
        #     click_checkbox[0].click()
        #     print("NOTE: RECAPTCHA CLICKED")

        #     time.sleep(100)
        return

    def cc_premium_activator(self):
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".mh-header-primary.svelte-vf0pv9")
                )
            )
        finally:
            go_premium = self.driver.find_elements(
                By.CSS_SELECTOR, ".mh-header-primary.svelte-vf0pv9"
            )
            if len(go_premium) != 0:
                go_premium[0].click()
                try:
                    WebDriverWait(self.driver, 100).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".ButtonInner-sc-14ud5tc-0")
                        )
                    )
                finally:
                    go_to_plan_page = self.driver.find_elements(
                        By.CSS_SELECTOR, ".ButtonInner-sc-14ud5tc-0"
                    )
                    if len(go_to_plan_page) != 0:
                        go_to_plan_page[0].click()
                        # check if the pyement coutnry is usa
                        self.check_pyment_country()
                        # end check if the pyement coutnry is usa

                        # fill adress infromation

                        self.fill_adress_information()

                        # end fill adress infromation

                        try:
                            WebDriverWait(self.driver, 100).until(
                                EC.presence_of_element_located(
                                    (By.CSS_SELECTOR, ".Indicator-sc-hjfusp-0.bRvWKL")
                                )
                            )
                        finally:
                            self.remove_descrections()
                            try:
                                go_to_cc_form = self.driver.find_elements(
                                    By.CSS_SELECTOR, ".Indicator-sc-hjfusp-0.bRvWKL"
                                )
                            except:
                                self.try_ccs()
                            else:
                                if len(go_to_cc_form) > 2:
                                    go_to_cc_form[1].click()
                                elif len(go_to_cc_form) == 2:
                                    go_to_cc_form[0].click()

                                self.try_ccs()

            # driver.quit()
            print("NOTE: ACCOUNT IS CREATED")
        return

    def check_pyment_country(self):
        current_url = self.driver.current_url
        finaleUrl = ""
        if "country=US" not in current_url:
            splited_url = current_url.split("&")
            for element in splited_url:
                if "country" in element:
                    finaleUrl = finaleUrl + "country=US" + "&"
                else:
                    finaleUrl = finaleUrl + element + "&"
            self.driver.get(finaleUrl)
        return

    def fill_adress_information(self):
        addressFile = C_Fichier(self.address_file_name)
        addressList = addressFile.Fichier_to_Liste()
        if len(addressList) != 4:
            print("ERROR: THE ADDRESS FILE NOT COMPLETED")
            exit
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "address-street"))
            )
        finally:
            # adrees street
            address_street_field = self.driver.find_element(By.ID, "address-street")
            address_street_field.send_keys(addressList[0].replace("\n", ""))

            # adrees city
            address_street_field = self.driver.find_element(By.ID, "address-city")
            address_street_field.send_keys(addressList[1].replace("\n", ""))

            # select the state
            select_element = self.driver.find_element(By.ID, "address-state")
            select = Select(select_element)
            select.select_by_visible_text(addressList[2].replace("\n", ""))

            # select zip code
            zip_code_field = self.driver.find_element(
                By.ID, "address-postal_code_short"
            )
            zip_code_field.send_keys(addressList[3].replace("\n", ""))

    def try_ccs(self):
        cc_file = C_Fichier(self.cc_file_name)
        regected_cc_file = C_Fichier(self.regected_cc_file_name)
        ccs = cc_file.Fichier_to_Liste()
        regected_ccs = regected_cc_file.Fichier_to_str()
        for cc in ccs:
            cc_splited = cc.split("|")
            if cc_splited[0] not in regected_ccs:
                credit_card = CC_Class(self.driver, cc_splited)
                credit_card.fill_cc_input()
                try:
                    WebDriverWait(self.driver, 100).until(
                        EC.invisibility_of_element_located(
                            (By.CSS_SELECTOR, 'div[data-testid="loading-indicator"]')
                        )
                    )
                finally:
                    try:
                        self.driver.find_element(
                            By.CSS_SELECTOR,
                            "Wrapper-sc-62m9tu-0.jieDxt.encore-negative-set",
                        )
                    except:
                        print("NOTE: CC REGECTED")
                        regected_cc_file.str_to_fichier(cc)
                    else:
                        self.export_account_data()
                        print(
                            "NOTE: ACCOUNT IS CREATED, CHECK THE FILE {}".format(
                                self.data_file
                            )
                        )
                        return
            else:
                continue

    def export_data(self):
        return [self.email, self.password]

    def close_tab(self):
        self.driver.quit()

    def main_spotify(self):
        self.get_driver()
        self.get_Email_from_yopmail()
        self.remove_descrections()
        self.fill_email_and_confrm()
        self.fill_password()
        self.fill_displayed_name()
        self.fill_date_of_birth()
        self.fill_gender()
        self.submit_form()
        self.cc_premium_activator()

    pass
