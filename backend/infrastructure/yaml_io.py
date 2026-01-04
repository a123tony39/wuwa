import yaml

def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def write_yaml(filename, ctx):
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(ctx, f, allow_unicode=True)