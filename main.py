import subprocess
import sys
import re
import yaml
import time


if len(sys.argv) != 3:
    raise Exception("Expected 2 arguments")

# Arg 1: ssh template
ssh_template = sys.argv[1]

# Arg 2: YML file
yml_file = sys.argv[2]

config_file = open(yml_file, "r")
data = yaml.load(config_file, Loader=yaml.FullLoader)



for step in data["steps"]:
    step = list(step.values())[0]
    ssh_result = ssh_template.format(user=step["user"])
    
    print(ssh_result + ":")
    
    prev_result = None
    for action in step["actions"]:
        
        action_split = action.split(" ")
        action_type = action_split[0]
        action_value = " ".join(action_split[1:])

        if action_type == "cmd":
            result = subprocess.run(["ssh", ssh_result, action_value], stdout=subprocess.PIPE)
            
            print("    Running  ", action_value)
            
            prev_result = result.stdout.decode("utf-8")
        elif action_type == "expect":

            action_value = action_value[1:len(action_value) - 1]
            match = re.match(action_value, prev_result)
            if not match:
                raise Exception(f"\"{prev_result} did not match the regex: {action_value}")
        elif action_type == "pause":
            print("    Pausing for", action_value)
            time.sleep(int(action_value))