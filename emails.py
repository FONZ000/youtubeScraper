import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import re

# Function to check for email addresses in a text
def extract_emails(text):
    # Regular expression pattern for matching email addresses
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    
    # Find all email addresses in the text
    emails = re.findall(email_pattern, text)
    
    return emails

# Set Email limit
email_limit = 1000  # Change this to the desired limit
email_count = 0
seen_emails = set()

# Seconds to hh:mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)


# Timer
start_time = time.time()

print('Category examples: Crypto, Tech review, travelling, programming, ..., etc')
criteria = str(input("Please enter the category you desire (Press ENTER if you don't want a category): "))
email_limit = int(input("Please enter the number of emails you want to scrape: "))

# The URL you want to scrape
url = f"https://playboard.co/en/search?q={criteria}"


def set_date(option):
    match option:
        case 0:
            url_date = ''
        case 1:
            url_date = '&lastAdAt=15%3A'
        case 2:
            url_date = '&lastAdAt=30%3A'
        case _:
            print('Invalid input!')
            url_date = ''

    return url_date

def set_country(option):
    match option:
        case 0:
            url_country = ''
        case 1:
            url_country = '&country=RU'
        case 2:
            url_country = '&country=US'
        case 3:
            url_country = '&country=GB'
        case 4:
            url_country = '&country=CA'
        case 5:
            url_country = '&country=FR'
        case 6:
            url_country = '&country=JP'
        case 7:
            url_country = '&country=IN'
        case _:
            print('Invalid input!')
            url_country = ''

    return url_country

sub_option_min = int(input("Enter subscribers minimum bound of range: ")) 
sub_option_max = int(input("Enter subscribers maximum bound of range: ")) 

url_subs = ''

if sub_option_min <= 0 and sub_option_max <=0:
    url_subs = ''

elif sub_option_min >= 0 and sub_option_max <= 0:
    url_subs = f'&subscribers={sub_option_min}%3A'

elif sub_option_min <= 0 and sub_option_max > 0:
    url_subs = f'&subscribers={sub_option_max}%3A'

elif sub_option_min > 0 and sub_option_max > 0 and sub_option_min < sub_option_max:
    url_subs = f'&subscribers={sub_option_min}%3A{sub_option_max}'

else:
    print('Error')


print("Choose last promotion if you don't want to choose just press 0!'")
print("1: Past 15 days")
print("2: past 30 days")

date_option = int(input("Enter subscribers range (1 or 2): "))
date_range = set_date(date_option)

print("Choose Country if you don't want to choose just press 0!'")
print("1: Russian Federation")
print("2: United States")
print("3: United Kingdom")
print("4: Canada")
print("5: France")
print("6: Japan")
print("7: India")

country_option = int(input("Choose country if you don't want to choose just press 0!"))
country_url = set_country(country_option)

if url_subs == '' and date_range == '' and country_url == '':
    url = f"https://playboard.co/en/search?q={criteria}"

else:
    url = f"https://playboard.co/en/search?q={criteria}{url_subs}{date_range}{country_url}&sortTypeId=1"



email_count = 0
# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
driver.get(url)

# Wait for the page to load initially
time.sleep(2)

# Save the scraped data to a CSV file
csv_filename = "scraped_data.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["EMAIL"])


    # Scroll to the end of the page
    while True:
        # Scroll down to trigger infinite scrolling
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        # Wait for 2 seconds to load more content
        time.sleep(6)

        # Get the page source
        page_source = driver.page_source
        # print(page_source)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all elements with class "channels"
        channels = soup.find(class_="channels")

        channels_list = channels.find_all(class_="list")

        for channel in channels_list:
            # Find elements with class "channel-cell" or "list__item"
            channel_items = channel.find_all(class_="channel-cell")
            
            for item in channel_items:
                # Find the div with class "meta"
                meta_div = item.find(class_="meta")
                if meta_div:
                    # Find the div with class "desc"
                    desc_div = item.find(class_="desc")
                    if desc_div:
                        desc_text = desc_div.get_text(strip=True)
                        only_emails = extract_emails(desc_text)
                    
                        
                        for email in only_emails:
                            if email not in seen_emails:
                                csv_writer.writerow([email])
                                seen_emails.add(email)
                                email_count += 1

                            if email_count >= email_limit:
                                print(f"Reached the limit of {email_limit} emails.")
                                break

                        if email_count >= email_limit:
                            break
                
            if email_count >= email_limit:
                break
                
        if email_count >= email_limit:
            break

        # Check if you have reached the end of the page
        current_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(20)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == current_height:
            break

    # Close the web browser
    driver.close()

end_time = time.time()
elapsed_time = end_time - start_time
final_time = convert_seconds(elapsed_time)

print(f"Data has been scraped and saved to {csv_filename}")
print("{} Emails out of {} email has been scraped in {}".format(email_count, email_limit, final_time))
