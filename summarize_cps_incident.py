import pandas as pd
from gemini_summarize import *
import time
import json

def main():

    filepath = "C:\\Users\\ongye\\Downloads\\cyber news\\CSP\\"
    file = "azure cyber incident or cyber attack"

    df = pd.read_excel(filepath + file + ".xlsx")
    count = 1

    summary_list = []

    for index, row in df_input.iterrows():

        print("#" + str(count))
        print(row["url"])

        summary = gemini_summarize(row["url"])

        summary_list.append(summary)

        time.sleep(15)

        count += 1

    df["summary"] = summary_list

    df.to_excel(filepath + file + " genai.xlsx" , index=False)

if __name__ == "__main__":
    main()