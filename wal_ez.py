"""
Walmart Item Purchaser
By Norton Lui
Working as of 12/2/2017 10:00pm
"""

__version__ = '1.0.0'
__author__ = 'Norton Lui'

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def get_walmart_info():
    """pass"""
    pref = get_user_data()
    order_selectors = pref[0]
    browser_paths = pref[1]
    item_link = pref[2]
    form_fill = {'email_form': pref[3][0],
                 'pass_form': pref[3][1],
                 'card_ccv_box': pref[3][2],}
    compiled_info = {'browser_paths': browser_paths, 'order_selectors': order_selectors,
                     'form_fill': form_fill, 'item':item_link
                    }
    return compiled_info


def get_user_data():
    """pass"""
    chrome_user_path = os.getenv('HOME')+"\\AppData\\Local\\Google\\Chrome\\User Data"
    driver_user_path = 'n'
    ublock_path = chrome_user_path+"\\Default\\Extensions\\cjpalhdlnbpafiamejdnhcphjbkeiagm\\"\
                +os.listdir(
                    chrome_user_path+"\\Default\\Extensions\\cjpalhdlnbpafiamejdnhcphjbkeiagm\\")[0]
    order_selectors = {'add_to_cart': '[data-tl-id=ProductPrimaryCTA-cta_add_to_cart_button]',
                       'cart_checkout':   '[data-automation-id=pac-pos-proceed-to-checkout]',
                       'cont_shipping':   '[data-tl-id=COAC1FulContBtn]',
                       'conf_address':   '[data-tl-id=COAC2ShpContBtn]',
                       'card_ccv_box':   '[data-tl-id=COAC3PayCCSecCodeInp0]',
                       'review_0rder':   '[data-tl-id=COAC3PayReviewOrderBtn]',
                       #"place_order":   '[data-tl-id=COPlaceOrderBtn]'
                      }
    print('***BE SURE TO WAIT FOR EACH PROMPT BEFORE PROCEEDING***\n')
    item_link = input('\nPlease enter link of item you wish to purchase on Walmart. \n:')
    print('using: '+item_link)
    use_current_chrome = input(
        '\nDo you want to use your current Chrome user data? (y/n) default is n :')
    if use_current_chrome == 'y':
        print('Using current Chrome user data(~spotty)\n')
        driver_user_path = "user-data-dir="+chrome_user_path
        ccv = input('CCV (security code) of the credit card being used for this purchase: ')
        user_info = ('', '', ccv)
    else:
        print('Not using current Chrome user data\n')
        username = input('Enter Walmart email: ')
        password = input('Enter password associated with above account: ')
        ccv = input('CCV (security code) of the credit card being used for this purchase: ')
        user_info = (username, password, ccv)

    return (order_selectors, {'chrome_user_path': driver_user_path, 'ublock_path': ublock_path},
            item_link, user_info)


def purchase_item(driver, order_selectors, form_fill):
    """pass"""
    for process_name, selector in order_selectors.items():
        try:
            WebDriverWait(driver,
                          10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            order_proceed = driver.find_element_by_css_selector(selector)
            if process_name in form_fill:
                order_proceed.send_keys(form_fill[process_name])
            else:
                order_proceed.click()
        except (TimeoutException, NoSuchElementException):
            order_proceed = driver.find_element_by_css_selector(selector)
            if process_name in form_fill:
                order_proceed.send_keys(form_fill[process_name])
            else:
                order_proceed.click()
        finally:
            pass


def login_walmart(driver, form_fill):
    """pass"""
    email_form = '[data-tl-id=signin-email-input]'
    pass_form = '[data-tl-id=signin-password-input]'
    sign_in = '[data-tl-id=signin-submit-btn]'
    login_selectors = {'email_form': email_form,
                       'pass_form': pass_form,
                       'sign_in': sign_in
                      }
    for process_name, selector in login_selectors.items():
        try:
            WebDriverWait(driver,
                          10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            order_proceed = driver.find_element_by_css_selector(selector)
            if process_name in form_fill:
                order_proceed.send_keys(form_fill[process_name])
            else:
                order_proceed.click()

        except (TimeoutException, NoSuchElementException):
            order_proceed = driver.find_element_by_css_selector(selector)
            if process_name in form_fill:
                order_proceed.send_keys(form_fill[process_name])
            else:
                order_proceed.click()
        finally:
            pass
    time.sleep(2)

def run_program(compiled_info):
    """pass"""
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    if compiled_info['browser_paths']['chrome_user_path'][0] == 'n':
        options.add_argument('load-extension=' + compiled_info['browser_paths']['ublock_path'])

    else:
        options.add_argument(compiled_info['browser_paths']['chrome_user_path'])

    driver = webdriver.Chrome(chrome_options=options)
    if compiled_info['browser_paths']['chrome_user_path'][0] == 'n':
        driver.get('https://www.walmart.com/account/login')
        login_walmart(driver, compiled_info['form_fill'])

    driver.get(compiled_info['item'])
    start = ' '
    while start != '':
        driver.get(compiled_info['item'])
        start = input(
            "\nPress Enter to start the purchase process, "+\
            "or input anything to refresh the page\n").strip()
    #driver.get('https://www.walmart.com/ip/Super-NES-Classic-Edition-Universal/741659089')
    starttiming = time.time()
    purchase_item(driver, compiled_info['order_selectors'], compiled_info['form_fill'])
    endtiming = time.time()

    print('\nTime Elapsed from adding to cart to placing order = '+
          str(endtiming-starttiming)+
          ' seconds')
    print('\nPurchase complete. Closing program in 15 seconds')
    time.sleep(15)
    driver.quit()
    sys.exit()


if __name__ == "__main__":
    COMPILED_INFORMATION = get_walmart_info()
    run_program(COMPILED_INFORMATION)
