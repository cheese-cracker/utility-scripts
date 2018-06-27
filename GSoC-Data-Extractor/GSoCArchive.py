#! /usr/bin/python3
# All GSOC are GSoC!


"""
This program extracts previous-years GSoC data into json files. Then it adds
contents of all these json files into one combined excel file. Remove the json
files with "rm *.json" if it is not needed! Requires jsonExcelerate for
making excel file.
"""

import re
import json
import requests
from jsonExcelerate import wb, populator, filler
from bs4 import BeautifulSoup

FILE_LIST = ["gsoc"+str(x).zfill(2)+".json" for x in range(9, 18)]
session = requests.session()


def clean_name(word):
    word = word.lower()
    if not word.isprintable():
        keep = re.compile("[a-z0-9 -.]+")
        word = "".join(list(filter(keep.search, word)))
    return word


def org_getter(url_list, json4fill):
    for item in url_list:
        org_name = item.text
        org_name = clean_name(org_name)
        org_page_url = "https://www.google-melange.com"+item.get("href")
        org_page = session.get(org_page_url)
        soup = BeautifulSoup(org_page.text, "html.parser")
        projhref = re.compile(item.get('href')+"/projects")
        projects = [proj.text for proj in soup.find_all(href=projhref)]
        org_dict = {
            "name": org_name,
            "no_people": len(projects),
            "projects": projects,
        }
        json4fill.append(org_dict)


def runGSoCold():
    for year in range(9, 16):
        styr = str(year).zfill(2)
        file_name = "gsoc"+styr+".json"
        year_url = "https://www.google-melange.com/archive/gsoc/20"+styr
        Soup = BeautifulSoup(session.get(year_url).text, "html.parser")
        result_set = []
        url_href_type = re.compile("/archive/gsoc/20../orgs/")
        url_list = [item for item in Soup.find_all(href=url_href_type)]
        org_getter(url_list, result_set)
        with open(file_name, 'w') as final_file:
            final_file.write(json.dumps(result_set))
        print("FILE: "+file_name)


"""Below Part scraps GSoC 16/17"""


def url_list(soup):
    urls = soup.find_all('a', 'organization-card__link')
    urls = ['https://summerofcode.withgoogle.com'+x.get('href') for x in urls]
    return urls


def populate(soup, urls, result_set):
    for x in range(len(urls)):
        org_page = session.get(urls[x])
        soup = BeautifulSoup(org_page.text, "html.parser")
        no_people = len(soup.find_all('md-card', 'archive-project-card'))
        org_title = soup.find('h3', 'banner__title').contents[0]
        org_title = clean_name(org_title)
        topic_tags = soup.find_all(
            'li',
            'organization__tag organization__tag--topic')
        topic_tags = [x.contents for x in topic_tags]
        tech_tags = soup.find_all(
            'li',
            'organization__tag organization__tag--technology')
        tech_tags = [x.contents for x in tech_tags]
        mhary_dicty = {
            'name': org_title,
            'no_people': no_people,
            'topic_tags': topic_tags,
            'technology_tags': tech_tags
        }
        result_set.append(mhary_dicty)


URL_2017 = 'https://summerofcode.withgoogle.com/archive/2017/organizations/'
URL_2016 = 'https://summerofcode.withgoogle.com/archive/2016/organizations/'


def runGSoC(file_name, year_url):
    result_set = []
    soup = BeautifulSoup(session.get(year_url).text, "html.parser")
    urls = url_list(soup)
    populate(soup, urls, result_set)
    with open(file_name, 'w') as final_file:
        final_file.write(json.dumps(result_set))
    print("FILE: "+file_name)


"""SCRIPT PART"""

runGSoCold()
runGSoC('gsoc16.json', URL_2016)
runGSoC('gsoc17.json', URL_2017)

# Transferred from jsonExcelerate
# Remove original active sheet and save
sheet0 = wb.active
populator(FILE_LIST)
wb.remove(sheet0)
wb.save('GSoC_Combined.xlsx')
