from RPA.Browser.Selenium import Selenium,ChromeOptions
from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent
from qrlib.QRUtils import display
import Constants
import time
import os
import zipfile



class AccuityComponent(QRComponent):
    def __init__(self):
        super().__init__() 
        self.browser = Selenium()


        self.URL = 'https://adfd.accuity.com/webclient/Login.xhtml'
    def _get_vault(self):
        # run_item = QRRunItem()
        # self.logger = self.run_item.logger
        self.__vault_data: dict = QREnv.VAULTS['accuity']
       

    def open_chrome(self):
        self._get_vault()
        self.browser.set_download_directory(directory= f'{Constants.ACCUITY_PATH}')
        self.browser.open_available_browser(self.URL, download=False)
        # self.browser.open_chrome_browser(self.URL)
        time.sleep(5)
        self.browser.maximize_browser_window()
        # time.sleep(30)
    def login(self):
        self._get_vault()
        USERNAME = "//input[@id='username']"
        PASSWORD = "//input[@id='value']"
        SUBMIT_BUTTON = "//div/button[@id='j_id_1p']"
        self.browser.wait_until_element_is_visible(USERNAME, Constants.TIMEOUT)
        self.browser.input_text(USERNAME, self.__vault_data["username"])
        self.browser.input_text(PASSWORD, self.__vault_data["password"])
        self.browser.wait_and_click_button(SUBMIT_BUTTON)
        time.sleep(5)

    # def scrape_data(self):
    #     HOME = '//*[@id="j_id_19:0:j_id_1f"]/span'
    #     FIRST_FILE = '//*[@id="j_id_19:0_0:j_id_1u"]'
    #     SMALL_SIZE = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[5]' #//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[3]
    #     download_button = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
    #     # DOWNLOAD_BUTTON = "//button[@id='downloadFiles:downloadFiles']"
    #     SECOND_FILE = '//*[@id="j_id_19:0_1:j_id_1u"]/span'
    #     SECOND_FILE_SMALL_SIZE = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[3]'
    #     # DOWNLOAD_LINK = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
    #     MIGRATION_TEST_FILE = '//*[@id="j_id_19:0_2:j_id_1u"]/span'
    #     CLICK_SMALL_SIZE_OF_MIGRATION = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
    #     FOURTH_FILE = '//*[@id="j_id_19:0_3:j_id_1u"]/span'
    #     CLICK_FOURTH_FILE_SMALL_SIZE_FILE = ''

    #     self.browser.click_element_when_visible(HOME)
    #     # self.browser.wait_until_element_is_visible(FIRST_FILE,Constants.TIMEOUT)
    #     self.browser.click_element_when_visible(FIRST_FILE)
    #     time.sleep(4)
    #     self.browser.wait_until_element_is_visible(SMALL_SIZE,Constants.TIMEOUT)
    #     self.browser.click_element_when_visible(SMALL_SIZE)
    #     time.sleep(3)
    #     self.browser.click_element_when_visible(download_button)
    #     # self.browser.wait_and_click_button(DOWNLOAD_BUTTON)
    #     # download_directory = f'{Constants.ACCUITY_PATH}'
    #     # files_in_directory = os.listdir(download_directory)
    #     self.browser.click_element_when_visible(SECOND_FILE)
    #     time.sleep(4)
    #     self.browser.wait_until_element_is_visible(SECOND_FILE_SMALL_SIZE,Constants.TIMEOUT)
    #     self.browser.click_element_when_visible(SECOND_FILE_SMALL_SIZE)
    #     time.sleep(3)
    #     self.browser.click_element_when_visible(download_button)

    #     self.browser.click_element_when_visible(MIGRATION_TEST_FILE)
    #     time.sleep(4)
    #     self.browser.wait_until_element_is_visible(CLICK_SMALL_SIZE_OF_MIGRATION,Constants.TIMEOUT)
    #     self.browser.click_element_when_visible(CLICK_SMALL_SIZE_OF_MIGRATION)
    #     time.sleep(3)
    #     self.browser.click_element_when_visible(download_button)

    #     self.browser.click_element_when_visible(FOURTH_FILE)
    #     time.sleep(4)
    #     self.browser.wait_until_element_is_visible(download_button,Constants.TIMEOUT)
    #     self.browser.click_element_when_visible(download_button)
    #     time.sleep(3)
    #     self.browser.click_element_when_visible(download_button)
    #     time.sleep(15)
    
    def scrape_first_file_data(self,initial_date):
        HOME = '//*[@id="j_id_19:0:j_id_1f"]/span'
        FIRST_FILE = '//*[@id="j_id_19:0_0:j_id_1u"]'
        SMALL_SIZE = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[5]' #//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[3]
        # download_button = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
        DOWNLOAD_BUTTON = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
        DATE_PATH = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[4]'
        # //*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[4]

        self.browser.click_element_when_visible(HOME)
        # self.browser.wait_until_element_is_visible(FIRST_FILE,Constants.TIMEOUT)
        self.browser.click_element_when_visible(FIRST_FILE)
        time.sleep(2)
        self.browser.wait_until_element_is_visible(DATE_PATH)
        date = self.browser.get_webelement(DATE_PATH).text
        date = str(date).split()[0]
        if date != initial_date:
            display(f'Date is {date}')
            time.sleep(3)
            self.browser.wait_until_element_is_visible(SMALL_SIZE,Constants.TIMEOUT)
            self.browser.click_element_when_visible(SMALL_SIZE)
            time.sleep(3)
            self.browser.click_element_when_visible(DOWNLOAD_BUTTON)
            return date
        else:
            display('No modification in date')
            return date
        # time.sleep(15)

    def scrape_second_file_data(self,initial_date):
        SECOND_FILE = '//*[@id="j_id_19:0_1:j_id_1u"]/span'
        SECOND_FILE_SMALL_SIZE = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[3]'
        DOWNLOAD_BUTTON = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
        DATE_PATH = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[4]'

        self.browser.click_element_when_visible(SECOND_FILE)
        date = self.browser.get_webelement(DATE_PATH).text
        date = str(date).split()[0]
        if date != initial_date:
            display(f'Date is {date}')
            time.sleep(3)
            self.browser.wait_until_element_is_visible(SECOND_FILE_SMALL_SIZE,Constants.TIMEOUT)
            self.browser.click_element_when_visible(SECOND_FILE_SMALL_SIZE)
            time.sleep(3)
            self.browser.click_element_when_visible(DOWNLOAD_BUTTON)
            return date
        else:
            display('No modification in date')
            return date
        # time.sleep(15)
    def scrape_third_file_data(self,initial_date):
        MIGRATION_TEST_FILE = '//*[@id="j_id_19:0_2:j_id_1u"]/span'
        CLICK_SMALL_SIZE_OF_MIGRATION = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
        DOWNLOAD_BUTTON = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
        DATE_PATH = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[4]'
        time.sleep(2)
        self.browser.wait_until_element_is_visible(MIGRATION_TEST_FILE,timeout=30)
        self.browser.click_element_when_visible(MIGRATION_TEST_FILE)
        time.sleep(3)
        date = self.browser.get_webelement(DATE_PATH).text
        date = str(date).split()[0]
        if date != initial_date:
            display(f'Date is {date}')
            self.browser.wait_until_element_is_visible(CLICK_SMALL_SIZE_OF_MIGRATION,Constants.TIMEOUT)
            self.browser.click_element_when_visible(CLICK_SMALL_SIZE_OF_MIGRATION)
            time.sleep(3)
            return date
        else:
            display('No modification in date')
            return date
        # self.browser.click_element_when_visible(DOWNLOAD_BUTTON)
        # time.sleep(15)

    def scrape_fourth_file_data(self,initial_date):
        FOURTH_FILE = '//*[@id="j_id_19:0_3:j_id_1u"]/span'
        DOWNLOAD_FILE_LINK = '//*[@id="fileListForm:j_id_8l:0:j_id_8v"]'
        DATE_PATH = '//*[@id="fileListForm:j_id_8l_data"]/tr[1]/td[4]'
        time.sleep(3)
        self.browser.click_element_when_visible(FOURTH_FILE)
        time.sleep(3)
        date = self.browser.get_webelement(DATE_PATH).text
        date = str(date).split()[0]
        if date != initial_date:
            display(f'Date is {date}')
            self.browser.wait_until_element_is_visible(DOWNLOAD_FILE_LINK,Constants.TIMEOUT)
            self.browser.click_element_when_visible(DOWNLOAD_FILE_LINK)
            time.sleep(3)
            # self.browser.click_element_when_visible(DOWNLOAD_FILE_LINK)
            # time.sleep(15)
            return date
        else:
            display('No modification in date')
            return date

    def close_browser(self):
        self.browser.close_browser()
    # def extract_zipfile(self):
    #     download_directory = f'{Constants.ACCUITY_PATH}'
    #     zip_file = os.listdir(download_directory)
    #     # zip_files = [file for file in zip_file if file.endswith('.zip')]
    #     display(f'zip file list is ==> {zip_file}')
    #     for file in zip_file:
    #         zip_file_path = os.path.join(download_directory,file)
    #         extract_directory = download_directory
    #         with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
    #             zip_ref.extractall(extract_directory)
    #     display('Successfully extract the zip files in its location')
            
