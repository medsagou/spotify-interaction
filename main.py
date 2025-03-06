# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:49:13 2023

@author: HP
"""

import requests
from bs4 import BeautifulSoup

from datetime import date

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from interaction import SpotifyGenerator
from class_fichier import C_Fichier


def main():
    sp = SpotifyGenerator()
    file = C_Fichier("data.txt")
    
    sp.get_driver()
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
    print("sleeping2000")
    time.sleep(2000)
    # sp.cc_premium_activator()
    L = sp.export_data()
    L.append(date.today())

    
    #file.creer_fichier_1()
    file.Liste_to_str_to_Fichier(L)
    
    
    
    
    return

if __name__ == "__main__":
    main()
    # import threading
    # print("starting")
    # thread1 = threading.Thread(target=main)
    # thread2 = threading.Thread(target=main)
    #
    # thread2.start()
    # thread1.start()
    #
    # thread1.join()
    # thread2.join()
