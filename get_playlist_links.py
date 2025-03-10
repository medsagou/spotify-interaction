from interaction import SpotifyGenerator
from class_fichier import C_Fichier
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_playlist_link():
    playlist_link = []
    # get account
    cF = C_Fichier(NF='ref_account.txt')
    account, password = cF.Fichier_to_Liste()
    print("main account is :", account)

    # login system
    sp = SpotifyGenerator()
    sp.email = account.strip()
    sp.get_driver()
    sp.get_site(site='https://www.spotify.com/login')
    sp.fill_email_login()
    sp.fill_password_login(password.strip())
    sp.submit_login()

    # check Login
    # print("cheking login...")
    sp.check_login_signup(login=1)

    print("Getting the Site")
    sp.get_site('https://open.spotify.com/')



    # Extract the aria-labelledby from the <div> inside each <li>
    labels = []
    print("Start lopping...")
    # print("-------------------------------------------------------------------------------------")
    # print(sp.driver.find_element("tag name", "body").text)
    # print("-------------------------------------------------------------------------------------")
    while True:
        ul = WebDriverWait(sp.driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[aria-label="Your Library"]')))
        list_items = ul.find_elements(By.TAG_NAME, "li")
        print("looping through the list...\n note: if this take too much just restart the script".upper())
        for li in list_items:
            try:
                div = li.find_element(By.TAG_NAME, "div")
                aria_labelledby = div.get_attribute("aria-labelledby")
                if aria_labelledby:
                    labels.append(aria_labelledby)
                    print(aria_labelledby)
            except:
                pass
        time.sleep(1)
        if labels != []:
            break
    playlist_link = []
    for label in labels:
        if "collection" in label:
            continue
        playlist_link.append("https://open.spotify.com/playlist/"+label.split(":")[-1])
    # print(playlist_link)


    print("Getting Liked song link...")
    sp.get_site("https://open.spotify.com/collection/tracks")

    while True:
        _ = WebDriverWait(sp.driver,40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="internal-track-link"]')))
        links = sp.driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="internal-track-link"]')
        hrefs = [link.get_attribute("href") for link in links]
        if hrefs != []:
            for h in hrefs:
                print(h)
            break
        # time.sleep(2)

    # Print the extracted links
    # print(hrefs)
    playlist_link.extend(hrefs)
    playlist_file = C_Fichier("playlists.txt")
    playlist_file.list_to_fichier(playlist_link)
    print(playlist_link)
    print("playlists links saved successfully")
    # time.sleep(100)
    sp.quit()
    return
    # return playlist_link


if __name__ == "__main__":
    while True:
        try:
            get_playlist_link()
        except:
            pass
        else:
            break
