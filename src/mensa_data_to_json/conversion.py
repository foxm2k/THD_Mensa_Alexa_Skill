class Conversion:

    def __init__(self):
        self.kennz = Kennz()
        self.att = Attributes()

    def get_kennz(self, inp):
        return self.kennz.kennz_conv(inp)

    def get_att(self, inp):
        return self.att.att_conv(inp)


class Attributes:
    ATTRIBUTES_CONVERSION_TABLE = {
        ("AA", "AB", "AC", "AD", "AE", "AF"): "Gluten",
        "C": "Eier",
        "D": "Fisch",
        "G": "Milchprodukte",
        ("E", "HA", "HB", "HC", "HD", "HE", "HF", "HG", "HH", "HI"): "Nüsse"
    }

    def att_conv(self, inp):
        for key, val in self.ATTRIBUTES_CONVERSION_TABLE.items():
            if type(key) is tuple:
                for e in key:
                    if e == inp:
                        return val
            elif key == inp:
                return val
        return "UNDEFINIERT"


class Kennz:
    KENNZ_CONVERSION_TABLE = {
        "V": "Vegetarisch",
        "R": "Rind",
        "G": "Geflügel",
        "S": "Schwein",
        "L": "TBD",
        "A": "Alkohol",
        "MV": "Mensa Vital",
        "VG": "Vegan",
        "B": "Bio-Gericht",
        "J": "TBD",
        "BL": "Bioland"
    }

    def kennz_conv(self, inp):
        for key, val in self.KENNZ_CONVERSION_TABLE.items():
            if key == inp:
                return val
        return "UNDEFINIERT"

# Testing
# c = Conversion()
# print(c.get_kennz("B"))
# print(c.get_att("14"))
