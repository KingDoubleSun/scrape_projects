import json
from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import time

headers = {
    'authority': 'www.tripadvisor.com.au',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'cookie': 'TADCID=3_NZzEbfWMEcH0RsABQCFdpBzzOuRA-9xvCxaMyI12ifY9OTrr1S3tsEpX4oYwk0H4i_ZrhxaIGzuxcycoeL8oo6Qx26R3QSnkk; TAUnique=%1%enc%3AXjs2vdhoE5s4tT%2Bu6k4dMCd%2Fz2CURR1H0QVOCZ0PKEoLxcDgmfvj1g%3D%3D; TASSK=enc%3AAC5Sq3%2Bk%2FjFPP%2Bk90fsm1XFLwQFWMJyjyAzotwr2MzXHX1vFzB%2Fni7DR3GCt5KZX50m9zOtUtg172PM1MyC%2BENkpL0VsI5eowy9ab1vZg5LzKlIuskAnBpg7y23cSqAklQ%3D%3D; ServerPool=C; PMC=V2*MS.96*MD.20211005*LD.20211005; TART=%1%enc%3AOLU%2FrupOHTATvQTacb%2F9u1qyguW3balX8Jyt8eldSQfLZPXiyzoIgkqJYEgrJQBfYQn%2BfO4ma1E%3D; TATravelInfo=V2*AY.2021*AM.11*AD.30*DY.2021*DM.12*DD.1*A.2*MG.-1*HP.2*FL.3*DSM.1633406806646*RS.1; TASID=C1089C54481E4628A89989DBA982202D; TAReturnTo=%1%%2FHotels-g255100-Melbourne_Victoria-Hotels.html; ak_bmsc=3F416E7A4F7C634A900F2374653E575D~000000000000000000000000000000~YAAQX65NaPsOqKJ7AQAAavKhTg08ygDovEPDPPGWwTqMIpSqdF5DuDo++1VIojoL+O5n0IxP1oEuX4rDVmQQGwReyQ9iYpslmVTZyVGuwK9i2SjBfov3yJj//k7LUKHmI+M2oz7QVQaT1xRsyXCMfK/2+biRwG4CKHGscUebwL45p/rlXdFSwcAChoOC8X0co2F+s/aoK0IhgT6xp2xDzAN11UdYp/paApspPh1Pag43K/KlUj5z16/LDcoz03wKLA2JIfdtCbsYlcoqJcovg3VCkCSGQGIm/n/Qz1AAScqe8RlweXxgP+S75E5Zemh/i5aKmaro7AVlobwThZs1DbSP92ntfGlUD/c/W7o6wxjaOxpyU5G583fwVjw9kZEzw+amCGW1EdQ0GOHnaEL87f8mJ98=; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; PAC=ABngYo3aY8qv7ZCmDFMqZZt-_sCxQyV7MGHecIwlsoulAYOuValVCWV0cINWSrIJeeVg9Ya1CPFDksw2LILn7pWuX7WRSe8epg3gRyilfS4QiU6JLAKN1oByP0QhoBr65Y9rcUI22p_mvwm6PgK_NJiOBpaCv20-lEwqWt8V_KkAnXrEcfYIP-jTj5ouZsP71A%3D%3D; _hjid=3e69d832-9468-4dd9-b3cf-a96638f08e82; _hjFirstSeen=1; _hjAbsoluteSessionInProgress=0; __vt=l9AX4SDHJOHhiBUYABQCIf6-ytF7QiW7ovfhqc-AvRh9CicT0gI1SMg1Pd-_i33gUchNe_FdC-6UpzmpTz5DMgfwIKTv3-Bduq7rsuQrq3g9imkaASU879ASAeNM5y4dxgg5jSfEpFbMV_Dd0pfa5m4NVw; _hjIncludedInPageviewSample=1; _hjIncludedInSessionSample=0; __gads=ID=3fab8b9e62658524:T=1633407230:S=ALNI_MZ1iF2-QO_pAWnBPhK96vdpePlZ9w; roybatty=TNI1625!AIWb7CZ5bKveovNcOZGT2bdKdCuRFZByrLJ53%2BHHaYKNjFfBtYTJKQPAOQdm2IbbWpRmY8k4iyY%2BUIWGR9De7tW9nItAxNv7oU2HRjonnpYsdPA6aVhVUdWrK1lHYT2tB%2FZk8ZIVoaFrnRbX5iGJbrvzVlszdaDFkS0cp84ItAO2%2C1; SRT=%1%enc%3AOLU%2FrupOHTATvQTacb%2F9u1qyguW3balX8Jyt8eldSQfLZPXiyzoIgkqJYEgrJQBfYQn%2BfO4ma1E%3D; TASession=V2ID.C1089C54481E4628A89989DBA982202D*SQ.12*LS.DemandLoadAjax*GR.63*TCPAR.54*TBR.33*EXEX.81*ABTR.41*PHTB.44*FS.32*CPU.69*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.255100*EAU._; TAUD=LA-1633406810748-1*RDD-1-2021_10_05*HDD-423646-2021_11_30.2021_12_01.1*LD-434032-2021.11.30.2021.12.1*LG-434034-2.1.F.; bm_sv=FCEEE671C272B52566506720F5D37236~WvYvq7sP3MzjKtLWgvkZfu2gE2ltEY39ouagl2cA4OnJf3xSt02VazNbf13Cg20ojdAW2X1MMLdnAAg+vuIlme+GvA3GUIrFBXgrGtNOJlC0HLFdSYP/cqYfR5Gi3dW61bGa8u6wTn1+sXFEBoI666OLkoi0UXSPR6QILl4EZEk=',
}


