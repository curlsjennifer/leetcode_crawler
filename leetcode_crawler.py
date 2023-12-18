import base64
import time
import os
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_all_problems(CODE_DRIVER):
    try:
        # if file exists, return directly
        return pd.read_csv("all_problems_list.csv")
    except:
        pass

    # get all problems from api
    CODE_DRIVER.get("https://leetcode.com/api/problems/all")
    html = CODE_DRIVER.find_element(By.XPATH, '/html/body').text
    time.sleep(1)

    # read api using json
    problems_info = json.loads(html)['stat_status_pairs']
    question_id = [item['stat']['question_id'] for item in problems_info]
    question__title = [item['stat']['question__title'] for item in problems_info]
    question__title_slug = [item['stat']['question__title_slug'] for item in problems_info]
    Difficulity = [item['difficulty']['level'] for item in problems_info]
    
    # save information
    data_info, columns = pd.DataFrame({}), ["question_id", "question__title", "Difficulity"]
    for item in columns:data_info[item] = eval(item)
    data_info['title_slug'] = question__title_slug
    
    data_info = data_info.sort_values("question_id")
    data_info.to_csv("all_problems_list.csv", index=False)
    return data_info

def login_leetcode(CODE_DRIVER, username, password):
    # insert username and password using webdriver
    CODE_DRIVER.get("https://leetcode.com/accounts/login")
    CODE_DRIVER.find_element(By.XPATH, '// *[ @ id = "id_login"]').send_keys(username)
    CODE_DRIVER.find_element(By.XPATH, '// *[ @ id = "id_password"]').send_keys(password)
    CODE_DRIVER.find_element(By.XPATH, '// *[ @ id = "id_password"]').send_keys(Keys.ENTER)
    time.sleep(40)
    return CODE_DRIVER

def get_submissions(CODE_DRIVER, problem_list):
    try:
        # if file exists, return directly
        return pd.read_csv("submission.csv")
    except:
        pass

    # get data from api
    url_txt = "https://leetcode.com/api/submissions/?offset={0}&limit=50"
    columns = ['title', 'title_slug', "id", 'lang_name', 'timestamp', 'status_display', 'runtime']
    offset = 0
    data_all = pd.DataFrame({})
    while True:
        try:
            # try to get 10 data each loop
            CODE_DRIVER.get(url_txt.format(offset))
            html = CODE_DRIVER.find_element(By.XPATH, '/html/body/pre').text

            # get information
            submission_info = json.loads(html)["submissions_dump"]
            info = pd.DataFrame({})
            for item in columns:info[item] = [it[item] for it in submission_info]

            # data filter (get accepted data, get new submission id)
            if len(info) < 1:break
            info = info[info["status_display"] == "Accepted"]
            info = info.join(problem_list.set_index('title_slug'), on='title_slug')
            info = info.set_index('id')
            info = info.loc[~info.index.isin(data_all.index)]

            # save submission code and runtime & memory
            info = get_submission_detail(CODE_DRIVER, info)
            data_all = pd.concat([data_all, info])
            offset += 10
            time.sleep(offset%7)
        except:
            break

    data_all = data_all.sort_values("timestamp").drop_duplicates(subset=['title_slug'], keep='last')
    data_all.to_csv("submission.csv", index=False)
    return data_all

def get_submission_detail(CODE_DRIVER, info):
    # save submission code and runtime & memory
    data = []
    for id, num, slug in zip(info.index, info['question_id'], info['title_slug']):
        try:
            url = 'https://leetcode.com/submissions/detail/{0}/'.format(id)
            CODE_DRIVER.get(url)
            code = CODE_DRIVER.find_element(By.XPATH, '//*[@id="ace"]/div/div[3]/div').text
            code_record = open("submission/{0}. {1}.txt".format(num, slug), "w", encoding="utf-8")
            code_record.write(code)
            code_record.close()
            runtime = CODE_DRIVER.find_element(By.XPATH, '//*[@id="runtime_detail_plot_placeholder"]/div[3]/div/div').text.split(" %")[0].split(" ")[-1] + " %"
            memory = CODE_DRIVER.find_element(By.XPATH, '//*[@id="memory_detail_plot_placeholder"]/div[3]/div/div').text.split(" %")[0].split(" ")[-1] + " %"
            data.append([id, runtime, memory])
            print("Problem {0}. {1} captured successfully !".format(num, slug))
        except:
            data.append([id, "0 %", "0 %"])
            print("Problem {0}. {1} captured Fail !".format(num, slug))
        time.sleep(id%7)

    # save data
    info['runtime'] = [it[1] for it in data]
    info['memory'] = [it[2] for it in data]
    info['submission_id'] = [it[0] for it in data]
    return info

if __name__ == "__main__":
    # keyin username, password, and webdriver_path
    username, password = 'curlsjennifer@gmail.com', 'Cjenni37'
    webdriver_path = "C:/Users/Goat/OneDrive/文件/python/chromedriver-win64/chromedriver.exe"
    service = Service(executable_path = webdriver_path)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    CODE_DRIVER = webdriver.Chrome(service=service, options=chrome_options)
    problem_list = get_all_problems(CODE_DRIVER)
    CODE_DRIVER = login_leetcode(CODE_DRIVER, username, password)
    submission_list = get_submissions(CODE_DRIVER, problem_list)

