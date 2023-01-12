from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.common.exceptions import TimeoutException

# URL to Scrape
URL = ("https://primo.bibliothek.kit.edu/primo-explore/search?query=any"
       ",contains,a&tab=kit_evastar&search_scope=KIT_Evastar&vid=KIT&offset=0")
# Structure of the output .csv file
HEADER = ['Title', 'Doc-Type', 'Authors', 'Year', 'Institutions',
          'Paper-ID', 'Abstract']
# Use write Header True when creating a
# new file and False when appending to a file
WRITE_HEADER = True

# When HEADLESS = True Chrome opens without GUI
HEADLESS = False

# Path to Chrome Driver
DRIVER_PATH = 'chromedriver/chromedriver.exe'

# Path to Chrome.exe
CHROME_PATH = 'D:/Programme/Google/Chrome/Application/chrome.exe'

# Path to Output file (must be csv)
OUTPUT_PATH = r'db/db_creation/output.csv'

# XPATH to First Result on Page
XPATH_FIRST_RESULT = ('/html/body/primo-explore/div[1]/prm-explore-main'
                      '/ui-view/prm-search/div/md-content'
                      '/div[1]/prm-search-result-list'
                      '/div/div[1]/div/div[1]/prm-brief-result-container/'
                      'div[1]/div[3]/prm-brief-result/h3/a')

# Define Number of results to be scraped. (KIT-Open) only shows ~2000 results
NUMBER_OF_RESULTS = 2000


def launchBrowser():
    '''Sets up and opens Browser (headless, wenn HEADLESS = True). Returns Driver.'''
    s = Service(DRIVER_PATH)
    options = Options()
    options.binary_location = CHROME_PATH

    if HEADLESS:
        options.headless = HEADLESS
        
        # Silences logging of Selenium
        options.add_argument("--log-level=3")
        options.add_argument('window-size=1920x1080')

    # Start Chrome
    scrape_driver = webdriver.Chrome(service=s, options=options)
    scrape_driver.get(URL)
    time.sleep(5)
    return scrape_driver


def find_element_by_XPATH(XPATH):
    try:
        return driver.find_element(By.XPATH, XPATH)
    except NoSuchElementException:
        print('Element ' + XPATH + ' could not be found')


def click_element_by_XPATH(XPATH):
    find_element_by_XPATH(XPATH).click()


def setFilter():
    '''Sets Filters'''
    # Obligatory interaction elements
    XPATH_MEHR_ANZEIGEN = '//*[@id="facets"]/prm-facet/div/div/div[4]/prm-facet-group/div/prm-facet-exact/div/div[2]/button'
    XPATH_NAV_BAR = '/html/body/primo-explore/div[1]/prm-explore-main/ui-view/prm-search/div/md-content/div[2]'
    XPATH_FILTER_ANWENDEN = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-facet/div[1]/div[2]/div/button[2]'

    # Optional Filters
    XPATH_FORSCHUNGSBERICHTE = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-facet/div/div/div[4]/prm-facet-group/div/prm-facet-exact/div/div/div[5]/div/md-checkbox/div[1]'
    XPATH_DISSERTATIONEN = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-facet/div/div/div[4]/prm-facet-group/div/prm-facet-exact/div/div/div[6]/div/md-checkbox/div[1]'
    XPATH_DIPLOMARBEITEN = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-facet/div/div/div[4]/prm-facet-group/div/prm-facet-exact/div/div/div[12]/div/md-checkbox/div[1]'
    XPATH_MASTERARBEITEN = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-facet/div/div/div[4]/prm-facet-group/div/prm-facet-exact/div/div/div[13]/div/md-checkbox/div[1]'
    XPATH_BACHELORARBEITEN = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-facet/div/div/div[4]/prm-facet-group/div/prm-facet-exact/div/div/div[14]/div/md-checkbox/div[1]'

    # add filters you want to apply here
    filter_xpaths = [XPATH_FORSCHUNGSBERICHTE, XPATH_DISSERTATIONEN, XPATH_DIPLOMARBEITEN, XPATH_MASTERARBEITEN, XPATH_BACHELORARBEITEN]

    click_element_by_XPATH(XPATH_MEHR_ANZEIGEN)

    # Wait for loading
    time.sleep(3)

    # need to hover over first button to activate it 
    action = ActionChains(driver)
    action.move_to_element(
        find_element_by_XPATH(filter_xpaths[0])).click().perform()

    time.sleep(1)

    # Scroll in Navbar
    driver.execute_script("arguments[0].scrollIntoView(true);",
                          find_element_by_XPATH(XPATH_NAV_BAR))

    for index in range(1, len(filter_xpaths) - 1):
        click_element_by_XPATH(filter_xpaths[index])

    # Goto Englisch Button
    btn_englisch = driver.find_element(By.CSS_SELECTOR,
                                       "[aria-label='Aufnehmen Englisch  ']")
    driver.execute_script("arguments[0].scrollIntoView();", btn_englisch)
    btn_englisch.click()

    click_element_by_XPATH(XPATH_FILTER_ANWENDEN)


