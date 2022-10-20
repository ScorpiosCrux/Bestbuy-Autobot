from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import info
import time
import multiprocessing as mp

#Links
RTX3080LINK1 = "https://www.bestbuy.ca/en-ca/product/asus-rog-strix-nvidia-geforce-rtx-3080-10gb-gddr6x-video-card/14954116"
#RTX3080LINK1 = "https://www.bestbuy.ca/en-ca/product/kingston-datatraveler-g3-32gb-usb-3-1-flash-drive-only-at-best-buy/13962207"
#RTX3080LINK1 = "https://www.bestbuy.ca/en-ca/product/lg-55-4k-uhd-hdr-lcd-webos-smart-tv-55un7000-2020/14760722"
#RTX3080LINK1 = "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6x-video-card/15084753"
#RTX3080LINK1 = "https://www.bestbuy.ca/en-ca/product/playstation-5-console-online-only/14962185"




def initialize_selenium():
    PATH = r"C:\Users\VividEradicator\Desktop\Bestbuy_bot\chromedriver"
    #PATH = r"/home/vivid/Desktop/RTX-3070-Best-Buy-Bot/chromedriver"
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(PATH, options=options)
    return driver
    

def clean_and_close_browser(driver):
    driver.delete_all_cookies()
    driver.close()
    driver.quit()


def rtx_loop(driver):
    counter = 150
    isComplete = False
    
    driver.get(RTX3080LINK1)
    while not isComplete:
        if counter <= 0:
            return False

        #See if the add to cart button is clickable for 15 seconds.
        try:
            atcBtn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".addToCartButton"))
            )
            
        #If that fails, then refresh the page.
        except:
            counter -= 1
            driver.refresh()
            continue

        #If the button has been found
        print("Add to cart button found")
        try:
            #Add to cart and wait a bit before moving on. Otherwise it won't add properly
            atcBtn.click()
            time.sleep(2)
            print ("Added to cart")

            #Go to the login 
            driver.get("https://www.bestbuy.ca/identity/global/signin?redirectUrl=https%3A%2F%2Fwww.bestbuy.ca%2Fcheckout%2F%3Fqit%3D1%23%2Fen-ca%2Fshipping%2FAB%2FT2N&lang=en-CA&contextId=checkout")
            print ("Redirecting to login")

            # fill in email and password
            emailField = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            emailField.send_keys(info.email)
            pwField = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            pwField.send_keys(info.password)

            # click the sign in button
            signInBtn = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div/div[1]/div/div/form/div/button"))
            )
            signInBtn.click()
            print("Signing in")

            time.sleep(5)
            # fill in card cvv
            cvvField = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, "cvv"))
            )
            cvvField.send_keys(info.cvv)
            print("cvv has been filled.")

            print("Attempting to place order")
            # place order
            placeOrderBtn = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".order-now"))
            )
            #placeOrderBtn.click()

            isComplete = True
        except:
            # make sure this link is the same as the link passed to driver.get() before looping
            driver.get(RTX3080LINK1)
            print("Error - restarting bot")
            continue

    print("Order successfully placed")


def worker():
    driver = initialize_selenium()
    rtx_loop(driver)
    clean_and_close_browser(driver)
    


if __name__ == '__main__':

    while (True):
        process = mp.Process(target=worker)
        process.start()
        process.join()