import subprocess
import os


process_name = "python_discord.py"

# Get the list of all processes
process_list = subprocess.check_output(["ps", "aux"])

# Search for the process with the given name
for line in process_list.splitlines():
    if process_name in str(line):
        # Extract the process ID from the line
        process_pid = str(int(line.split()[1]))
        # Kill the process with the given ID
        print(f"Running ... sudo ... kill {process_pid}")
        subprocess.run(["sudo", "kill", "-9", process_pid])
        print(f"Killed process {process_pid} ({process_name}).")

# runn the command
command = "/home/pi/kappabot/KappaBot/venv/bin/python3 python_discord.py &"
args = command.split(" ")

subprocess.Popen(args, cwd='/home/pi/kappabot/KappaBot')
# process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)





