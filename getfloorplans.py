from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

	
def download_pdf(lnk):
    options = webdriver.ChromeOptions()
    download_folder = "/Users/jennahimawan/Downloads"
    profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": download_folder,
               "download.extensions_to_open": ""}

    options.add_experimental_option("prefs", profile)

    print("Downloading file from link: {}".format(lnk))

    driver = webdriver.Chrome(chrome_options = options)
    driver.get(lnk)

    filename = lnk.split("/")[4].split(".cfm")[0]
    print("File: {}".format(filename))

    print("Status: Download Complete.")
    print("Folder: {}".format(download_folder))

    driver.close()

def getFloorPlans(filename):
    links = []
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://floorplans.mit.edu/searchPDF.asp')
    select_box = browser.find_element_by_name('Bldg') # if your select_box has a name.. why use xpath?..... this step could use either xpath or name, but name is sooo much easier.
    options = [x for x in select_box.find_elements_by_tag_name("option")] #this part is cool, because it searches the elements contained inside of select_box and then adds them to the list options if they have the tag name "options"
    for i in range(len(options)):
        select.select_by_index(i)
        go = select.select_by_value('Go')
        go.click()
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if len(elem.text) == 1:
                links.append(elem.text)
        for linktext in links:
            link = driver.find_element_by_partial_link_text(linktext)
            link.click()
    while True:
        try:
            link = driver.find_element_by_partial_link_text('1')
            break
        except:
            pass
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        links.append(elem.text)
    for linktext in links:
        link = driver.find_element_by_partial_link_text(linktext)
        link.click()
        elem = driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("outerHTML")
        for line in (source_code.splitlines()[17:-1]):
            try:
                temp = line.split()
                res[temp[0]] = temp[2]
            except:
                continue
        driver.back()
    for string in ['</pre><p><a', 'Duo', 'Error:', '<form', '<input', '<iframe',
        '&lt;p&gt;Your', '<div', 'If', 'you', '<a', 'consult', 'contact',
        'enrolled,']:
        del res[string]
    return res
