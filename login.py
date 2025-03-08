from interaction import SpotifyGenerator
from class_fichier import C_Fichier
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from main import fill_address
def get_playlist_link():
    playlist_link = []
    # get account
    account, password = ("sautteneucrafrau-1246@yopmail.com", "yourPassword88")
    print("main account is :", account)

    # login system
    sp = SpotifyGenerator()
    sp.email = account.strip()
    sp.get_driver(user="kheYdSdd", password="LGsFYFAY", proxy="45.199.205.7", port='64848')
    sp.get_site(site='https://www.spotify.com/login')
    sp.fill_email_login()
    sp.fill_password_login(password.strip())
    sp.submit_login()

    # check Login
    print("cheking login...")
    sp.check_login_signup()

    sp.get_site("https://www.spotify.com/ng/family/join/invite/0cby9X4YCzCc7XB/".replace("invite", "address"))
    address = "121 Apapa Rd, Ebute Metta, Lagos 101245, Lagos, Nigeria"
    fill_address(driver=sp.driver, address=address)

    time.sleep(20000)




    sp.get_site('https://open.spotify.com/playlist/43pGPIvtoeTWUDzdCDDQYu')
    try:
        _ = WebDriverWait(sp.driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="add-button"]')))
    except Exception as e:
        print(e)
    else:
        button = sp.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="add-button"]')
        button.click()
        print("button clicked")

    time.sleep(20000)


if __name__ == "__main__":
    get_playlist_link()