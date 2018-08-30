import yaml


class YamlParser(object):
    def __init__(self):
        pass

    def parse(self, filepath):
        print("Parsing Yaml")
        with open(filepath, 'r') as fh:
            data = yaml.load(fh)
            cs = data["conferences"]
            sources = []
            for c, years in cs.items():
                print(c)
                print(years)
                for year, link in years.items():
                    name = c + str(year)
                    sources.append({
                        "name": name,
                        "link": link
                    })

        return sources
