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

    liked_songs_div = WebDriverWait(sp.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Liked Songs"]'))
    )

    # Get the aria-rowcount attribute
    row_count = int(liked_songs_div.get_attribute("aria-rowcount"))
    if row_count == 0:
        return
    print("You have :", row_count, "songs")
    liked_songs = set()
    while True:
        # scroll_to_buttom(driver=sp.driver)
        _ = WebDriverWait(sp.driver,40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="internal-track-link"]')))
        links = sp.driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="internal-track-link"]')
        for link in links:
            liked_songs.add(link.get_attribute("href"))
        print(liked_songs)
        element = sp.driver.find_element("css selector", f"[aria-rowindex='{len(liked_songs)}']")
        sp.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(3)
        # print(len(liked_songs))
        # print(row_count-1)
        if len(liked_songs) == row_count-1:
            break

    if liked_songs:
        for h in liked_songs:
            print(h)


    # time.sleep(200)
        # time.sleep(2)

    # Print the extracted links
    # print(hrefs)
    playlist_link.extend(liked_songs)
    playlist_file = C_Fichier("playlists.txt")
    playlist_file.list_to_fichier(playlist_link)
    print(playlist_link)
    print("playlists links saved successfully")
    # time.sleep(100)
    sp.quit()
    return
    # return playlist_link


if __name__ == "__main__":
    get_playlist_link()

