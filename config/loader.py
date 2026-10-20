import os
import yaml

def load_config():
    path=os.path.join(os.path.dirname(__file__),"env.yaml")
    with open(path,encoding="utf-8") as f:
        return yaml.safe_load(f)