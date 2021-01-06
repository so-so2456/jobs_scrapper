import requests
from bs4 import BeautifulSoup


def get_last_pages(url):
    request = requests.get(url)
    result = BeautifulSoup(request.text, "html.parser")
    pages = result.find_all("a", class_="s-pagination--item")
    last_page = pages[-2].get_text(strip=True)
    last_page = int(last_page)
    return last_page


def extract_job(card):
    job_id = card["data-jobid"]
    title = card.find("a", class_="s-link")["title"]
    company, location = card.find(
        "h3", class_="mb4").find_all(
            "span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping stackoverflow page {page+1}..")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        job_list = soup.find_all("div", class_="-job")
        for job_card in job_list:
            jobs.append(extract_job(job_card))
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_pages(url)
    jobs = extract_jobs(last_page, url)
    return jobs
