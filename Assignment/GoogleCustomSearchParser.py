import json
import random
import requests
from bs4 import BeautifulSoup


res_dict = {}
text = input("Enter the keyword to search: ")
print("Fetching Results from Google...")
res_dict["keyword"] = text
url = 'https://google.com/search?q=' + text
A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
       )
 
Agent = A[random.randrange(len(A))]
headers = {'user-agent': Agent}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

all_top = soup.find_all('g-scrolling-carousel')
top_results = all_top[0].find_all('div',class_='JJZKK') if len(all_top)>0 else ""
results = soup.find_all('div',class_='rc')

counter = 0
res_dict["results"] = {}
res_dict["results"]["top_results"] = {}
res_dict["results"]["organic_results"] = {}

for result in top_results[:3]:
    counter += 1
    indi_dict = {}
    temp = result.find_all('div',class_='mCBkyc oz3cqf p5AXld nDgy9d')[0].text
    indi_dict['title'] = temp
    ttemp = result.find_all('g-img',class_='RdhoHd')
    indi_dict['site_name'] = ttemp[0].select('img')[0].get('alt') if len(ttemp)>0 else ""
    indi_dict['link'] = result.find_all('a')[0].get('href')
    indi_dict['description'] = temp
    res_dict["results"]["top_results"][counter]= indi_dict

counter = 0
for result in results:
    counter += 1
    indi_dict = {}
    indi_dict["title"] = result.select('span')[0].text
    indi_dict["site_name"] = result.select('cite')[0].text
    indi_dict["link"] = result.select('a')[0].get('href')
    indi_dict["description"] = "".join([x.text for x in result.find('div',class_="IsZvec").select("span")])
    res_dict["results"]["organic_results"][counter]= indi_dict

with open(f"./Outputs/results_{text}.json","w") as fl:
    json.dump(res_dict,fl,indent=2)

print("Data fetched and written to JSON Successfully.")