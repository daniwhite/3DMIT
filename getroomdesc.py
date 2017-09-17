from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

def numberToDesc(filename):
    filename = filename.split('/')[-1]
    res = {}
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://floorplans.mit.edu/cgi-bin-db-mit/wdbmitscript.asp?Report=ibrl&Item=MIT')
    cont = driver.find_element_by_name('Select')
    cont.click()
    while True:
        try:
            link = driver.find_element_by_partial_link_text(filename[0])
            break
        except:
            pass
    link.click()
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    for line in (source_code.splitlines()[17:-1]):
        try:
            temp = line.split()
            res[temp[0]] = temp[2]
        except:
            continue
    for string in ['</pre><p><a', 'Duo', 'Error:', '<form', '<input', '<iframe',
        '&lt;p&gt;Your', '<div', 'If', 'you', '<a', 'consult', 'contact',
        'enrolled,']:
        try:
            del res[string]
        except KeyError:
            pass
    driver.close()
##    print(res)
    return res

##numberToDesc('/Users/jennahimawan/Desktop/1_0.png')
