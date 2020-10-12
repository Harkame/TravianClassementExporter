from tce import TravianClassementExporter
import json


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    exporter = TravianClassementExporter()

    exporter.init_arguments()

    exporter.run()
