import json
import yaml
import random
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    all_conf = get_all_config("./config.yaml")
    res_dict = {}
    text = input("Enter the keyword to search: ")
    print("Fetching Results from Google...")
    res_dict["keyword"] = text
    url = all_conf["search_url"] + text

    all_agents_list = all_conf["agents_list"]
    selected_agent = all_agents_list[random.randrange(len(all_agents_list))]
    headers = {'user-agent': selected_agent}
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

    with open(f"{all_conf["out_file_path"]}results_{text.replace(" ", "_")}.json","w") as fl:
        json.dump(res_dict,fl,indent=2)

    print("Data fetched and written to JSON Successfully.")

def get_all_config(conf_file_path):
    all_conf = None
    try:
        with open(conf_file_path) as f:
            all_conf = yaml.load(f, Loader=yaml.FullLoader)
    except:
        all_conf = None
        print("Error in opening the config file.")
    finally:
        return all_conf