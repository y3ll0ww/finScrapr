from refs.PageObject import find


def cookie_popup(): return find('//span[text()="DISAGREE"]/parent::button')
def upgrade_popup(): return find('//*[@id="modal-elite-ad-close"]')
