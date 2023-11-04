import subprocess
import json

# Define the ordered processes to search for
ordered_processes = [
    "IOMFB_bics_daemon",
    "distnoted",
    "notifyd"
]

def main():
    try:
        # Run the Pymobiledevice3 command to list processes on the iPhone and save it to a PSI file
        psi_filename = "iphone_processes.psi"
        command = ["Pymobiledevice3", "processes", "ps"]
        with open(psi_filename, "w") as psi_file:
            completed_process = subprocess.run(command, stdout=psi_file, text=True)

        # Check if the command was successful
        if completed_process.returncode == 0:
            # Read the PSI file and search for the specified ordered processes
            with open(psi_filename, "r") as psi_file:
                psi_content = psi_file.read()
                find_ordered_processes(psi_content, ordered_processes)
        else:
            print("Error running Pymobiledevice3.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def find_ordered_processes(psi_content, ordered_processes):
    import re
    clean_content = psi_content.encode("utf-8").decode("utf-8")
    found_processes = []
    for name in ordered_processes:
        pattern = re.compile(f"\"([0-9]+)\".*\n.*ProcessName.*({name})")
        matches = pattern.findall(clean_content)
        if len(matches) == 1:
            found_processes.append(matches[0]) #f"Process found: PID {matches[0][0]}, Process Name: {matches[0][1]}")

    if len(found_processes) == len(ordered_processes):
        print("Found all ordered processes.")
        ordered_found_processes = sorted(found_processes, key=lambda x: x[0])
        for process_info in found_processes:
            print(process_info)
    else:
        print("Could not find all ordered processes.")
        for pid, name in ordered_processes.items():
            if f'"{pid}":' not in psi_content or f'"{name}"' not in psi_content:
                print(f"Process not found: PID {pid}, Process Name: {name}")

if __name__ == "__main__":
    main()
