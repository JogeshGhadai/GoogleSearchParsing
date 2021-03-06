import os
import json
import yaml
import random
import logging
import requests
from bs4 import BeautifulSoup


def get_all_config(conf_file_path):
    """
    It fetches all the configurations required from config file.
    
    Parameters
    ----------
    conf_file_path : str
        It contains Config file's path.
    
    Returns
    -------
    dict
    """
    all_conf = None
    
    try:
        with open(conf_file_path) as f:
            all_conf = yaml.load(f, Loader=yaml.FullLoader)
    
    except Exception as e:
        logging.error("Error in opening the config file."+e.message)
    
    finally:
        return all_conf


def get_web_agent(all_conf):
    """
    It selects a random web agent from the web agents list present
    in the Configuration file.
    
    Parameters
    ----------
    all_conf : dict
        It contains all the configuration data required.
    
    Returns
    -------
    str
    """
    selected_agent = None
    
    try:
        all_agents_list = all_conf["agents_list"]
        selected_agent = all_agents_list[random.randrange(len(all_agents_list))]
    
    except Exception as e:
        logging.error("Error in fetching the agents list from config file."+e.message)
    
    finally:
        return selected_agent


def check_make_outputs_directory(dir_path):
    """
    It checks for the presence of Outputs Directory, if not present
    then creates the same.
    
    Parameters
    ----------
    dir_path : str
        It contains the path of Outputs directory.
    """
    
    if not(os.path.exists(dir_path)):
        os.mkdir(dir_path)


def write_results_to_json(all_conf, res_dict, text):
    """
    It writes the results fetched to JSON output files.
    
    Parameters
    ----------
    all_conf : dict
        It contains all the configuration data required.
    res_dict : dict
        It contains all the results fetched.
    text : str
        It contains the Text input to the program to include the same in the
        output JSON file's name.
    """
    
    try:
        with open(f"{all_conf['out_file_path']}results_{text.replace(' ', '_')}.json","w") as fl:
            json.dump(res_dict,fl,indent=2)
    
        logging.info("Data written to JSON Successfully.")
    
    except Exception as e:
        logging.error("Error in writing results to JSON."+e.message)


def get_result_dict(all_conf, text):
    """
    It takes the text keyword as input and fetches the results for the
    same from Google and returns them in the form of a dictionary.
    
    Parameters
    ----------
    all_conf : dict
        It contains all the configuration data required.
    text : str
        It contains the Text input to the program which is used to search
        in the Google.
    
    Returns
    -------
    dict
    """
    
    try:
        url = all_conf["search_url"] + text
        selected_agent = get_web_agent(all_conf)
        headers = {'user-agent': selected_agent}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_top = soup.find_all('g-scrolling-carousel', class_='F8yfEe')
        results = soup.find_all('div',class_='rc')

        counter = 0
        res_dict = {}
        res_dict["keyword"] = text
        res_dict["results"] = {}
        res_dict["results"]["organic_results"] = {}
        res_dict["results"]["other_results"] = {}
    
        for result in results:
            counter += 1
            indi_dict = {}
            indi_dict["title"] = result.select('span')[0].text
            indi_dict["site_name"] = result.select('cite')[0].text
            indi_dict["link"] = result.select('a')[0].get('href')
            indi_dict["description"] = "".join([x.text for x in result.find('div',class_="IsZvec").select("span")])
            res_dict["results"]["organic_results"][counter]= indi_dict
        
        first_res_flag = 1
        section_counter = 0
        
        for results in all_top:
            top_results = results.find_all('div',class_='JJZKK')
            counter = 0
            
            if first_res_flag:
                res_dict["results"]["other_results"]["top_results"] = {}
            
            else:
                section_counter += 1
                res_dict["results"]["other_results"][f"section_{section_counter}"] = {}
            
            for result in top_results[:3]:
                counter += 1
                indi_dict = {}
                temp = result.find_all('div',class_='mCBkyc oz3cqf p5AXld nDgy9d')[0].text
                indi_dict['title'] = temp
                ttemp = result.find_all('g-img',class_='RdhoHd')
                indi_dict['site_name'] = ttemp[0].select('img')[0].get('alt') if len(ttemp)>0 else ""
                indi_dict['link'] = result.find_all('a')[0].get('href')
                indi_dict['description'] = temp
                
                if first_res_flag:
                    res_dict["results"]["other_results"]["top_results"][counter] = indi_dict
                
                else:
                    res_dict["results"]["other_results"][f"section_{section_counter}"][counter] = indi_dict
            
            if first_res_flag:
                first_res_flag = 0
   
        logging.info("Results fetched from Google Successfully.")
        
    except Exception as e:
        logging.error("Error in fetching search results from Google."+e.message)
    
    finally:
        return res_dict


if __name__ == "__main__":
    text = input("Enter the keyword to search: ")
    logging.info("Fetching Results from Google...")
    all_conf = get_all_config("./config.yaml")
    res_dict = get_result_dict(all_conf, text)
    check_make_outputs_directory(all_conf['out_file_path'])
    write_results_to_json(all_conf, res_dict, text)
