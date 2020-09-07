#!/usr/local/bin/python3.8

import urllib.request
import time, sys, os
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS


def silgeorae(api_url):
    """  pandas option  """
    value_list = [] * 100
    pd.set_option("display.max_rows", 1000)
    pd.set_option("display.max_columns", 1000)
    pd.set_option("display.width", 1000)

    """ variables """
    data = urllib.request.urlopen(api_url).read().decode("utf8")
    tree = ET.fromstring(data)
    item_list = tree.findall("body/items/item")
    dn = [
        "서초더샵포레",
        "서초포레스타2단지",
        "서초포레스타3단지",
        "서초포레스타5단지",
        "서초포레스타6단지",
        "서초포레스타7단지",
        "힐스테이트 서초 젠트리스",
        #"엘에이치서초4단지"
    ]
    cols = ["아파트명", "거래_날짜", "전용_면적", "층", "거래_금액"]

    for apt_list in item_list:
        if apt_list[4].text in dn:
            value = [
                apt_list[4].text,
                apt_list[2].text
                + "년"
                + apt_list[5].text
                + "월"
                + apt_list[6].text
                + "일",
                apt_list[7].text,
                apt_list[-1].text,
                apt_list[0].text,
            ]
            value_list.append(value)

    if len(value_list) == 0:
        print("거래가 없는 달입니다.")
    else:
        df = pd.DataFrame(value_list, columns=cols)
        df.sort_values(by="아파트명", ascending=True).style.set_properties(**{'width':'150px'})
        
        df.index = np.arange(1, len(df) + 1)

        print(df)
        html = df.to_html(justify="center")
        with open("silgeorae.html", "a", encoding="utf-8") as file:
            file.writelines('<meta charset="UTF-8">\n')
            file.write('')
            file.write(base_date)
            file.write(html)

if __name__ == "__main__":
    """ init """
    filename = "./silgeorae.html"
    if os.path.isfile(filename):
        os.remove(filename)

    url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
    serviceKey = "jlezFfeKU0KiWgXB2GtMxpSK6Rt%2F6oE1Ot4C5UMTjqDDOnCnbJ2oJEkxJ%2Fe2G6ZZPugcoEpS%2By9nTy3zefOZiw%3D%3D"
    base_date = "202008"
    gu_code = "11650"
    numrow = 1000
    for nal in range(1, int(time.strftime("%m")) + 1):
        base_date = time.strftime("%Y") + "0" + str(nal)
        print('BASE DATE: ', base_date)
        payload = (
            "LAWD_CD="
            + gu_code
            + "&"
            + "DEAL_YMD="
            + base_date
            + "&"
            + "serviceKey="
            + serviceKey
        )
        api_url = url + payload
        silgeorae(api_url)

