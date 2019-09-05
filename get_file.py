from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import bs4
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
import json

def get_page(config):
    with open(config) as j:
        data = json.load(j)

    driver = webdriver.Chrome()
    driver.get("https://academique-dmz.synchro.umontreal.ca/psp/acprpr9/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL")


    def fill_elem(elem_id, value, end=Keys.RETURN):
        elem = driver.find_element_by_id(elem_id)
        elem.clear()
        elem.send_keys(value)
        elem.send_keys(end)


    fill_elem('txtIdentifiant', data['username'], end=Keys.TAB)
    fill_elem('txtMDP', data['password'])

    driver.find_element_by_id('win0groupletPTNUI_LAND_REC_GROUPLET$1').click()
    driver.switch_to.frame(0)
    dropdown = driver.find_element(By.ID, "DERIVED_SSS_SCL_SSS_MORE_ACADEMICS")
    dropdown.find_element(By.XPATH, "//option[. = 'Votre horaire cours']").click()
    driver.find_element(By.ID, "DERIVED_SSS_SCL_SSS_MORE_ACADEMICS").click()
    driver.find_element(By.NAME, "DERIVED_SSS_SCL_SSS_GO_1$IMG").click()

    driver.switch_to.default_content()
    driver.switch_to.frame('ptifrmtgtframe')


    wait_by_id = lambda elem_id: WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, elem_id))
    )

    wait_by_id('SSR_DUMMY_RECV1$sels$0$$0').click()
    wait_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()

    driver.switch_to.default_content()
    driver.switch_to.frame('ptifrmtgtframe')

    wait_by_id("DERIVED_REGFRM1_SA_STUDYLIST_D").click()
    wait_by_id("DERIVED_REGFRM1_SA_STUDYLIST_W").click()
    wait_by_id("DERIVED_REGFRM1_SA_STUDYLIST_SHOW$14$").click()

    driver.switch_to.default_content()
    driver.switch_to.frame('ptifrmtgtframe')

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'processing'))
    )
    print('found elem')
    driver.switch_to.default_content()
    driver.switch_to.frame('ptifrmtgtframe')

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'processing'))
    )
    driver.switch_to.default_content()
    driver.switch_to.frame('ptifrmtgtframe')
    a = str(wait_by_id('ACE_STDNT_ENRL_SSV2$0').get_attribute('outerHTML'))
    driver.quit()
    return a


if __name__ == '__main__':
    data = get_page('data.json')
    with open('page.html', 'w') as fd:
        fd.write(data)
