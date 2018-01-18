from lxml import etree, html
import sys
from selenium import webdriver
from PIL import Image
from cStringIO import StringIO

verbose = 1 
driver = webdriver.Chrome()

driver.get('https://serviceinfo.harley-davidson.com/sip/user/loginForm')


username = driver.find_element_by_name('username')
username.send_keys('haligen')

password = driver.find_element_by_name('password')
password.send_keys('Lancer5137')

form = driver.find_element_by_id('login-submit')
form.submit()

file = open("285745.html", "r")
file2 = file.read()

tree = html.fromstring(file2)

serviceURLs = tree.xpath('//@href')

begin = 'softail'
count = 0
end = '.png'

js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'


for service in serviceURLs:
    website = "https://serviceinfo.harley-davidson.com" + service
    driver.get(website)
    scrollheight = driver.execute_script(js)

    try:
        if verbose > 0: 
            print scrollheight

        slices = []
        offset = 0
        while offset < scrollheight:
            if verbose > 0: 
                print offset

            driver.execute_script("window.scrollTo(0, %s);" % offset)
            img = Image.open(StringIO(driver.get_screenshot_as_png()))
            offset += img.size[1]
            slices.append(img)

            if verbose > 0:
                driver.get_screenshot_as_file('%s/screen_%s.png' % ('/tmp', offset))
                print scrollheight


        screenshot = Image.new('RGB', (slices[0].size[0], scrollheight))
        offset = 0
        for img in slices:
            screenshot.paste(img, (0, offset))
            offset += img.size[1]

        screenshot.save(begin + str(count) + end)

    except:
        print("nope")
    count += 1
 
driver.close()
