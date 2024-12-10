import yaml

def load(filename: str) -> any:
    c = None
    with open(filename, 'rt') as fh:
        c = yaml.load(fh, yaml.SafeLoader)
    return c
