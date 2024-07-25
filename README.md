# SoundgasmDOTnet profile scraper  

A re-write of the original script.  

Changes:  
- check for existing files and directory before downloading new files from site, allows for incremental updates to existing file collections.  
- use of mutagen to set metatdata in file to be populated with content from site. Metadata includes:  
  - Title - title of track  
  - Album - title of track  
  - Artist - Soundgasm user  
  - Comment - recording description in Soundgasm  
  - Date - release date based on Soundgasm file metadata
  - Track Number - keeps tracks in order of date published to site
- omitted raw.txt file usage, was causing issues when re-checking collections for new files

### NEW DEPENDENCY
`pip install mutagen`  

A rather elementary profile scraper that will download all the publicly available audio files associated with any one account. This script requires selenium Webdriver specifically the Chrome variant.   
**This script requires editing to function.**   
- You are required to manually paste in the link to the profile you wish to scrape.  
- You are required to manually enter the path to which the files are to be downloaded, change the prefix of the `recording_path` variable (IN TWO LOCATIONS).   

### Requirements  
Python 3.7+  
Chrome selenium Webdriver (installed to the specified location in the script)  
OS agnostic as long as wget is functional.


#### Disclaimer
I do not condone or suggest the use of the script for any reason and this script is for educational purposes only.  
You should always respect the robots.txt of any website.
