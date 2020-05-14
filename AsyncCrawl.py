from bs4 import BeautifulSoup
import asyncio
import aiohttp

domainName = "qadesign.staples.com"
applicationPath = "/services/printing"


def getVisitLink(rawUrl):
    rawUrl = rawUrl.strip()
    if rawUrl == "#":
        return None
    rawUrl = rawUrl.replace(f"https://{domainName}", "")
    rawUrl = rawUrl.replace(f"{applicationPath}", "")
    if rawUrl.find("/") == 0 and rawUrl.find("//") < 0:
        return rawUrl
    return None


def parseTarget(pageData, targetElement, selectClasses):
    targetUrls = set()
    page = BeautifulSoup(pageData, "html.parser")
    if (selectClasses == None):
        for link in page.find_all("a"):
            rawLink = link.get("href")
            url = None if rawLink == None else getVisitLink(rawLink)
            if not url == None:
                targetUrls.add(url)
    else:
        for selector in selectClasses:
            for nextlink in page.find_all(targetElement, class_=selector):
                rawLink = nextlink.get("href")
                nextUrl = None if rawLink == None else getVisitLink(rawLink)
                if not nextUrl == None:
                    targetUrls.add(nextUrl)
    return targetUrls


async def getPageContent(session, url):
    async with session.get(url, ssl=False, timeout=None) as response:
        data = await response.text()
        print(f"{url} :{response.status}")
        if response.status == 500:
            # print("500")
            return ""
        else:
            return data


async def getContentForPages(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(getPageContent(
            session, f"https://{domainName}{applicationPath}{url}"))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)
    for t in tasks:
        content = t.result()
        nextUrls = parseTarget(
            content, "a", ["absolute-link", "tag-tile-click"])
        if len(nextUrls) > 0:
            await getContentForPages(session, nextUrls)


async def main():
    async with aiohttp.ClientSession() as session:
        content = await getPageContent(session, f"https://{domainName}{applicationPath}/")
        siteUrls = parseTarget(content, "a", None)
        siteUrls.remove("/")
        siteUrls.add(
            "/legacy/Themes?q=1Vs6CjtwxY_VteZzh2jc1dkRmT82QfiZ5yw3oRZWjYdH6cz_FTg4bjMz9,yB,qccP")
        siteUrls.add(
            "/legacy/Themes?q=1Uc9eBd2VmItDYim,6nB,jSca5hAGnx7M94WVes6PX6JqK8KGiO8mHnbD_3e2LR50")
        await getContentForPages(session, siteUrls)

if __name__ == "__main__":
    asyncio.run(main())
