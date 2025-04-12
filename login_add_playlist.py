from interaction import SpotifyGenerator
from class_fichier import C_Fichier
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

# load_dotenv()
#
# USER = str(os.getenv("USER_PORXY"))
# PASSWORD = str(os.getenv("PASSWORD"))
# PROXY = str(os.getenv("PROXY"))
# PORT = str(os.getenv("PORT"))
#




def get_playlist_link():
    playlist_link = []
    # get account
    # cF = C_Fichier(NF='ref_account.txt')
    # account, password = cF.Fichier_to_Liste()
    account, password = input("Enter your ref account (email:password): ").strip().split(":")
    print("main account is :", account)

    # login system
    sp = SpotifyGenerator()
    sp.email = account.strip()
    while True:
        test = input("You want to use proxy? (y/n): ")
        if test.lower() == "y":
            PROXY, PORT, USER, PASSWORD = input("Enter your proxy (ip:port:user:pass): ").strip().split(":")
            print(USER, PASSWORD, PROXY, PORT)
            sp.get_driver(user=USER, password=PASSWORD, proxy=PROXY, port=PORT, get_playlist=True)
            break
        elif test.lower() == "n":
            sp.get_driver(get_playlist=True)
            break

    sp.get_site(site='https://www.spotify.com/login')
    sp.fill_email_login()
    sp.fill_password_login(password.strip())
    sp.submit_login()

    # check Login
    # print("cheking login...")
    sp.check_login_signup(login=1)
    playlist_links = [item.strip() for item in C_Fichier("playlists.txt").Fichier_to_Liste()]
    if len(playlist_links) != 0:
        for link in playlist_links:
            sp.get_site(link)
            try:
                _ = WebDriverWait(sp.driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="add-button"]')))
            except Exception as e:
                print("Eroor:", link)
                with open("errored_links.txt", 'a') as f:
                    f.write(link)
                    f.write('\n')
                print("-------------------------------------------------------------------------------------")
                print(sp.driver.find_element("tag name", "body").text)
                print("-------------------------------------------------------------------------------------")
                # print(e)
                continue
            else:
                button = sp.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="add-button"]')
                button.click()
                print("Done:", link)
                time.sleep(1)
    else:
        print("No links to add")
    # sp.calculate_usage()
    sp.quit()
    return
    # return playlist_link


if __name__ == "__main__":
    get_playlist_link()

