import pandas as pd
from gemini_summarize import *
import time
import json

#print(df.transpose())
#rows = table_data.strip().split('\n')
#cleaned_data = '\n'.join([row for row in rows if row != '|---|---|---|---|---|---|---|---|---|---|---|---|'])

# Create a StringIO object and read into a DataFrame
#data_buffer = io.StringIO(cleaned_data)
#df = pd.read_csv(data_buffer, sep="|", header=0)

def convert_lists_to_strings(data):

  for key, value in data.items():
    if isinstance(value, list):
      data[key] = ', '.join(value)
  return data


def main():

    filepath = "C:\\Users\\ongye\\Downloads\\cyber news\\CSP\\"
    file = "azure cyber incident or cyber attack"

    df_input = pd.read_excel(filepath + file + ".xlsx")
    count = 1

    df_list = []

    for index, row in df_input.iterrows():

        print("#" + str(count))
        print(row["url"])


        try:

            jsonString = gemini_data_collection(row["url"])

            print(jsonString)

            try:

                jsonString_format = jsonString.replace("```json","").replace("```","").replace("\n","").replace("{  ","{\n").replace("}", "\n}")

                modified_data = convert_lists_to_strings(json.loads(jsonString_format))

                df = pd.DataFrame.from_dict(modified_data, orient="index")

            except json.decoder.JSONDecodeError:

                jsonString={
                    "affected country": "NIL",
                    "affected organization": "NIL",
                    "affected industry": "NIL",
                    "attack type": "NIL",
                    "attacker": "NIL",
                    "attacker country": "NIL",
                    "attacker type": "NIL",
                    "attacker motivation": "NIL",
                    "impact of the cyber incident": "NIL",
                    "lesson learn": "NIL",
                    "mitigation": "NIL"
                }

                df = pd.DataFrame.from_dict(jsonString, orient="index")

        except requests.exceptions.ConnectionError:

            jsonString = {
                "affected country": "NIL",
                "affected organization": "NIL",
                "affected industry": "NIL",
                "attack type": "NIL",
                "attacker": "NIL",
                "attacker country": "NIL",
                "attacker type": "NIL",
                "attacker motivation": "NIL",
                "impact of the cyber incident": "NIL",
                "lesson learn": "NIL",
                "mitigation": "NIL"
            }

            df = pd.DataFrame.from_dict(jsonString, orient="index")

        df_processed = df.transpose()

        df_processed["url"] = [row["url"]]

        df_list.append(df_processed)

        time.sleep(15)

        count+=1

    df_concat = pd.concat(df_list)

    merged_df = pd.merge(df_input, df_concat , on='url', how='left')

    merged_df.to_excel(filepath + file + " genai.xlsx" , index=False)


if __name__ == "__main__":
    main()