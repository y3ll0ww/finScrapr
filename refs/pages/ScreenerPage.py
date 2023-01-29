from refs.PageObject import find


def next(): return find('//b[text()="next"]')
def symbol(row): return find(__getXpath(row=row, col=2))
def name(row): return find(__getXpath(row=row, col=3))
def sector(row): return find(__getXpath(row=row, col=4))
def industry(row): return find(__getXpath(row=row, col=5))
def country(row): return find(__getXpath(row=row, col=6))
def link(row): return find(__getXpath(row=row, col=2) + '/a').get_attribute('href')
def __getXpath(row, col): return '//*[@id="screener-views-table"]/tbody/tr[4]/td/table/tbody/tr[' + str(row) + ']/td[' + str(col) + ']'
