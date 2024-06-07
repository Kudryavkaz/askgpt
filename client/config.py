import yaml


class Config(object):
    def __init__(self, config_path):
        with open(config_path, "r") as file:
            data = yaml.safe_load(file)
        self.api_key = data['api_key']
        self.base_url = data['base_url']
        self.model = data['model']
        self.prompt = data['prompt']
        self.max_context_size = data['max_context_size']
