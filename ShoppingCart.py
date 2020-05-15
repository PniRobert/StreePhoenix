import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

domainName = "qadesign.staples.com"
applicationPath = "/services/printing"

if __name__ == "__main__":
    startUrl = f"https://{domainName}{applicationPath}/product/337c731e2cc14900/builder/"
    driver = webdriver.Firefox()
    try:
        driver.maximize_window()
        driver.get(startUrl)
        sleep(2)
        while(True):
            builderUrl = driver.current_url
            nextUrl = builderUrl.replace("Builder", "review")
            endPos = nextUrl.find("#")
            nextUrl = nextUrl[:endPos] + "/"
            driver.get(nextUrl)
            sleep(30)
            driver.find_element_by_css_selector(
                "label.test_approvalCheckbox").click()
            driver.find_element_by_css_selector(
                "button.tag-advance-to-upsell-button").click()
            sleep(20)
            driver.find_element_by_css_selector(
                "button.tag-add-to-cart-button").click()
            editLink = None
            while(editLink == None):
                sleep(20)
                editLink = driver.find_element_by_link_text("Edit")
            print(editLink)
            editLink.click()

    finally:
        driver.quit()
