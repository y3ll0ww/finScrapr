from refs.PageObject import find


INCOME_STATEMENT = "Income Statement"
BALANCE_SHEET = "Balance Sheet"
CASH_FLOW = "Cash Flow"

table_xpath = '//*[@id="statements"]/table[2]'


def table(): return find(table_xpath)
def tr(tr): return find(__get_xpath(tr))
def td(tr, td): return find(__get_xpath(tr, td))
def exchange(symbol): return find('//a[text()="' + symbol + '"]/following-sibling::span')


def statements():
    return {
    INCOME_STATEMENT: find('//a[text()="income statement"]'),
    BALANCE_SHEET: find('//a[text()="balance sheet"]'),
    CASH_FLOW: find('//a[text()="cash flow"]')
    }


def __get_xpath(tr, td=None):
    xpath = table_xpath + '/tbody/tr[' + str(tr) + ']'
    if td is not None:
        return xpath + '/td[' + str(td) + ']'
    return xpath
