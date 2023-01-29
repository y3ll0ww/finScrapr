from Printer import *
from browser import Browser
from export import File
from refs import urls
from refs.pages import PopupsPage
from refs.pages.ScreenerPage import *

companies = []
dictionary = {"companies": []}

before = "This action will collect all companies available on finviz.\nEstimated time: " + colored(CYAN, "20-30 minutes\n")
after = "Number of companies added: "


def collect():
    print(before)

    Browser.go_to(urls.screener)

    counter = 0
    contin = True
    while contin:
        for i in range(22):
            if i > 1:
                # Remove popup whenever it shows up
                if PopupsPage.upgrade_popup().is_displayed():
                    PopupsPage.upgrade_popup().click()
                # Extract row from table (if possible)
                try:
                    company = {
                        "symbol": symbol(i).text,
                        "name": name(i).text,
                        "sector": sector(i).text,
                        "industry": industry(i).text,
                        "country": country(i).text,
                        "link": link(i)
                    }
                    companies.append(company)
                    print(company)
                    counter += 1
                # If there are no more rows quit the loop
                except:
                    contin = False
                    break
            if i > 20:
                # At the end of the table click next
                try:
                    next().click()
                # If next cannot be clicked quit the loop
                except:
                    contin = False
                    break

    # Save to json file in /export/files/
    dictionary["companies"] = companies
    File.write(dictionary, "companies_list", "companies")

    print(after, colored(MAGENTA, str(counter)))
