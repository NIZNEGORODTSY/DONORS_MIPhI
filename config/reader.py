import yaml

CONFIG: dict[str, str | int] = {}

def read_config() -> None:
    global CONFIG
    with open('config.yaml', 'r') as config_file:
        CONFIG = yaml.safe_load(config_file)

def get_param_value(param_name: str) -> str | int:
    return CONFIG[param_name]

read_config()
print(get_param_value('dbhost'))
