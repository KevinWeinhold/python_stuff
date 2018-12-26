from bs4 import BeautifulSoup
import requests
import argparse


'''
Here is the basic scraper;
creating parse arguments
'''
parser = argparse.ArgumentParser()
parser.add_argument("-u" , "--url", required = True, help = "Url for website you want to scrape")
parser.add_argument("-f" , "--folder", required = True, help = "Folder name for images")
parser.add_argument("-n" , "--name", required = True, help = "Name for files you want to save")
parser.add_argument("-s" , "--size", required = True, help = "Number of images you want to download from beginning")
args = parser.parse_args()

url = args.url
host_start = url.index('://')+3
host_end = url.index('/',host_start)
host = url[host_start:host_end]
http_type = url[:host_start-2]
#getting webpage HTML
page = requests.get(url)
#print(page.text)

soup = BeautifulSoup(page.text, "html.parser")
links = soup.find_all('img')
#This is to print links to photos
counter = 0

#The downloading loop for each link
for link in links:
    if counter == int(args.size):
        break
    img_src = link.get('src')
    #Adding the img src to http://example.com
    if host in img_src:
        download_url = url[:host_end] + img_src
    else:
        if 'http' in img_src:
             download_url =  img_src
        else:
            download_url = http_type + img_src

    print(f'Downloading: {download_url}')
    data = requests.get(download_url)
    pixelboi = data.headers['Content-length']
    if int(pixelboi) > 1000:
        print(data.headers['Content-length'])

        if data.status_code == 200:
            #writes to a file
            with open(args.folder + '/' + args.name + '_' + str(counter),'wb') as f:
                f.write(data.content)

        counter += 1


    #print(link.get('src'))
#this tells you how many photos there are
#print(len(links))
