from refs.PageObject import find


def email(): return find('//span[text()="Your email"]/following-sibling::input')
def password(): return find('//span[text()="Your password"]/following-sibling::input')
def login(): return find('//input[@value="Log in"]')

def valid(): return find('//a[text()="y3ll0ww"]')

