# Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import mutagen

import os
import time
import datetime

# user-defined URL of profile
# EXAMPLE: "https://soundgasm.net/u/USERNAME"

# ---- PASTE SOUNDGASM USERNAME TO THIS LINE ----
url = "https://soundgasm.net/u/<USERNAME>"

# ---- REVISE THIS PATH TO MATCH YOUR FILE STRUCTURE ----
rootDirectory = "/mnt/pond/media/Audio/GWA"

# username extraction for folder creation
userSplit = url.split("/")
user = userSplit[-1]

totalItems = 0
newItems = 0
existItems = 0

userDirectory = "{0}/{1}".format(rootDirectory, user)

if not(os.path.exists(userDirectory)):
  make_Command = "mkdir " + userDirectory
  os.system(make_Command)

#  driver options boilerplate #

# options for webdriver
options = Options()
options.add_argument("--headless")
# options.add_argument("--window-size=192x108")
options.add_argument("user-data-dir=selenium")

# options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # automation detection evasion
options.add_experimental_option('useAutomationExtension', False)  # automation detection evasion

# driver = webdriver.Chrome(options=options, executable_path="./sel_driver/chromedriver")

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(60)

recording_driver = webdriver.Chrome(options=options)
recording_driver.set_page_load_timeout(60)

print("Getting URL list...")

# profile get
driver.get(url)
# media posts extraction
fileList = driver.find_elements(By.XPATH,'/html/body/div[*]/a')
totalItems = len(fileList)

print("Downloading files...")
for sound_link in fileList:	
  # variable Flushing
	name = ""
	title = ""
	link = ""
	descr = ""
	releaseDate = ""
	trackNum = ""

	recordingPage = sound_link.get_attribute("href")
	if recordingPage is not None:
		url_split = recordingPage.split("/")
		
		# ---- get recording title ----
		title = url_split[-1].replace("-", " ")  # make pretty

		recording_path = '{0}/{1}.m4a'.format(userDirectory, title)
		if not(os.path.isfile(recording_path)):
			#print("Title: " + title)
			recording_driver.get(recordingPage)
			time.sleep(2)  # slow your roll let it load, req'd to give time for file url to return
		
			# ---- get artist ----
			# name = recording_driver.find_element(By.XPATH,'/html/body/div[1]/a', ).text.replace("'", "").replace('"', "").replace('/', " ").replace('*', " ")
			# print("name: " + name)

			# ---- get recording description ----
			descr = recording_driver.find_element(By.CLASS_NAME,"jp-description").text
			descr = descr.replace("'", "") # removing quote characters from metadata, see TIDAL script for more correct fix
			# print("descr: " + descr)

			# ---- get audio file url ----
			link = recording_driver.find_element(By.XPATH,'//*[@id="jp_audio_0"]').get_attribute("src")
			# print("link: " + link)
		
			# ---- download audio file ----
			w_Get_command = "wget {0} -nv -c -O '{1}' > /dev/null 2>&1".format(link, recording_path)# .split()
			os.system(w_Get_command)
			
			# ---- get date of soundgasm file, seems to be the upload date ----            
			modDate = os.path.getmtime(recording_path) # %m/%d/%Y
			# releaseDate = (datetime.datetime.fromtimestamp(modDate).strftime("%m-%d-%Y"))
			releaseDate = (datetime.datetime.fromtimestamp(modDate).strftime("%Y-%m-%d"))
			print(releaseDate + " " + title)
			with open(recording_path, 'r+b') as file:
				media_file = mutagen.File(file, easy=True)
				media_file['title'] = title
				media_file['album'] = user # title
				media_file['artist'] = user
				media_file['comment'] = descr
				media_file['date'] = releaseDate
				media_file['tracknumber'] = str((totalItems - (newItems + existItems))) + '/0'
				media_file.save(file)
			newItems = newItems + 1

		else:
			existItems = existItems + 1
	else:
		print("Broken Link")

print("\n---- Track Summary ----\nExisting:\t" + str(existItems) + "\nNew:\t\t" + str(newItems)+ "\nTotal:\t\t" + str(totalItems))
driver.quit()
recording_driver.quit()
