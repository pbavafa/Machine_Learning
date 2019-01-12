from selenium import webdriver

driver = webdriver.Firefox()
driver.get('https://www.movoto.com/bakersfield-ca/price-2500000-0/@35.373292,-119.018712/')

street = driver.find_elements_by_xpath('//span[@itemprop="streetAddress"]')
print(street)
