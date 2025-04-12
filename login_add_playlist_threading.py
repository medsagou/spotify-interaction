from interaction import SpotifyGenerator
from class_fichier import C_Fichier

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# load_dotenv()
#
# USER = str(os.getenv("USER_PORXY"))
# PASSWORD = str(os.getenv("PASSWORD"))
# PROXY = str(os.getenv("PROXY"))
# PORT = str(os.getenv("PORT"))
#
from concurrent.futures import ThreadPoolExecutor
import time

def worker(link, cookies, local_storage):
    # Start new driver
    sp = SpotifyGenerator()
    sp.get_driver()

    try:
        # Open the site first so we can set cookies
        sp.driver.get("https://www.spotify.com")  # This matches the domain where login was performed

        # Filter cookies for the current domain
        for cookie in cookies:
            # Some cookies might be for open.spotify.com or www.spotify.com
            # We must ensure we're setting cookies only for the current domain
            if "spotify.com" in cookie.get("domain", ""):
                # Adjust domain to current one if necessary
                cookie["domain"] = ".spotify.com"
                try:
                    sp.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Error adding cookie {cookie.get('name')}: {e}")
        print('sleeping')
        time.sleep(20)
        # Set localStorage
        sp.driver.execute_script(f"""
            var items = JSON.parse('{local_storage}');
            for (var key in items) {{
                localStorage.setItem(key, items[key]);
            }}
        """)

        time.sleep(200)

        sp.driver.get(link)

        try:
            WebDriverWait(sp.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="add-button"]'))
            )
            sp.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="add-button"]').click()
            print("Done:", link)
        except Exception as e:
            print("Failed:", link)
            print(e)
    except Exception as e:
        print(e)
    finally:
        sp.quit()




def get_playlist_link():
    account, password = input("Enter your ref account (email:password): ").strip().split(":")
    print("main account is :", account)

    sp = SpotifyGenerator()
    sp.email = account.strip()

    if input("You want to use proxy? (y/n): ").lower() == "y":
        PROXY, PORT, USER, PASSWORD = input("Enter your proxy (ip:port:user:pass): ").strip().split(":")
        sp.get_driver(user=USER, password=PASSWORD, proxy=PROXY, port=PORT, get_playlist=True)
    else:
        sp.get_driver(get_playlist=True)

    sp.get_site('https://www.spotify.com/login')
    sp.fill_email_login()
    sp.fill_password_login(password.strip())
    sp.submit_login()
    sp.check_login_signup(login=1)

    # Extract session
    cookies = sp.driver.get_cookies()
    local_storage = sp.driver.execute_script("return JSON.stringify(localStorage);")

    playlist_links = [item.strip() for item in C_Fichier("playlists.txt").Fichier_to_Liste()]
    if not playlist_links:
        print("No links to add")
        sp.quit()
        return

    # Multithreading
    with ThreadPoolExecutor(max_workers=1) as executor:
        for link in playlist_links:
            executor.submit(worker, link, cookies, local_storage)

    sp.quit()

if __name__ == '__main__':
    get_playlist_link()