def get_all_hotel_url(soup):
    main_list = soup.find('div', {'id': 'taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0'})
    return ["https://www.tripadvisor.com.au/" + a['href'] for a in
            main_list.find_all('a', {'class': 'property_title prominent'})]


def get_next_page_url(soup):
    next_page_url = soup \
        .find('div', {'id': 'taplc_main_pagination_bar_hotels_less_links_v2_0'}) \
        .find('a', {'class': 'nav next ui_button primary'})
    if not next_page_url:
        return False
    return next_page_url['href']


def get_text(component):
    try:
        return component.get_text()
    except:
        return None


def get_hotel_information(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features='html.parser')

    data = {}
    # name and address
    header = soup.find('div', {'class': 'react-container', 'id': 'component_4'})
    # name
    hotel_name = header.find('h1', {'class': 'fkWsC b d Pn', 'id': 'HEADING'})
    data['name'] = get_text(hotel_name)
    # address
    hotel_address = header.find('span', {'class': 'ceIOZ yYjkv'})
    data['address'] = get_text(hotel_address)
    # price
    main = soup.find('div', {'class': 'react-container', 'id': 'component_5'})
    price = main.find('div', {'class': 'vyNCd b Wi'})
    data['price'] = get_text(price)
    if not get_text(price):
        price = main.find('div', {'data-sizegroup': "hr_chevron_prices"})
        data['price'] = get_text(price)

    if data['price'] is not None:
        data['price'] = int(data['price'].split('$')[-1])

    # # rate and property amenities
    # rate
    about = soup.find('div', {'class': 'react-container', 'id': 'component_13'})

    try:
        rate = about.find('div', {'class': 'bSlOX Xe f P'})
        rate_score = float(get_text(rate.find('span', {'class': 'bvcwU P'})))
        rate_number = int(''.join(get_text(rate.find('span', {'class': 'btQSs q Wi z Wc'})).split()[0].split(',')))
        scores = about.find_all('div', {'class': 'cmZRz f'})
        scores.append(about.find('div', {'class': 'cmZRz f dfnfs'}))
        score_list = [{'name': get_text(div), 'score': int(div.find('span')['class'][1].split('_')[-1])} for div in scores]
    except:
        rate_score = None
        rate_number = None
        score_list = None
        print(f'no rate or scores {url}')
    data['rate'] = rate_score
    data['reviews'] = rate_number
    data['scores'] = score_list

    # features
    try:
        features = about \
            .find_all('div', {'class': 'ui_column'})[1] \
            .find_all('div', {'class': 'bUmsU f ME H3 _c'})
        data['features'] = [get_text(feature) for feature in features]
    except:
        print(f'no fearures {url}')
        data['features'] = None

    # language
    try:
        language = about.find_all('div', {'class': 'ui_column is-6'})
        if len(language) < 2:
            data['language'] = None
        else:
            language = language[1].find('div', {'class': 'ssr-init-26f'})
            language = json.loads(language['data-ssrev-handlers'])
            data['language'] = [tag['amenityNameLocalized'] for tag in language['load'][-1]['languageTags']]
    except:
        data['language'] = None
        print(f'No about {url}')

    data['url'] = url
    return data


if __name__ == '__main__':
    # get all hotel pages
    home_url = 'https://www.tripadvisor.com.au'
    next_page_url = '/Hotels-g255100-Melbourne_Victoria-Hotels.html'
    hotel_urls = []
    while next_page_url:
        response = requests.get(home_url + next_page_url, headers=headers)
        soup = BeautifulSoup(response.content, features='html.parser')
        hotel_urls += get_all_hotel_url(soup)
        next_page_url = get_next_page_url(soup)

    start = time.time()
    with Pool() as pool:
        result = pool.map(get_hotel_information, hotel_urls)
    end = time.time()

    with open('hotel_data.json', 'w') as result_file:
        json.dump(result, result_file)

    print(f'Used {end - start} s')
