from enum import Enum
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

domainName = "qadesign.staples.com"
applicationPath = "/services/printing"


class SelectMode(Enum):
    byTagName = 1
    byCssSelector = 2


def getVisitLink(rawUrl):
    if rawUrl == None:
        return None
    rawUrl = rawUrl.strip()
    if rawUrl == "#":
        return None
    rawUrl = rawUrl.replace(f"https://{domainName}", "")
    rawUrl = rawUrl.replace(f"{applicationPath}", "")
    if rawUrl.find("/") == 0 and rawUrl.find("//") < 0:
        return rawUrl
    return None


def visitLink(url, driver):
    visitUrl = f"https://{domainName}{applicationPath}{url}"
    print(visitUrl)
    driver.get(visitUrl)
    nextUrls = set()
    getLinkTargetUrls(driver, SelectMode.byCssSelector,
                      "a.absolute-link", "href", nextUrls)
    getLinkTargetUrls(driver, SelectMode.byCssSelector,
                      "a.tag-tile-click", "href", nextUrls)
    for next in nextUrls:
        visitLink(next, driver)


def getLinkTargetUrls(driver, selectMode, selector, attributeSelector, resultUrls):
    driver.implicitly_wait(20)
    elements = None
    if selectMode == SelectMode.byCssSelector:
        elements = driver.find_elements_by_css_selector(selector)
    else:
        elements = driver.find_elements_by_tag_name(selector)
    for elem in elements:
        nextUrl = getVisitLink(elem.get_attribute(attributeSelector))
        if not nextUrl == None:
            resultUrls.add(nextUrl)


if __name__ == "__main__":
    targetUrls = set()
    startUrl = f"https://{domainName}{applicationPath}/ping/btwd"
    driverOptions = Options()
    driverOptions.headless = True
    driver = webdriver.Firefox(options=driverOptions)
    try:
        driver.maximize_window()
        print(startUrl)
        driver.get(startUrl)
        # cookie = driver.get_cookie("plsx")
        # cookie["value"] = "808601866.20480.0000"
        driver.get(startUrl)
        sleep(10)
        startUrl = f"https://{domainName}{applicationPath}/"
        driver.get(startUrl)
        getLinkTargetUrls(driver, SelectMode.byTagName,
                          "a", "href", targetUrls)
        targetUrls.remove("/")
        targetUrls.add(
            "/legacy/Themes?q=1Vs6CjtwxY_VteZzh2jc1dkRmT82QfiZ5yw3oRZWjYdH6cz_FTg4bjMz9,yB,qccP")
        targetUrls.add(
            "/legacy/Themes?q=1Uc9eBd2VmItDYim,6nB,jSca5hAGnx7M94WVes6PX6JqK8KGiO8mHnbD_3e2LR50")
        for visitUrl in targetUrls:
            visitLink(visitUrl, driver)
    finally:
        driver.quit()
