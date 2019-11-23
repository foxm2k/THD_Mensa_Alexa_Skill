import requests
import pandas as pd
from src.mensa_data_to_json.conversion import Conversion

# Pandas setting to display more columns
pd.set_option('display.max_columns', 20)


class MensaDataToJson:

    def __init__(self, calendar_week):

        if calendar_week < 1 or calendar_week > 53 or type(calendar_week) is not int:
            raise ValueError("Impossible calendar week.")

        self.data = requests.get("https://www.stwno.de/infomax/daten-extern/csv/HS-DEG/"
                                 + calendar_week
                                 + ".csv?t=1572510478").text

    def clean_up(self):
        """
        Removed "Selbstbedienung" from substring. Problems throught "\n" in string.

        Before:

        06.11.2019;We;HG4;// Selbstbedienung //

        Bio-Spaghetti Bolognese (A,AA,F);S,BL;3,30 / 4,30 / 4,80;3,30;4,30;4,80

        After:

        06.11.2019;We;HG4;Bio-Spaghetti Bolognese (A,AA,F);S,BL;3,30 / 4,30 / 4,80;3,30;4,30;4,80
        """

        data = self.data.split(";")
        for i in range(len(data)):

            # Remove part of string until last index of the occurrence of "//". Remove whitespaces.

            if "//" in data[i]:
                index_of_last = data[i].rfind("/")
                index_of_backslash = data[i].find('\n', index_of_last)

                data[i] = data[i][index_of_backslash:]
                data[i] = data[i].strip()

        # TODO Drop last row (currently done in DF)

        # Rebuild csv-string
        data_str = ""
        for i in range(len(data)):
            if i == len(data):
                continue
            data_str += (data[i] + ";")

        return data_str

    def remove_g(self, entry):
        # Example: "Salatmix Krautsalat buntG RadischensalatGThousand Island Dressing Essig-Öl Dressing mediteranG"
        # Check if "G" is in entry at all
        if "G" in entry:
            # Count entries of "G"
            g_count = entry.count("G")
            # Loop through all entries of "G"
            for i in range(g_count):
                # Find next index of "G"
                g_index = entry.find("G")
                if g_index != 0:
                    # If "G" is at the end ("mediteranG")
                    if g_index == len(entry) - 1:
                        entry = entry[:len(entry) - 1]

                    # Make sure "G" is not at the start of a new word (char at g_index - 1 is not a whitespace)
                    # or a "-" (for instance: "Kartoffel-Gemüsepuffer mit Tzaziki")

                    # If "G" is at the end of a word ("buntG")
                    elif entry[g_index - 1] != " " and entry[g_index - 1] != "-" and entry[g_index + 1] == " ":
                        entry = entry[:g_index] + entry[g_index + 1:]
                    # If "G" is between two words ("RadischensalatGThousand")
                    elif entry[g_index - 1] != " " and entry[g_index - 1] != "-" and entry[g_index + 1] != " ":
                        entry = entry[:g_index] + entry[g_index + 1:]
                        entry = entry[:g_index] + " " + entry[g_index:]
            return entry
        return entry

    def run(self):

        data = self.clean_up()

        # Create dataframe and name columns
        df = pd.DataFrame([x.split(';') for x in data.split('\n')])
        df = df.rename(columns=df.iloc[0])

        # Rename
        df = df.rename(columns={'gast\r': 'gast'})
        # Drop last row (no values in csv)
        df.drop(df.tail(1).index, inplace=True)
        # Drop first row (has column names in it)
        df = df.iloc[1:]
        # Drop "preis" column (format: 0,70 / 0,90 / 1,40) since we already have: "0,70;0,90;1,40" (csv-ready)
        df = df.drop(['preis'], axis=1)
        # Remove \r from "gast" column
        df['gast'] = df[['gast']].replace(r'\s+|\\r', '', regex=True)

        """
        Comma to dot (String to float)
        
        Before: 4,40 (type: str)
        After: 4.40 (type: float)
        """

        # stud', 'bed']] = df[['stud', 'bed']].str.replace(',', '.').astype('float') # Not working but nice
        df['stud'] = df['stud'].str.replace(',', '.').astype('float')  # Working
        df['bed'] = df['bed'].str.replace(',', '.').astype('float')
        df['gast'] = df['gast'].str.replace(',', '.').astype('float')

        #
        """
        Extract attributes from name-string and clean up names.
        
        Before: ['name'] = Salat Buffet (1,3,6,9,16,C,G,J,L)
        After: ['name'] = Salat Buffet; ['attribute'] = [1,3,6,9,16,C,G,J,L] (type: list)
        """

        # Extract
        df['attributes'] = df['name'].str.extract(r"\(([^)]+)\)")
        # To list
        df['attributes'] = df['attributes'].str.split(",")
        # Remove attributes from name
        df['name'] = df['name'].replace(r"\(([^)]+)\)", '', regex=True)
        # Remove whitespaces (left and right)
        df['name'] = df['name'].str.strip()

        """
        Remove "- vegan" from ['name']
        
        Before: Ananasjoghurt - vegan
        After: Ananasjoghurt
        """
        df['name'] = df['name'].str.replace(" - vegan", "").str.strip()

        """
        Remove "G" from ['name']
        
        Before: "Salatmix Krautsalat buntG RadischensalatGThousand Island Dressing Essig-Öl Dressing mediteranG"
        After: "Salatmix Krautsalat bunt Radischensalat Thousand Island Dressing Essig-Öl Dressing mediteran"
        """

        df['name'] = df['name'].apply(self.remove_g)

        """
        Kennz-mensa_data_to_json, Attribute-mensa_data_to_json

        Before: "S,BL"
        After: ["Schwein", "Bioland"] (type: list)
        """

        # Remove NaNs
        df[['attributes', 'kennz']] = df[['attributes', 'kennz']].fillna(value=0)

        # Init Conversion
        conv = Conversion()

        # Kennz-mensa_data_to_json
        df['kennz_list'] = df['kennz'].str.split(",")

        def kennz_conv(entry):
            # Special case when entry is NaN
            if type(entry) is int:
                return []
            conv_ls = []
            for i in entry:
                conv_ls.append(conv.get_kennz(i))
            return list(set(conv_ls))

        df['kennz_conv_list'] = df['kennz_list'].apply(kennz_conv)

        # Attributes-mensa_data_to_json

        def att_conv(entry):
            # Special case when entry is NaN
            if type(entry) is int:
                return []
            conv_ls = []
            for i in entry:
                conv_ls.append(conv.get_att(i))
            return list(set(conv_ls))

        df['attributes_conv'] = df['attributes'].apply(att_conv)

        # Dataframe to json
        # df_json = df.to_json(orient='records', force_ascii=False)  # force_ascii=False because of Umlaute
        df.to_json("data.json", orient='records', force_ascii=False)  # force_ascii=False because of Umlaute
        # print(df_json)
        # df.to_csv("test.csv", encoding='utf-8', sep=";")
