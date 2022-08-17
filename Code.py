# Importing Libraries
import urllib.request as url
from bs4 import BeautifulSoup as bs


# Mounting with Google Drive Files
# Note: the code is meant to run on Google Colab
from google.colab import drive
drive.mount('/content/drive')


# Accessing Desired Website and Finding all Companies' URLS
arr_links = []
for i in range(1,350):
  URL = "https://www.great.gov.uk/international/trade/search/?industries=AEROSPACE&industries=ADVANCED_MANUFACTURING&industries=AIRPORTS&industries=AGRICULTURE_HORTICULTURE_AND_FISHERIES&industries=AUTOMOTIVE&industries=BIOTECHNOLOGY_AND_PHARMACEUTICALS&industries=BUSINESS_AND_CONSUMER_SERVICES&industries=CHEMICALS&industries=CLOTHING_FOOTWEAR_AND_FASHION&industries=COMMUNICATIONS&industries=CONSTRUCTION&industries=CREATIVE_AND_MEDIA&industries=EDUCATION_AND_TRAINING&industries=ELECTRONICS_AND_IT_HARDWARE&industries=ENVIRONMENT&industries=FINANCIAL_AND_PROFESSIONAL_SERVICES&industries=FOOD_AND_DRINK&industries=GIFTWARE_JEWELLERY_AND_TABLEWARE&industries=GLOBAL_SPORTS_INFRASTRUCTURE&industries=HEALTHCARE_AND_MEDICAL&industries=HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS&industries=LIFE_SCIENCES&industries=LEISURE_AND_TOURISM&industries=LEGAL_SERVICES&industries=MARINE&industries=MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING&industries=METALLURGICAL_PROCESS_PLANT&industries=METALS_MINERALS_AND_MATERIALS&industries=MINING&industries=OIL_AND_GAS&industries=PORTS_AND_LOGISTICS&industries=POWER&industries=RAILWAYS&industries=RENEWABLE_ENERGY&industries=RETAIL_AND_LUXURY&industries=SECURITY&industries=SOFTWARE_AND_COMPUTER_SERVICES&industries=TEXTILES_INTERIOR_TEXTILES_AND_CARPETS&industries=WATER&page="
  website = URL + str(i)
  try:
    # Creating a Soup out of the Desired Website:
    req = url.Request(website, headers={'User-Agent' : 'Magic Browser'})
    con = url.urlopen(req)
    soup = bs(con.read())
    # Printing Page Number to Check Live Progress:
    print(i)
    # Checking for URLs inside Companies' Cards:
    companies_urls = soup.find('div',{'id':'companies-column'}).find('ul').findAll('li')
    for company_url in companies_urls:
      arr_links.append("https://www.great.gov.uk"+company_url.a['href'])
  except:
    # Printing Page Loading Errors (if any):
    print(str(i) + " ERROR")
    pass
    
# Extracting Names, Number of Employees, and Descriptions
names = []
employees = []
descriptions = []
faulty_links = []
count = 1
for link in arr_links:
  try:
    # Creating a Soup out of each Company's Profile Page:
    req = url.Request(link, headers={'User-Agent' : 'Magic Browser'})
    con = url.urlopen(req)
    soup = bs(con.read())
    # Checking for Company Name & Number of Employees Information:
    names.append(soup.find('div',{'id':'content-column'}).find('h2').text.strip())
    employees.append(soup.find('div',{'id':'data-column'}).findAll('dd')[2].text.strip())
    # Printing Live Status:
    print(count)
    count += 1
    # Creating a Soup out of the Description Page:
    req = url.Request(link[:link.find("?")]+soup.find('div',{'id':"company-description-container"}).findAll('p')[-1].a['href'], headers={'User-Agent' : 'Magic Browser'})
    con = url.urlopen(req)
    soup = bs(con.read())
    # Checking for all paragraphs in Description Page:
    paragraphs = soup.find('div',{'id':'company-description-container'}).findAll('p')[1:]
    description = ""
    for paragraph in paragraphs:
      # Concatenating Paragraphs in Single String (also fixing the quotation mark problem to avoid conflict with the csv format):
      description += paragraph.text.replace('"',"''") + "\n"
    descriptions.append(description)
  except:
    # Printing & Storing Faulty Companies' URLs (to resolve them manually):
    print("ERROR: " + link)
    faulty_links.append(link)
    pass
    
# Writing Results in CSV file (Note: the file needs to be created in Google Drive before compiling these lines)
f = open('/content/drive/My Drive/Colab Notebooks/companies_data.csv', 'w')
f.write("Company Name,No. of Employees,Company Description\n")
for i in range(count-1):
  f.write(names[i] + "," + employees[i] + ", \"" + descriptions[i] + "\"\n")
f.close()
