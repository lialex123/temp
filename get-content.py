import os
from collections import namedtuple
from lxml import html
import cchardet as chardet
from itertools import chain
from bs4 import BeautifulSoup, FeatureNotFound

RawStory = namedtuple('RawStory', 'url html')
StoryTitle = namedtuple('StoryTitle', 'url title')
StoryRestContent = namedtuple('StoryRestContent', 'url restcontent')

def get_download_file_name(url):
  fileid = url.replace("http://web.archive.org/web/", "")
  fileid = fileid.replace("http://", "")
  htmlfileid = fileid.replace("/", "-") + ".html"
  return htmlfileid

if __name__ == "__main__":
  download_dir = "./xsum-raw-downloads"
  map_webarxiv_bbcid_file = "XSum-WebArxiveUrls-BBCids.txt"
  
  result_dir = "./xsum-extracts-from-downloads"
  os.system("mkdir -p "+result_dir)
  failed_id_file = open("xsum-extracts-from-downloads-failedIds.txt", "w")

  # Get all bbcids
  bbcids_dict = {}
  for line in open(map_webarxiv_bbcid_file).readlines():
    data = line.strip().split()
    bbcids_dict[data[1]] = data[0]
  print(len(bbcids_dict))

  count = 0

  # Process all downloads
  for bbcid in bbcids_dict:
    
    if os.path.isfile(result_dir+"/"+bbcid+".data"):
      # Alread processed
      continue

    webarxivid = bbcids_dict[bbcid]
    downloaded_file = download_dir+"/"+get_download_file_name(webarxivid)
    
    if not os.path.isfile(downloaded_file):
      failed_id_file.write(bbcid+"\tHTML FILE IS NOT YET DOWNLOADED.\n")
      continue

    html = open(downloaded_file).read()
    if (html == ""):
        continue
    
    parsed_html = BeautifulSoup(html, features="lxml")
    #print(downloaded_file)
    #print(parsed_html.find('title').text)
    #print(parsed_html.find('time'))
    if ('-sport-' in downloaded_file):
        continue
        #print(parsed_html.find('meta', attrs={'property':'rnews:datePublished'})['content'])
    elif('-news-' in downloaded_file):
        continue
        #print(parsed_html.find('div', attrs={'class':'date date--v2'})['data-datetime'])
    else:
        print(downloaded_file)
