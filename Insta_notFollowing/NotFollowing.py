import getpass
import pandas as pd
from time                                    import sleep
from selenium                                import webdriver
from selenium.webdriver.common.keys          import Keys
from selenium.webdriver.common.action_chains import ActionChains

def get_unfollowers(username, browser, TargetAccount):

    search_bar = browser.find_element_by_xpath("//input[@placeholder='Search']")
    search_bar.send_keys(TargetAccount)
    sleep(5)
    print("First Enter")
    search_bar.send_keys(Keys.ENTER)
    print("Second Enter")
    search_bar.send_keys(Keys.ENTER)

    #user = browser.find_element_by_xpath("//a[contains(@href,'/{}')]".format(username))
    #user.click()
    #sleep(2)

    print('Following')
    follow_scroll = browser.find_element_by_xpath("//a[contains(@href,'/following')]")
    follow_scroll.click()
    following = _get_names(browser)

    print('Followers')
    followers_scroll = browser.find_element_by_xpath("//a[contains(@href,'/followers')]")
    followers_scroll.click()
    followers = _get_names(browser)

    print('Find the Cunts')
    not_following_back = [user for user in following if user not in followers]
    print(not_following_back)
    df = pd.DataFrame(not_following_back) 
    df.to_csv('NotFollowing.csv')

    return 

def _get_names(browser):
    
    sleep(2)
    scroll_box = browser.find_element_by_class_name('isgrP')
    last_height, height = 0, 1

    while last_height != height:
        last_height = height
        sleep(5)
        height = browser.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight); 
            return arguments[0].scrollHeight;
            """, scroll_box)

    links = scroll_box.find_elements_by_tag_name('a')
    print('Building List of names')
    names = [name.text for name in links if name.text != '']
    # close button 
    print('Closing list')
    close_list = browser.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")
    close_list.click()

    return names


def insta_unfollowers(username, password, target):
    browser = webdriver.Firefox()
    browser.implicitly_wait(20)
    browser.get('https://www.instagram.com/')

    element = browser.find_element_by_name("username")
    element.send_keys(username)
    sleep(5)
    element = browser.find_element_by_name("password")
    element.send_keys(password)

    sleep(5)
    print("Logging in")
    login_link = browser.find_element_by_xpath("//div[text()='Log In']")
    login_link.click()

    sleep(2)
    print("Notifications? Absolutely Not")
    login_remember = browser.find_element_by_xpath("//button[text()='Not Now']")
    login_remember.click()

    sleep(2)
    print("Another Not Now")
    another_remember = browser.find_element_by_xpath("//button[text()='Not Now']")
    another_remember.click()

    get_unfollowers(username, browser, target)

    print("Fin Diddle diddly")
    print("Close Browser")
    browser.close()

username = input("Enter username: ")
password = getpass.getpass('Enter password: ')
target = input("Enter target account: ")

insta_unfollowers(username, password, target)
