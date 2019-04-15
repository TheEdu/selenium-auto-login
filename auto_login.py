from selenium import webdriver
from common import config


def _get_element(driver,
                 element_id,
                 element_name,
                 error_msg='\tElement (Name or ID) is not configured'):

    if element_id:
        return driver.find_element_by_id(element_id)
    elif element_name:
        return driver.find_element_by_name(element_name)
    else:
        raise ValueError(error_msg)


def login_one_page(driver, page):
    try:

        print('login {}'.format(page['name']))
        driver.get(page['url'])

        if not page['login']['is_logged']:
            user = _get_element(driver,
                                page['login']['user_name_element_id'],
                                page['login']['user_name_element_name'],
                                '\tUser Name Element (Name or ID) is not configured')

            password = _get_element(driver,
                                    page['login']['pass_element_id'],
                                    page['login']['pass_element_name'],
                                    '\tPassword Element (Name or ID) is not configured')

            login = _get_element(driver,
                                 page['login']['login_button_id'],
                                 page['login']['login_button_name'],
                                 '\tLogin Element (Name or ID) is not configured')

            user.send_keys(page['login']['user_name'])
            password.send_keys(page['login']['password'])
            login.click()
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)


def login_all_pages(driver, pages):

    for index, page in enumerate(pages):
        if index > 0:
            driver.execute_script("window.open('about:blank', 'tab{}');"
                                  .format(index))
            driver.switch_to.window("tab{}".format(index))

        login_one_page(driver, page)


if __name__ == '__main__':
    driver = None

    try:
        webdriver_path = config()['webdriver']['path']
        driver = webdriver.Chrome(executable_path=webdriver_path)
        # login_one_page(driver, config()['pages'][0])
        login_all_pages(driver, config()['pages'])
    finally:
        pass
        # driver.quit() # close web browser
