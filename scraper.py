# Import libraries and packages for the project 
from logging.config import IDENTIFIER
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import csv
print('- Finish importing packages')

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome()
sleep(2)
url ='https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Task 1.2: Import username and password
credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print('- Finish importing the login credentials')
sleep(2)


# Task 1.2: Key in login credentials
email_field = driver.find_element(By.ID, 'username')
email_field.send_keys(username)
print('- Finish keying in email')
sleep(3)


password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(password)
print('- Finish keying in password')
sleep(2)

# Task 1.2: Click the Login button
signin_field = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
sleep(3)

print('- Finish Task 1: Login to Linkedin')

# Task 2: Search for the profile we want to craw



search_field = driver.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input')

# Task 2.2: Input the search query to the search bar
search_query = input('What profile do you want to scrape? ')
search_field.send_keys(search_query)

# Task 2.3: Search
search_field.send_keys(Keys.RETURN)

print('- Finish Task 2: Search for profiles')

sleep(5)
# Task 2.4: Click the people button


# Task 3: Scrape the URLs of the profiles
# Task 3.1: Write a function to extract the URLs of one page
def GetURL():
    page_source = BeautifulSoup(driver.page_source,'html.parser')
    profiles = page_source.find_all('a', class_ = 'app-aware-link') #('a', class_ = 'search-result__result-link ember-view')
    all_profile_URL = []
    for profile in profiles:
        # profile_ID = profile.get('href')
        # profile_URL = "https://www.linkedin.com" + profile_ID
        profile_URL = profile.get('href')
        if profile_URL not in all_profile_URL:
            all_profile_URL.append(profile_URL)
    return all_profile_URL


# Task 3.2: Navigate through many page, and extract the profile URLs of each page
input_page = int(input('How many pages you want to scrape: '))
URLs_all_page = []
for page in range(input_page):
    URLs_one_page = GetURL()
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
    sleep(3)
    next_button = driver.find_element(By.CLASS_NAME,"artdeco-pagination__button--next")
    driver.execute_script("arguments[0].click();", next_button)
    URLs_all_page = URLs_all_page + URLs_one_page
    sleep(2)

print('- Finish Task 3: Scrape the URLs')


# Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
with open('output1.csv', 'w',  newline = '') as file_output:
    headers = ['Name', 'Location', 'Job Title', 'Current Job','company','education','year','coursename','company2']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        driver.get(linkedin_URL)
        print('- Accessing profile: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find('main',{'class':"scaffold-layout__main"})
        try:
            name = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Profile name is: ', name)
            location = info_div.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Profile location is: ', location)
            title = info_div.find('div', class_='text-body-medium break-words').get_text().strip()
            print('--- Profile title is: ', title)
            current_job = info_div.find('div',class_='display-flex flex-row justify-space-between').get_text().strip()
            print('--- Profile current job is: ', current_job )
            company = info_div.find('span',class_='pv-text-details__right-panel-item-text hoverable-link-text break-words text-body-small t-black').get_text().strip()
            print('--- Profile current job is: ', company )
            education = info_div.find('span',class_='pv-text-details__right-panel-item-text hoverable-link-text break-words text-body-small t-black').get_text().strip()          
            print('--- Profile current job is: ',education )
            year = info_div.find('span',class_='t-14 t-normal t-black--light').get_text().strip()
            print('--- Profile current job is: ', year )
            Course_name = info_div.find('span',class_='t-14 t-normal').get_text().strip()
            print('--- Profile current job is: ', Course_name )
            company1 = info_div.find('span',class_='mr1 t-bold').get_text().strip()
            print('--- Profile current job is: ', company1 )






            writer.writerow({headers[0]:name, headers[1]:location, headers[2]:title, headers[3]:current_job, headers[4]:company, headers[5]:education, headers[6]:year, headers[7]:Course_name, headers[8]:company1})
            print('\n')
        except:
            pass

print('Mission Completed!')
