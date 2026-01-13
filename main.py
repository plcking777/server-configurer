import subprocess
import sys
import re
import yaml


if len(sys.argv) != 3:
    raise Exception("Expected 2 arguments")

# Arg 1: ssh template
ssh_template = sys.argv[1]
print(ssh_template)

# Arg 2: YML file
yml_file = sys.argv[2]
print(yml_file)


config_file = open(yml_file, "r")
data = yaml.load(config_file, Loader=yaml.FullLoader)


print(data)


for user in data["users"]:
    ssh_result = ssh_template.format(user=user)
    result = subprocess.run(["ssh", "-T", ssh_result, "echo test"], capture_output=True, text=True)
    print("res: ", result)