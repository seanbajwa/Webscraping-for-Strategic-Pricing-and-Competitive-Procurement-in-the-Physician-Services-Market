from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os
import pathlib

SEARCH_URL='https://www.cms.gov/apps/physician-fee-schedule/search/search-results.aspx?Y={}&T=4&HT=1&CT=3&H1={}&H2={}&H3={}&H4={}&H5={}&M=5'
DOWNLOADS='/Users/seanbajwa/Downloads/'

def getCodes(file):
	codes = set()
	with open(file) as f:
		for line in f:
			if len(line) > 0:
				line = line.strip()
				codes.add(line)
	return codes
				
def beginDriver(driver):
	driver.get("https://www.cms.gov/apps/physician-fee-schedule/search/search-criteria.aspx")
	assert "Physician Fee" in driver.title
	terms_accept = driver.find_element_by_id("ctl00_ctl00_ctl00_CMSGMainContentPlaceHolder_ToolContentPlaceHolder_PFSSContentPlaceHolder_accept")
	terms_accept.click()
	time.sleep(1)

def getUrls(codes, years):
	urls = {}
	for year in years:
		urls[year] = []
		for i in range(0,len(codes), 5):
			curr_url = SEARCH_URL.format(year, codes[i], codes[i+1], codes[i+2], codes[i+3], codes[i+4])
			urls[year].append(curr_url)
	return urls

def downloadFile(url, driver):
	driver.get(url)
	download_button = driver.find_element_by_xpath('//*[@title="Download Results"]')
	download_button.click()

def runDriver(urls, actual_years, driver):
	for year in urls:
		print(year)
		path = 'clean_data/{}'.format(actual_years[year])
		pathlib.Path(path).mkdir(exist_ok=True)
		count = 0
		for url in urls[year]:
			downloadFile(url, driver)
			time.sleep(2)
			for f in os.listdir(DOWNLOADS):
				if (f[0] != '.'):
					os.rename('{}{}'.format(DOWNLOADS,f), 'clean_data/{}/{}-{}'.format(actual_years[year],count,f))
			time.sleep(2)
			count += 1
					
if __name__ == '__main__':
	code_file = 'hcpc_codes.txt'
	codes = list(getCodes(code_file))
	years = [i for i in range(3,23)]
	actual_years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008A', '2008B', '2009', '2010A', '2010B', '2011', '2012A', '2012B', '2013', '2014', '2015A', '2015B']
	year_dict = { years[i] : actual_years[len(actual_years)-i-1] for i in range(len(years))}
	driver = webdriver.Firefox()
	beginDriver(driver)
	urls = getUrls(codes, years)
	runDriver(urls, year_dict, driver)
	driver.close()