def nextEntry():
    driver.find_element(By.XPATH,
                        ("//button[@aria-label='Zum nächsten "
                         "Datensatz gehen']/prm-icon/md-icon")).click()


def findAbstract():
    '''Returns (success, abstract).'''

    # length to cut away 'mehr...' etc., when additional Text is found
    CUT_SIZE = 7
    text_of_abstract = ''

    try:
        abstract = driver.find_element(By.ID, 'KIT_KITopen_abstract_eng')
        text_of_abstract = abstract.get_attribute('innerHTML')
        try:
            add_abstract = driver.find_element(By.ID,
                                               ('KIT_KITopen_abstract_'
                                                'additional_eng'))
            text_of_abstract = abstract.text[
                0:-(CUT_SIZE + 1)] + add_abstract.get_attribute(
                    'innerHTML').replace("<br>", "")
        except NoSuchElementException:
            pass
    except NoSuchElementException:
        try:
            abstract = driver.find_element(By.ID, 'KIT_KITopen_abstract')
            text_of_abstract = abstract.get_attribute('innerHTML')
            try:
                add_abstract = driver.find_element(By.ID,
                                                   ('KIT_KITopen_'
                                                    'abstract_additional'))
                text_of_abstract = abstract.text[
                    0:-(CUT_SIZE + 1)] + add_abstract.get_attribute(
                        'innerHTML').replace("<br>", "")
            except NoSuchElementException:
                pass
        except NoSuchElementException:
            try:
                abstract = driver.find_element(By.XPATH,
                                               ("//div[@id='KITopen"
                                                "_remote_details']"
                                                "//span[@title='Abstract"
                                                "(englisch)']/../..//div"
                                                "[@class='latex']"))
                text_of_abstract = abstract.get_attribute('innerHTML')
            except NoSuchElementException:
                try:
                    abstract = driver.find_element(By.XPATH,
                                                   ("//div[@id='KITopen"
                                                    "_remote_details"
                                                    "']//span[@title='Abstract"
                                                    "']/../..//div[@class"
                                                    "='latex']"))
                    text_of_abstract = abstract.get_attribute('innerHTML')
                except NoSuchElementException:
                    print('--- Iteration: ' + str(i) + ', no abstract found')
                    return (False, '')
    return (True, text_of_abstract)


def get_text_by_XPATH(XPATH):
    """Returns the text of an element by XPATH.

    Args:
        XPATH (str): XPATH of the element

    Returns:
        _type_: _description_
    """    
    return find_element_by_XPATH(XPATH).text


if WRITE_HEADER:
    with open(OUTPUT_PATH, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)

driver = launchBrowser()
setFilter()

input('Press Enter to start Scraping')

time.sleep(4)
click_element_by_XPATH(XPATH_FIRST_RESULT)
time.sleep(5)

for i in range(NUMBER_OF_RESULTS):

    XPATH_DOCTYPE = ("//span[@title='Publikationstyp']/.."
                     "/../div[2]/div/div/div/prm-highlight/div")
    XPATH_AUTHORS = "//div[@id='KIT_KITopen_allauthors']"
    XPATH_YEAR = ("//div[@id='brief']//span[@data-field"
                  "-selector='creationdate']/prm-highlight/span")
    XPATH_INSTITUTIONS = ("//span[@title='Zugehörige Institution(en)"
                          "am KIT']/../../div[2]/div/div/div/prm-highlight/div")
    XPATH_PAPER_ID = ("//span[@title='Identifikator']/.."
                      "/../div[2]/div/div/div/prm-highlight/div")

    title = doctype = authors = year = institutions = paper_ID = ''

    if i != 0:
        nextEntry()

    try:
        title_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   ("//div[@id="
                                                    "'KITopen_remote_details"
                                                    "']/child::*"))))
        time.sleep(0.5)
        title = driver.find_element(By.XPATH,
                                    ("//div[@id='brief']//"
                                     "span[@data-field-selector"
                                     "='::title']/prm-highlight/span")).text
    except NoSuchElementException: 
        pass
    except TimeoutException:
        print('error')

    # Check for abstract
    # Unfortunately many different versions are present in KIT open...
    foundAbstract, abstract_text = findAbstract

    if not foundAbstract:
        continue

    doctype, authors, year, institutions, paper_ID = get_text_by_XPATH(
        XPATH_DOCTYPE), get_text_by_XPATH(
            XPATH_AUTHORS), get_text_by_XPATH(
                XPATH_YEAR), get_text_by_XPATH(XPATH_PAPER_ID)

    # HEADER = ['Title', 'Doc-Type', 'Authors',
    #           'Year', 'Institutions', 'Paper-ID', 'Abstract']
    row = [title, doctype, authors, year, institutions,
           paper_ID, abstract_text]

    with open(OUTPUT_PATH, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print('+++ Iteration: ' + str(i)+ ', found abstract')
