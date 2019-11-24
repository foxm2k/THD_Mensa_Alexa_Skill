from src.mensa_data_to_json.main import MensaDataToJson


class TestMensaDataToJson:

    def test_run(self):
        t = MensaDataToJson(calendar_week=48)
        t.run()


t = TestMensaDataToJson()
t.test_run()
