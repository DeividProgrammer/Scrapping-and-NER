import json
import time
import requests
from bs4 import BeautifulSoup


def addToJsonFile(res):
    json_data = json.dumps(res, indent=4)
    with open('../results/projectData.json', 'w') as f:
        f.write(json_data)


def get_dates(soup):
    script_tag = soup.find('script', type='application/ld+json')
    json_data = script_tag.string
    parsed_json = json.loads(json_data)
    date_modified = parsed_json['dateModified']
    date_published = parsed_json['datePublished']

    return date_modified, date_published


def get_project_information(soup):
    paragraphs = soup.findAll('section', class_="work__info__section col col--right")
    project_information = ' '.join(paragraph.get_text() for paragraph in paragraphs)
    return project_information


def get_teams(soup):
    teams_list = soup.find('div', class_='work__info__team')
    return [team.get_text() for team in teams_list.find_all('li') if team.text != '-' or team.text != ""]


def crawler(seed, crawl_interval, crawl_depth_limit, user_agent):
    frontier = {(seed, 0)}
    crawled = []
    firstIteration = True
    res = []
    i=0
    while frontier and i<=25:
    #after crawling 25 pages we stop for timming issues but this filter should be deleted
        i+=1
        page, depth = frontier.pop()
        try:
            print('Crawled:', page)
            source = requests.get(page, headers={'User-Agent': user_agent}).text
            soup = BeautifulSoup(source, 'html.parser')

            if firstIteration:
                links = soup.find_all('a')
                firstIteration = False

            else:  # projects information
                related_projects_route = soup.find_all('a', class_='work-card__link')
                related_projects_url = {'https://www.wearecollins.com' + p['href'] for p in related_projects_route}

                project_title = soup.find('h4', class_='work__info-toggle')  # .text
                if project_title != None:
                    project_title = project_title.text
                    teams = get_teams(soup)
                    date_modified, date_published = get_dates(soup)
                    project_information = get_project_information(soup)
                    links = related_projects_route

                    res.append({'project_title': project_title, 'team': teams,
                                'project_information': project_information,
                                'date_modified': date_modified,
                                'date_published': date_published,
                                'project_url': page,
                                'related_projects': list(related_projects_url)})



            if page not in crawled and depth < crawl_depth_limit:
                for link in links:
                    if 'work' in link['href']:
                        url = 'https://www.wearecollins.com' + link['href']
                        if url not in crawled:
                            frontier.add((url, depth + 1))
                crawled.append(page)

            time.sleep(crawl_interval)


        except Exception as e:
            print(e)
    return res


if __name__ == "__main__":
    seed = 'https://www.wearecollins.com/work/'
    crawl_interval = 1
    crawl_depth = 4
    user_agent = 'Mozilla/5.0'

    result = crawler(seed, crawl_interval, crawl_depth, user_agent)
    addToJsonFile(result)