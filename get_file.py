from typing import List
import itertools as itt

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

synchro_url = "https://academique-dmz.synchro.umontreal.ca"


def fill_elem(driver, elem_id, value, end=Keys.RETURN):
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, elem_id))
    )
    elem.clear()
    elem.send_keys(value)
    elem.send_keys(end)


def login(username, password):
    driver: WebDriver = webdriver.Chrome()
    driver.get(synchro_url)
    fill_elem(driver, 'txtIdentifiant', username, end=Keys.TAB)
    fill_elem(driver, 'txtMDP', password)
    driver.find_element_by_id('win0groupletPTNUI_LAND_REC_GROUPLET$1').click()
    driver.switch_to.frame(0)
    return driver


def goto_main_iframe(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame('ptifrmtgtframe')


def wait_for_process_to_end(driver):
    goto_main_iframe(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'processing'))
    )
    goto_main_iframe(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'processing'))
    )


def semester_ratio_name(x):
    return 'SSR_DUMMY_RECV1$sels${}$$0'.format(x)


def wait_by_id(driver, elem_id):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, elem_id))
    )


def get_semester_list(driver: WebDriver):
    dropdown = driver.find_element(By.ID, "DERIVED_SSS_SCL_SSS_MORE_ACADEMICS")
    dropdown.find_element(By.XPATH, "//option[. = 'Votre horaire cours']").click()
    driver.find_element(By.ID, "DERIVED_SSS_SCL_SSS_MORE_ACADEMICS").click()
    driver.find_element(By.NAME, "DERIVED_SSS_SCL_SSS_GO_1$IMG").click()

    driver.switch_to.default_content()
    driver.switch_to.frame('ptifrmtgtframe')

    wait_for_process_to_end(driver)
    semester_elements = driver.find_elements_by_class_name('PSRADIOBUTTON')
    return [i.find_element_by_xpath('./../../..').text for i in semester_elements]


# either needs a driver or username/password
def get_courses(semesters, driver: WebDriver):
    course_table = []
    for i, semester in zip(itt.count(0), semesters):
        if i > 0:
            driver.back()
            goto_main_iframe(driver)
            get_semester_list(driver)

        driver.find_elements_by_class_name('PSRADIOBUTTON')[semester].click()
        wait_by_id(driver, "DERIVED_SSS_SCT_SSR_PB_GO").click()

        goto_main_iframe(driver)

        wait_by_id(driver, "DERIVED_REGFRM1_SA_STUDYLIST_D").click()
        wait_by_id(driver, "DERIVED_REGFRM1_SA_STUDYLIST_W").click()
        wait_by_id(driver, "DERIVED_REGFRM1_SA_STUDYLIST_SHOW$14$").click()

        wait_for_process_to_end(driver)

        course_table.append(str(wait_by_id(driver, 'ACE_STDNT_ENRL_SSV2$0').get_attribute('outerHTML')))


    return course_table
