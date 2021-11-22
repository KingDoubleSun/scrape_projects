import json
import re
import sys
from bs4 import BeautifulSoup
import requests


def get_game_data(url, headers):
    base_url = "https://www.freetogame.com"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features='lxml')

    game_data = {}
    # video
    try:
        video = soup.find('video')
        game_data['video_src'] = base_url + video.source["src"]
    except TypeError:
        print("no video", url)
        game_data['video_src'] = None

    # about <div id="summary">
    a = soup.find('div', id="summary")
    game_data["about"] = a.get_text()

    # screenshots <div class="row text-center text-lg-left"> <a href=>
    try:
        screenshots = soup.find('div', {'class': "row text-center text-lg-left"}).find_all('a')
        game_data["screenshots"] = [base_url + a["href"] for a in screenshots]
    except AttributeError:
        print("no screenshots", url)

    # pc requirements
    try:
        minimum_req = soup.find(lambda tag: re.match(r'Minimum', tag.get_text()))
        for sibling in minimum_req.next_siblings:
            if minimum_req.span.get_text() == "(Windows)":
                requirement_types = ["OS", "Memory", "Storage", "Processor", "Graphics", "Additional Notes"]
                # find next section with information
                if sibling.name == "div":
                    requirements = sibling.find_all('p')
                    reqs_data = {}
                    for i, type in enumerate(requirement_types):
                        reqs_data[type] = requirements[i].get_text()
                    game_data["system_requirements"] = reqs_data
                    break
            else:
                if sibling.name == "span":
                    requirements = sibling.find_all('p')
                    game_data["system_requirements"] = '\n'.join([e.get_text() for e in requirements])
    except AttributeError:
        print("No system req", url)
        game_data["system_requirements"] = None

    return json.dumps(game_data)


if __name__ == '__main__':
    headers = {
        'authority': 'www.freetogame.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'cookie': 'FREETOGAME=344f9ec8d51f2537cb7e1ce7da178e5b; _ga=GA1.2.417496318.1636891657; _gid=GA1.2.1707903118.1636891657; _gat_gtag_UA_161104669_1=1',
    }
    args = sys.argv
    print(get_game_data(args[1], headers))
