import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import re

BASE_URL = "https://www.work.ua"


def years_to_level(yrs):
    if yrs <= 1: return "junior"
    if yrs <= 4: return "middle"
    return "senior"


def determine_experience(text):
    text = text.lower()

    if re.search(r"\b(trainee|intern|internship)\b", text): return "junior"
    if re.search(r"\b(junior|jr)\b", text): return "junior"
    if re.search(r"\b(middle|mid)\b", text): return "middle"
    if re.search(r"\b(senior|sr|lead|architect)\b", text): return "senior"

    if re.search(r"(без досвіду|no experience|готові взяти студента)", text):
        return "junior"

    m = re.search(r"(\d)\s*(?:years?|yrs?|рок|років|р\.|рр\.)", text)
    if m:
        yrs = int(m.group(1))
        if yrs <= 1: return "junior"
        if yrs <= 4: return "middle"
        return "senior"

    return "unknown"


def get_vacancy_links(max_pages=20):
    all_links = []
    for page in range(1, max_pages + 1):
        print(f"Parsing the page {page}...")
        url = f"{BASE_URL}/jobs-python/?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.select("div.job-link")
        for job in jobs:
            a = job.select_one("h2 a")
            if a:
                href = a.get("href")
                all_links.append(BASE_URL + href)
        time.sleep(1)
    return all_links


def get_vacancy_description(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            desc_div = soup.find("div", id="job-description")
            return desc_div.get_text(separator=" ", strip=True) if desc_div else ""
    except:
        return ""
    return ""


def save_to_csv(data):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'vacancies.csv')

    fieldnames = ['url', 'description', 'experience_level']

    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"\n✅ Data with experience saved in {file_path}")


if __name__ == "__main__":
    links = get_vacancy_links(max_pages=20)
    scraped_data = []

    for index, link in enumerate(links[:15]):
        print(f"[{index + 1}/{len(links[:15])}] processing : {link}")
        desc = get_vacancy_description(link)
        if desc:
            level = determine_experience(desc)
            scraped_data.append({
                'url': link,
                'description': desc,
                'experience_level': level
            })
        time.sleep(1)

    save_to_csv(scraped_data)
