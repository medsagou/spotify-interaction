# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:49:39 2023

@author: HP
"""
import string
import requests
from faker import Faker
import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import secrets

from Module_cc import CC_Class
from class_fichier import C_Fichier
import os
curr_dir = os.getcwd()
class SpotifyGenerator:
    def __init__(self):
        self.driver = ""
        self.email = ""
        self.password = self.generate_password()
        # self.extenstion = "xk-en"
        self.cc_file_name = "cc.txt"
        self.regected_cc_file_name = "cc_regected.txt"
        self.data_file = "data.txt"
        self.extenstion = "xk-en"
        self.address_file_name = "address.txt"
        self.retry_count = 0

    # def generate_password(self):
    #     chars = string.ascii_letters + string.digits + string.punctuation
    #     while True:
    #         password = ''.join(random.choices(chars, k=14))
    #         if (any(c.isupper() for c in password) and
    #                 any(c.isdigit() for c in password) and
    #                 any(c in string.punctuation for c in password)):
    #             return password

    def calculate_usage(self):
        total_bytes = sum(len(request.response.body) for request in self.driver.requests if request.response)

        # Convert bytes to MB
        total_mb = total_bytes / (1024 * 1024)

        print(f"Total Data Transferred: {total_mb:.2f} MB")
        return total_mb
    def generate_password(self, length=20):
        allowed_punctuation = string.punctuation.replace(":", "").replace("'", "").replace("`", "")

        # Ensure at least one special character (excluding `:`)
        punctuation_char = secrets.choice(allowed_punctuation)

        # Generate the rest of the password using letters and digits only
        characters = string.ascii_letters + string.digits
        password_body = ''.join(secrets.choice(characters) for _ in range(length - 1))

        # Convert password to a list and insert the punctuation at a non-first position
        password = list(password_body)
        insert_position = secrets.randbelow(length - 1) + 1  # Ensures it's not at position 0
        password.insert(insert_position, punctuation_char)

        return ''.join(password)
    def get_driver(self, user="", password="", proxy="", port=""):
        options = webdriver.ChromeOptions()
        options.add_argument("--load-extension={0}".format(curr_dir + "/CapSolver"))
        options.add_argument("--lang=en")
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-images")
        options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")

        # options.add_argument("--disk-cache-size=4096")
        # options.add_argument("--disk-cache-dir=/tmp/cache")
        # options.set_capability("pageLoadStrategy", "none")
        # options.add_argument("--guest")
        # ubuntu
        # options.add_argument("--user-data-dir=/tmp/selenium_profile")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # service = Service("/usr/local/bin/chromedriver")
        service = Service()
        ## Set Up Selenium Chrome driver
        if user == "" or password == "" or proxy == "" or port == "":
            print("getting the driver...")
            driver = webdriver.Chrome(options=options, service=service)
        else:
            proxy_options = {
                'proxy': {
                    'http': f'http://{user}:{password}@{proxy}:{port}',
                    'https': f'http://{user}:{password}@{proxy}:{port}',
                    'no_proxy': 'localhost:127.0.0.1'
                },
                # 'disable_encoding': True,
            }
            driver = webdriver.Chrome(seleniumwire_options=proxy_options, options=options, service=service)


        def block_unwanted_requests(request):
            if request.url.endswith(('.jpg', '.png', '.gif', '.css')):
                request.abort()

        self.driver = driver
        self.driver.request_interceptor = block_unwanted_requests
        # self.driver.maximize_window()
        # self.driver.get("https://www.google.com/recaptcha/api2/demo")
        # self.driver.get("https://www.myip.com/")
        # time.sleep(200)
        # self.check_capSolver()
        # self.driver.get("https://nowsecure.nl")
        # self.driver.get("https://bot.sannysoft.com/")
        # time.sleep(600)

        # time.sleep(300)
        # print("NOTE: DRIVER CONNECTED")
        # print("here")
        # driver = webdxriver.Chrome()
        print("NOTE: DRIVER CONNECTED")
        return
    def get_site(self, site = "https://www.spotify.com/signup"):
        try:
            self.driver.get(site)
        except Exception as e:
            print(e)
            self.quit()
            exit()
        return
    def check_capSolver(self):
        i = 0
        while True:
            i+=1
            if i >= 10:
                i = 0
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sign up')]"))
                    )
                    print("Sign up text found")
                    self.submit()
                except:
                    print("Sign up button not found")
                    exit()

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
                print("no Capsolver found")
                return False
        except:
            print("no Capsolver tip button found")
            return False


    def hit_continue(self):
        if self.check_capSolver():
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Continue']]"))
                )
            except:
                print("no Continue text found")
                self.check_login_signup()
                return False
            else:
                continue_btn = self.driver.find_element(By.XPATH,"//button[span[text()='Continue']]")

                actions = ActionChains(self.driver)
                actions.move_to_element(continue_btn).pause(0.5).click().perform()
                # continue_btn.click()
                print("continue clicked")
                while True:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.invisibility_of_element_located((By.XPATH, "//button[span[text()='Continue']]"))
                        )
                    except:
                        try:
                            continue_btn = self.driver.find_element(By.XPATH, "//button[span[text()='Continue']]")
                            continue_btn.click()
                        except:
                            pass
                    else:
                        self.check_login_signup()
                        break

        else:
            # print(self.driver.find_element("tag name", "body").text)
            print("no captcha so no continue")
            self.check_login_signup()
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
        try:
            policy_close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                By.CSS_SELECTOR,
                ".onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon",
            ))
            if len(policy_close_button) != 0:
                try:
                    policy_close_button[0].click()
                    print("NOTE: REMOVED POLICY")
                except:
                    print("expection line 226 interaction.py")

            try:
                cookies_button = self.driver.find_element(
                    By.ID, "onetrust-accept-btn-handler"
                )
            except:
                print("NOTE: No cookies there")
            else:
                cookies_button.click()
                print("REMOVE COOKIES")
        except:
            print("Exception line 240 interaction.py")

        return

    def submit_login(self):
        try:
            cookies_button = self.driver.find_element(
                By.ID, "login-button"
            )
        except:
            print("NOTE: No submit found")
        else:
            cookies_button.click()
            print("Form submitted")
    def submit(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@data-testid="submit"]'))
            )
        except:
            print("NOTE: No submit there")
        else:

            submit = self.driver.find_element(By.XPATH, '//*[@data-testid="submit"]')
            # print('working')
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", submit)
            # submit.click()
        return

    def check_login_signup(self, login = 0):
        print("checking login/signup...")
        try:
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Something went wrong')]")
                ))
        except:
            pass
        else:
            print("Something went wrong with captcha, retrying..")
            self.driver.refresh()
            self.hit_continue()
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[aria-controls="profileMenu"]')
                ))
        except Exception as e:
            if self.retry_count >= 3:
                print("3 attempts reached. Exiting script. (starting new account)")
                self.quit()
                exit()
            self.retry_count += 1
            print("error with captcha, retrying..")

            # print(self.driver.find_element("tag name", "body").text)


            self.driver.refresh()
            self.hit_continue()
        else:
            print("Login/signup success")
            if login == 0:
                return True

    def save_data(self, file_name='data.txt'):
        data_file = C_Fichier(file_name)
        # data_file.Liste_to_str_to_Fichier([self.email, self.password, datetime.now().strftime("%Y-%m-%d")])
        data_file.Liste_to_str_to_Fichier([self.email, self.password])

    def fill_displayed_name(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "displayName"))
            )
        except:
            print("NOTE: No name there")
        else:
            display_name_field = self.driver.find_element(By.ID, "displayName")
            fake = Faker()
            display_name_field.send_keys(fake.name())
        return

    def fill_password_login(self, password_text):
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "login-password"))
            )
        except:
            print("NOTE: No password there")

        else:
            password = self.driver.find_element(By.ID, "login-password")
            password.send_keys(password_text)
    def fill_password(self):

        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "new-password"))
            )
        except:
            print("NOTE: No password there")

        else:
            password = self.driver.find_element(By.ID, "new-password")
            password.send_keys(self.password)

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


    def fill_email_login(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-username"))
            )
        except:
            print("we didn't find email field")
        else:
            email_field = self.driver.find_element(By.ID, "login-username")
            email_field.send_keys(self.email)
            print('email done')
    def fill_email_and_confrm(self):
        try:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
        except:
            print("we didn't find email field")
        else:
            # self.remove_descrections()
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(self.email)
            # try:
            #     # Find and click the cookie accept button
            #     cookie_button = self.driver.find_element(By.ID, "onetrust-pc-btn-handler")
            #     cookie_button.click()
            #     time.sleep(2)  # Wait after closing popup
            # except:
            #     print("No cookie banner found")
            self.submit()

        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located((By.ID, "username"))
                )
            except:
                # print("here")
                # email_field = self.driver.find_element(By.ID, "username")
                # email_field.send_keys(self.email)
                # self.driver.save_screenshot('screenshot.png')
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
            # gender_radiobutton[0].click()
            self.driver.execute_script("arguments[0].click();", gender_radiobutton[0])
        else:
            gender_radiobutton2 = self.driver.find_elements(
                By.CSS_SELECTOR, ".Indicator-sc-hjfusp-0.dFGMcY"
            )
            # gender_radiobutton2[0].click()
            self.driver.execute_script("arguments[0].click();", gender_radiobutton2[0])
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
        # submit_button[0].click()
        self.driver.execute_script("arguments[0].click();", submit_button[0])
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

    def quit(self):
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


if __name__=="__main__":
    sp = SpotifyGenerator()
    sp.get_driver()
    sp.get_site()

    sp.fill_email_and_confrm()
    time.sleep(200)
