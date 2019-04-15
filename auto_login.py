import argparse
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
    page_url = page['url']
    login_info = page['login']
    print('getting {}'.format(page_url))
    try:
        driver.get(page_url)

        if not login_info['is_logged']:
            user = _get_element(driver,
                                login_info['user_name_element_id'],
                                login_info['user_name_element_name'],
                                '\tUser Name Element (Name or ID) is not configured')

            password = _get_element(driver,
                                    login_info['pass_element_id'],
                                    login_info['pass_element_name'],
                                    '\tPassword Element (Name or ID) is not configured')

            login_button = _get_element(driver,
                                        login_info['login_button_id'],
                                        login_info['login_button_name'],
                                        '\tLogin Element (Name or ID) is not configured')

            user.send_keys(login_info['user_name'])
            password.send_keys(login_info['password'])
            login_button.click()
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

        page = config()['pages'][page]
        login_one_page(driver, page)


if __name__ == '__main__':
    driver = None
    parser = argparse.ArgumentParser()
    page_choices = config()['pages'].keys()

    parser.add_argument('-l',
                        '--pages',
                        nargs='+',
                        help='Pages to login',
                        choices=page_choices,
                        default=page_choices,)

    pages_selected = parser.parse_args().pages

    try:
        webdriver_path = config()['webdriver']['path']
        driver = webdriver.Chrome(executable_path=webdriver_path)
        # login_one_page(driver, config()['pages'][0])
        login_all_pages(driver, pages_selected)
    finally:
        pass
        # driver.quit() # close web browser
