# import configparser
#
# config = configparser.ConfigParser()
#
# config.read('input.cfg')
# print({s:dict(config.items(s)) for s in config.sections()})


import yaml

with open("input.yaml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)
    print(data["MIXTURE"]["Type"])
