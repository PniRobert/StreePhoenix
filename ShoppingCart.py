from bs4 import BeautifulSoup
from time import sleep
import asyncio
import aiohttp
import json
import re

domainName = "qadesign.staples.com"
applicationPath = "/services/printing"
productKey = "337c731e2cc14900"


async def loadCartPage(session):
    async with session.get(f"https://{domainName}{applicationPath}/Cart", ssl=False, timeout=None) as response:
        data = await response.text()
    userIdPart = re.findall(
        "set_encUserID\('.*'\)", data)[0]
    encUserId = re.split("'", userIdPart)[1]
    sleep(1)
    async with session.post(f"https://{domainName}{applicationPath}/PC.WebServices/CartService.svc/GetCartItemCounts",
                            json={"encUserID": encUserId}, ssl=False, timeout=None) as apiResponse:
        data = await apiResponse.text()
    sleep(1)
    return None


async def addToShoppingCart(session, groupKey, projectKey):
    data = {
        "GroupProjectKey": groupKey,
        "Projects": [
            {
                "ProjectKey": projectKey,
                "Quantity": 500
            }
        ]
    }
    async with session.post(f"https://{domainName}{applicationPath}/api/v3/cart/AddGroupProjectToCart",
                            json=data, ssl=False, timeout=None) as response:
        await response.text()
        sleep(2)
        return None


async def updateProject(session, projectKey):
    data = {
        "ProjectId": projectKey,
        "ProductKey": productKey,
        "SelectedOptions": {
            "Color": "Full Color",
            "Stock": "Premium",
            "SingleSided": "Disabled",
            "Finishing": "Gloss",
            "EditingFeatures": "SupportsAddPhotoFreeForm"
        },
        "SelectedQuantity": 500
    }
    async with session.post(f"https://{domainName}{applicationPath}/api/v3/project/UpdateForReview/{projectKey}",
                            json=data, ssl=False, timeout=None) as response:
        await response.text()
        sleep(2)
        return None


async def setShipMethod(session):
    async with session.post(f"https://{domainName}{applicationPath}/cart/api/ShippingMethod",
                            json={"Id": "1tJHqTB,glCJdT3MYpet5WpqwOARm9GXE"}, ssl=False, timeout=None) as response:
        await response.text()
        sleep(2)
        return None


async def approveProject(session, projectKey):
    async with session.post(f"https://{domainName}{applicationPath}/api/v3/project/Approve/{projectKey}",
                            json={}, ssl=False, timeout=None) as response:
        await response.text()
        sleep(2)
        return None


async def getProjectInfo(session):
    async with session.get(f"https://{domainName}{applicationPath}/product/{productKey}/builder/", ssl=False, timeout=None) as response:
        data = await response.text()
        groupId = re.findall("[0-9]+", response.url.path)[0]
    summaryUrl = f"https://{domainName}{applicationPath}/api/builder/v3/project/group/summary/{groupId}"
    async with session.get(summaryUrl, ssl=False, timeout=None) as jsonResponse:
        data = json.loads(await jsonResponse.text())

    return (groupId, data["SubProjects"][0]["ProjectKey"])


async def main():
    async with aiohttp.ClientSession() as session:
        projectInfo = await getProjectInfo(session)
        await approveProject(session, projectInfo[1])
        while True:
            await setShipMethod(session)
            await updateProject(session, projectInfo[1])
            await addToShoppingCart(session, projectInfo[0], projectInfo[1])
            await loadCartPage(session)
            sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
