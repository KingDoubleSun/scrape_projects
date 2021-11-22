from bs4 import BeautifulSoup
import requests
import json


def get_data(urls):
    data = []
    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, features='html.parser')
        q_section = soup.find('div', {'id': 'interview_questions'})
        q_and_a = q_section.find('ol', {'class': 'float list-none'})
        q_and_a = q_and_a.find_all('li')
        for q in q_and_a:
            try:
                one_line = {'topic': url.split('/')[-2],
                            'question': q.find('h2').getText().strip(),
                            'answers': []}
            except AttributeError:
                print(f"not find question: {url}")
                continue
            for a in q.find_all('p'):
                answer = a.getText().strip()
                if len(answer) > 50:
                    one_line['answers'].append(answer)
            if not one_line['answers']:
                print(f'empty answer: {url}, {one_line["question"]}')
                continue
            data.append(one_line)
    return data


headers = {
    'authority': 'www.mockquestions.com',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'accept': '*/*',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'origin': 'https://www.mockquestions.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.mockquestions.com/companies/Tech/',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'cookie': '_ga=GA1.2.2113951643.1632888304; _gid=GA1.2.2129918003.1632888304; __gads=ID=3f00ddff9cf5c279-223669aafacb00dc:T=1632888304:RT=1632888304:S=ALNI_MY9DXiCGcfXCuLr87FXE2NHrF9ntQ; __stripe_mid=e457585d-5211-4184-afbe-2ca51539ebf9185749; email=yoyo.lu698%40gmail.com; id=962506; status=yes; PHPSESSID=h55uoj40q2gfp2bnsk3v8cvrsn; n=Amazon; c=Software%2BEngineer; t=Company; __stripe_sid=087d990e-1418-45f2-adcb-4203706c71b317b763; mi_question_databasedesignanalyst=1; catalog-category=Tech; catalog-division=Accounting%20Software',
}

data = {
  'page': 'companies',
  'url_directory_name': 'company',
  'category': 'Tech',
  'division': 'Data',
  'bb_color': 'bb-color-0892EB',
  'start_button': 'bg-4AADEE',
  'color': 'color-416AC0'
}


topic = 'careers'
# get all topics href
# r = requests.get(f'https://www.mockquestions.com/{topic}/')
# soup = BeautifulSoup(r.text, features='html.parser')
# industries = soup.find('div', {'class': "width20 mobile-width100 mt64 tlp-mt32 pp-mt16 pl-mt16 mb96 pp-mb60 pl-mb24 pr2per tlp-pr1per br-light-gray mobile-hide division-menu"}).find('ul')
# industry_urls = [i['href'] for i in industries.find_all('a', {'class': None})]
industry_urls = ['https://www.mockquestions.com/companies/Tech/']

for url in industry_urls:

    r = requests.post('https://www.mockquestions.com/process/directory/show_names.php', headers=headers, data=data)
    soup = BeautifulSoup(r.content, features='html.parser')
    topics = soup.find_all('a', {'class': 'inline-block b-gray black-bg-to-dark-hover br20 pt2 pr15 pb2 pl15 black-4D4D4D black-to-white roboto text14 tlp-text12 tll-text14 pp-text14 pl-text14 font700 lh32 cursor'})
    urls = [t['href'] for t in topics]
    # urls = ["https://www.mockquestions.com/position/Intern/"]
    industry = url.split('/')[-2]
    with open(f'{industry}.json', 'w') as f:
        json.dump(get_data(urls), f)
