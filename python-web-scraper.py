import requests
from bs4 import BeautifulSoup
import re

url = "https://berlinstartupjobs.com/"

all_jobs = []
all_skills = []

# check pagenation
def get_pages(url):
    response = requests.get(url + "engineering/", headers = {'User-agent': 'your bot 0.1'})
    soup = BeautifulSoup(response.content, "html.parser")
    pages = len(soup.find("ul", class_="bsj-nav").find_all(class_="page-numbers")[0:-1])
    return pages

# extract all skills
def scrap_skills(url):
    response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
    soup = BeautifulSoup(response.content, "html.parser")
    skills = soup.find("section").find("div", id="skills-list").find("ul").find_all("li")
    for skill in skills:
        skill = skill.find("a").text.lower()
        pattern = re.compile(r"\s*(.+?)\s*\(.*\)$")
        skill = pattern.search(skill).group(1)
        skill = skill.replace(" ", "-")
        if skill == "marketing":
            skill = skill + "-2" # marketing url change
        all_skills.append(skill)
scrap_skills(url)

# extract jobs
def scrap_page(url):
    print(url)
    response = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("ul", class_="jobs-list-items").find_all("li")

    for job in jobs:
        header = job.find("div", class_="bjs-jlid__header").find_all("a")
        title = header[0].text
        company = header[-1].text
        desciption = job.find("div", class_="bjs-jlid__description").text
        pattern = re.compile(r"\n\t\t\t(.+?)\t\t")
        desciption = pattern.findall(desciption)
        job_url = header[0]
        if job_url:
            job_url = job_url["href"]

        job_data = {
            "title": title,
            "company": company,
            "desciption": desciption,
            "link": job_url,
        }
        all_jobs.append(job_data)

# extract job by skill
def scrap_jobs_by_skill(url, skill):
    by_skill = f"skill-areas/{skill}/"
    scrap_page(url + by_skill)

for page in range(get_pages(url)):
    scrap_page(url + f"engineering/page/{page + 1}/")

for skill in all_skills:
    scrap_jobs_by_skill(url, skill)

print(all_jobs)