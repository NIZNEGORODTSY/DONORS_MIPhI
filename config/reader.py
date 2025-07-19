
import yaml
from typing import Dict, Optional, Union

CONFIG: Dict[str, Optional[Union[str, int]]] = {}

def read_config() -> None:
    global CONFIG
    with open('config/config.yaml', 'r') as config_file:
        CONFIG = yaml.safe_load(config_file)

# Используем Union или Optional
def get_param_value(param_name: str) -> Union[str, int, None]:
    return CONFIG.get(param_name)  # .get() возвращает None, если ключа нет

read_config()
print(get_param_value('dbhost'))