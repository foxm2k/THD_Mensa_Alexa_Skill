from src.lambda_package.filter_data import FilterData


class TestFilterJson:

    def test_hauptgericht(self):
        fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz="vegan", attributes=None, use_relative_path=False)
        print(fj.get_response())

    def test_suppe(self):
        fj = FilterData(warengruppe="suppe", dt="2019-11-20", kennz=None, attributes=None, use_relative_path=False)
        print(fj.get_response())

    def test_beilagen(self):
        fj = FilterData(warengruppe="beilagen", dt="2019-11-20", kennz=None, attributes=None, use_relative_path=False)
        print(fj.get_response())

    def test_vorlieben(self):

        vorlieben = ["vegetarisch", "vegan"]

        for v in vorlieben:
            fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz=v, attributes=None, use_relative_path=False)
            print(fj.get_response())

    def test_allergien(self):

        allergien = ["Milchprodukte", "Nüsse", "Fisch", "Eier", "Gluten"]

        for a in allergien:
            fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz=None, attributes=a, use_relative_path=False)
            print(fj.get_response())

        fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz=None, attributes="test", use_relative_path=False)
        print(fj.get_response())

        fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz=None, attributes=[1, 2], use_relative_path=False)
        print(fj.get_response())

    def test_add_vegan_when_vegetarisch(self):
        fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz="vegetarisch", attributes=None, use_relative_path=False)
        print(fj.get_response())

    def test_convert_ja_to_vegetarisch(self):
        fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz="ja", attributes=None, use_relative_path=False)
        print(fj.get_response())

        fj = FilterData(warengruppe="hauptgericht", dt="2019-11-20", kennz=["ja", "vegan"], attributes=None, use_relative_path=False)
        print(fj.get_response())

# Uncomment
t = TestFilterJson()
# t.test_general()
# t.test_suppe()
# t.test_beilagen()

# t.test_vorlieben()
# t.test_allergien()
t.test_add_vegan_when_vegetarisch()
# t.test_convert_ja_to_vegetarisch()
