from browser import Browser

def find(by):
    return Browser.get_driver().find_element('xpath', by)
