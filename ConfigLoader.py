import json


class ConfigLoader:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            config = json.load(f)
        self.mode = config['mode']
        self.dt_sec = 1 / float(config['FPS'])
        self.port_stage = f'{config["PORT-stage"]}'
        self.port_laser = f'{config["PORT-laser"]}'
        self.baudrate_laser = config["BAUDRATE-laser"]
