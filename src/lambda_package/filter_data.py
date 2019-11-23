# import requests
import json
import os


class FilterData:

    def __init__(self, warengruppe, dt=None, kennz=None, attributes=None, use_relative_path=True):
        """

        Loads data and filters the data accordingly.

        :param warengruppe:
            Desired warengruppe. Default: "HG*"
        :param dt:
            Date
        :param kennz:
            Kennzeichnung like "vegetarier" or "veganer"
        :param attributes:
            Allergien like "Nüsse, Eier"
        """
        # self.json = requests.get('https://raw.githubusercontent.com/lucasfbn/repl/master/json_format.json').json()

        data_path = "data.json" if use_relative_path else os.path.dirname(__file__) + "\\data.json"

        with open(data_path) as f:
            self.data = json.load(f)
        self.response = None

        self.warengruppe = warengruppe
        self.dt = dt
        self.kennz = kennz
        self.attributes = attributes

        self.handle_none_case()
        self.correct_kennz()
        self.get()

    def handle_none_case(self):
        if type(self.kennz) == str and self.kennz == "None":
            self.kennz = None
        if type(self.attributes) == str and self.attributes == "None":
            self.attributes = None

    def correct_kennz(self):
        # Add vegan to the kennzeichnungen when user input was vegetarisch
        if type(self.kennz) is list and "vegetarisch" in self.kennz:
            self.kennz.append("vegan")
        elif type(self.kennz) == str and self.kennz == "vegetarisch":
            self.kennz = [self.kennz, "vegan"]
        # Convert "ja" to "vegetarisch"
        if type(self.kennz) == list and "ja" in self.kennz:
            self.kennz[self.kennz.index("ja")] = "vegetarisch"
        elif type(self.kennz) == str and self.kennz == "ja":
            self.kennz = "vegetarisch"

    def get_response(self):

        if len(self.response) == 0:
            return "Leider konnte ich kein passendes Gericht für dich finden. Ändere bitte " \
                   "deine Präferenzen oder wähle ein anderes Datum."
        if len(self.response) == 1:
            return "Folgendes Gericht entspricht deinen Präferenzen: " + self.response[0]['name'] + ". Guten Appetit!"

        base_str = "Folgende Gerichte entsprechen deinen Präferenzen: \n"
        for i in range(len(self.response)):
            if i == len(self.response) - 1:
                base_str += self.response[i]['name'] + ". Guten Appetit!"
                break

            base_str += self.response[i]['name'] + ", " + "\n"

        return base_str

    def get(self):

        def convert_alexa_date_reponse(alexa_date):
            """
            Converts an alexa given date to a format as it is represented in the data json.
            :param alexa_date:
                Date given by the alexa response
            :return:
                Correct format for data json
            """
            temp = alexa_date.split("-")
            temp.reverse()

            assert (len(temp) == 3), "Date seems incorrect: " + alexa_date
            return temp[0] + "." + temp[1] + "." + temp[2]

        # Error handling
        if self.warengruppe is None or self.warengruppe.lower() not in ["suppe", "hauptgericht", "beilagen",
                                                                        "nachspeisen"]:
            raise ValueError("Wrong Warengruppe specified.")

        if self.dt is not None and type(self.dt) is not str:
            raise ValueError("Wrong datatype for Datum.")

        if self.kennz is not None:
            if type(self.kennz) == list:
                self.kennz = [x.lower() for x in self.kennz]
            else:
                self.kennz = self.kennz.lower()
            accepted_kennz = ["vegetarisch", "vegan", "alles", "rind", "geflügel", "schwein",
                              "alkohol", "mensa vital", "vegan",
                              "bio-gericht", "bioland"]
            if (type(self.kennz) == list and not all(elem in accepted_kennz for elem in self.kennz) or
                type(self.kennz) == str and self.kennz not in accepted_kennz):
                raise ValueError("Wrong Kennzeichnung specified.")

        if self.attributes is not None:
            if type(self.attributes) == list:
                self.attributes = [x.lower() for x in self.attributes]
            else:
                self.attributes = self.attributes.lower()

            accepted_attributes = ["gluten", "eier", "fisch", "milchprodukte", "nüsse"]

            if (type(self.attributes) == list and not all(elem in accepted_attributes for elem in self.attributes) or
                type(self.attributes) == str and self.attributes not in accepted_attributes):
                raise ValueError("Wrong Attribute specified.")

        warengruppe = self.warengruppe.lower()

        if warengruppe == "suppe":
            warengruppe_searchterm = "suppe"
        elif warengruppe == "hauptgericht":
            warengruppe_searchterm = "H"
        elif warengruppe == "beilagen":
            warengruppe_searchterm = "B"
        elif warengruppe == "nachspeisen":
            warengruppe_searchterm = "N"
        else:
            raise ValueError("No match between warengruppe and searchterm.")

        warengruppe_filter = []
        for item in self.data:
            if item['warengruppe'].startswith(warengruppe_searchterm):
                warengruppe_filter.append(item)

        date_filter = []
        if self.dt is None:
            date_filter = warengruppe_filter
        else:
            dt = convert_alexa_date_reponse(self.dt)
            for item in warengruppe_filter:
                if item['datum'] == dt:
                    date_filter.append(item)

        kennz_filter = []
        if self.kennz is None:
            kennz_filter = date_filter
        else:
            for item in date_filter:
                for kennzeichnung in item['kennz_conv_list']:
                    if kennzeichnung.lower() in self.kennz:
                        kennz_filter.append(item)
        attributes_filter = []
        if self.attributes is None:
            attributes_filter = kennz_filter
        else:
            for item in kennz_filter:

                item['attributes_conv'] = filter(None, item['attributes_conv'])
                if not any(x.lower() in self.attributes for x in item['attributes_conv']):
                    attributes_filter.append(item)

        self.response = attributes_filter
