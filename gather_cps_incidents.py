from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
import time
import re
import datetime
import telebot
from get_date_of_article import *

def get_today():

    today = datetime.date.today()
    formatted_date = today.strftime("%d/%m/%Y")

    return formatted_date

#!!!! Remember to update GoogleNews module via Pip!!!!#

#topic_list = ["azure cyber incident or cyber attack", "amazon web services cyber incident or cyber attack", \
#"Google Cloud Platform cyber incident or cyber attack", "Oracle Cloud cyber incident or cyber attack", "Alibaba Cloud cyber incident or cyber attack", "IBM Cloud cyber incident or cyber attack"]

topic_list = ["azure cyber incident or cyber attack", "amazon web services cyber incident or cyber attack", \
"Google Cloud Platform cyber incident or cyber attack", "Oracle Cloud cyber incident or cyber attack", "Alibaba Cloud cyber incident or cyber attack", "IBM Cloud cyber incident or cyber attack"]



#year = "2024"

for topic in topic_list:

    #output_filepath = "C:\\Users\\ongye\\Downloads\\cyber news\\CSP\\" + str(topic) + "_" + str(year) + "_new.xlsx"

    output_filepath = "C:\\Users\\ongye\\Downloads\\cyber news\\CSP\\" + str(topic) + ".xlsx"

    print("search " + str(topic))

    start_date = "01/01/" + str(2014)

    print(str(start_date) + " to " + str(get_today()))

    news = GoogleNews(start=get_today(), end=get_today())
    news.search(topic)
    result = news.result()

    page1_df = pd.DataFrame.from_dict(result)

    page_df_list = []
    page_df_list.append(page1_df)

    time.sleep(5)

    for page in range(2, 11):
        print("processing page #" + str(page))

        page_result = news.page_at(page)
        page_df = pd.DataFrame.from_dict(page_result)
        page_df_list.append(page_df)

        time.sleep(2)

    appended_df = pd.concat(page_df_list)
    appended_df.drop(columns=["img"])

    df_dedup = appended_df.drop_duplicates('title', keep='first')

    link_list = []

    for index, row in df_dedup.iterrows():

        link_replaced = row["link"].replace("/url?esrc=s&q=&rct=j&sa=U&url=", "")

        replacement = re.findall("&ved=.*", link_replaced)[0]

        link_list.append(link_replaced.replace(replacement, ""))

    df_dedup["url"] = link_list

    df_drop = df_dedup.drop(['img', 'link'], axis=1)

    topic_lst = []

    for i in range(len(df_drop)):

        topic_lst.append(topic)

    df_drop["topic"] = topic_lst

    df_processed = get_date_of_article(df_drop)

    df = df_processed[~df_processed['article date'].str.contains("Error")]

    # Convert date column to datetime
    df['article date'] = pd.to_datetime(df['article date'], format='%d/%m/%Y')

    df.to_excel(output_filepath,  index=False)

    time.sleep(5)
