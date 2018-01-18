from lxml import etree, html
import sys
from selenium import webdriver

#must use PhantomJS even though its depreciated to get full page capture
driver = webdriver.PhantomJS()

#initial login page
driver.get('https://serviceinfo.harley-davidson.com/sip/user/loginForm')

#sip username / password
username = driver.find_element_by_name('username')
username.send_keys('******')

password = driver.find_element_by_name('password')
password.send_keys('******')

form = driver.find_element_by_id('login-submit')
form.submit()

#name of the HTML file for the document you want to save
file = open("287572.html", "r")
file2 = file.read() #html to string

tree = html.fromstring(file2)

serviceURLs = tree.xpath('//@href') #extracts all the page links

#used to make unique file names
begin = 'softail'
count = 0
end = '.png'

#iterate though each url extracted from the HTML
for service in serviceURLs:
    #combine main url with extracted url
    website = "https://serviceinfo.harley-davidson.com" + service
    driver.get(website)
    driver.set_window_size(1280, 1024) #must set the window size for PhantomJS

    try:
        #change ./diagman/ to whatever folder you made to save the pics in
        driver.save_screenshot('./diagman/' + begin + str(count) + end)

    except:
        print("nope")
    count += 1 #used for file name generation
 
driver.close()
