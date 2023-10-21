import tkinter as tk
import paramiko
import threading
from tkinter import filedialog
import paramiko.util
import os
import logging
import configparser
from paramiko.ssh_exception import NoValidConnectionsError
import sys
from tkinter import scrolledtext
import tkinter as tk
from tkinter import ttk
import re

current_directory = os.getcwd()

# Create a Tkinter window
window = tk.Tk()
window.title("FETCHER")
ssh = None
ssh2 = None
stop_threads = False  # Flag to stop threads

window.geometry("1547x988")  # Csökkentsük az ablak magasságát


#def set_command1_from_dropdown():
#    selected_grep = grep_dropdown.get()
#    command1_var.set("     |" + selected_grep)

#command1_var = tk.StringVar()

def set_command1_from_dropdown():
    selected_grep = grep_dropdown.get()
    current_command1 = command1_var.get()
    
    # Ha a current_command1 nem üres, akkor adjunk hozzá egy "| grep" részt
    if current_command1:
        new_command1 = f"{current_command1} | grep {selected_grep}"
    else:
        new_command1 = f"grep {selected_grep}"
    
    command1_var.set(new_command1)

# Create a StringVar to store the current command 1
command1_var = tk.StringVar()

# Create a Label
label = tk.Label(window, text="Select a Grep Expression:")
label.grid(row=1, column=9)

# Create a list of grep expressions
grep_options = ["'DEBUG'", "'TRACE'", "'INFO'", "'WARN'", "'ERROR'", "'Excel'", "'Executing excel'" , "'with input'", "'log'", "'Event'", "'event-attribute'", "'Event handling for event'", "'Summary report of SetValues event'", "'Number of successfully found implementations:'definenumber'", "'Number of implementations with inconsistencies (ignored):'definenumber'", "'Number of implementations with error while updating:'definenumber'", "'fire event 'defineeventname'", "'fire event'", "'Export triggered by event'", "'Http request:'", ]


constant_text_widget = tk.Text(window, wrap=tk.WORD, width=79, height=10)
constant_text_widget.grid(row=11,column=6,columnspan=12)

constant_text_widget = tk.Text(window, wrap=tk.WORD, width=88, height=10)
constant_text_widget.grid(row=11, column=8,columnspan=10)

# Define a tag for the constant text widget
constant_text_widget.tag_configure("constant_text", font=("Arial", 12), foreground="black",background="yellow")

# Add the constant text to the constant_text_widget with the "constant_text" tag
constant_text = """You can use the predefined grep expressions to filter the log messages.:
But you can also add your own grep expression to the command.

For example: You enter the following command: alias, you select 'log' from the drop-down, it would append it like this | grep 'log' to the command.                      
the final result would be this alias | grep 'log' and it would filter.






"""
constant_text_widget.insert(tk.END, constant_text, "constant_text")


def add_custom_grep():
    custom_grep = custom_grep_entry.get()
    if custom_grep:
        # Append the custom grep expression to the list
        grep_options.append(f"'{custom_grep}'")
        # Update the dropdown values
        grep_dropdown["values"] = grep_options
        # Clear the custom grep entry
        custom_grep_entry.delete(0, tk.END)


# Create a Dropdown (Combobox) widget
grep_dropdown = ttk.Combobox(window, values=grep_options)
grep_dropdown.grid(row=0, column=9, ipadx=135)

# Create a Button to set the command 1 based on the selected grep expression
set_button = tk.Button(window, text="Add the grep to your command", command=set_command1_from_dropdown)
set_button.grid(row=0, column=1)


# Create an Entry widget to display and edit Command 1
command1_entry = tk.Entry(window, textvariable=command1_var, width=40)
set_button.grid(row=0, column=18)

label = tk.Label(window, text="Add your custom grep to the system!")
label.grid(row=4, column=8)
# Create an Entry widget for custom grep expressions
custom_grep_entry = tk.Entry(window,width=50)
custom_grep_entry.grid(row=5, column=8)

# Create a Button to add the custom grep expression to the list
add_custom_grep_button = tk.Button(window, text="Add Custom Grep", command=add_custom_grep)
add_custom_grep_button.grid(row=6, column=8)

def create_mysql_dump():
    global ssh, local_path, status_label
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
            hostname=ssh_host_var.get(),
            username=ssh_username_var.get(),
            key_filename=ssh_key_filename_var.get(),
            port=int(ssh_port_var.get())
    )
    first_step = stdin, stdout, stderr = ssh.exec_command("mysql")
    print(first_step)
    second_step = stdin, stdout, stderr = ssh.exec_command("show databases")
    print(second_step)
    #parts = alias_text.split('alias ')[1].split('-')

    #if len(parts) >= 2:
    #    stagename = parts[0].strip()
    #    print(stagename)
    #else:
    #    print("There is an issue with the alias command")
    #third_step_command = ""
    #third_step = stdin, stdout, stderr = ssh.exec_command("use omandev1a")
    #print(third_step)
    #fourth_step = stdin, stdout, stderr = ssh.exec_command("CREATE USER 'l2mysqltemp'@'localhost' IDENTIFIED BY 'YourPassword259)';")
    #print(fourth_step)
    #fifth_step = stdin, stdout, stderr = ssh.exec_command("GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'l2mysqltemp'@'localhost' WITH GRANT OPTION;")
    








def check_tomcat_java__deployer_version():
    global ssh, local_path, status_label
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
            hostname=ssh_host_var.get(),
            username=ssh_username_var.get(),
            key_filename=ssh_key_filename_var.get(),
            port=int(ssh_port_var.get())
    )   
    command = "alias | grep \"version\" | cut -d\"=\" -f2"  # Keresd meg a catalina.out fájlt
    stdin1, stdout1, stderr1 = ssh.exec_command(str(command))
    output = stdout1.read().decode('utf-8').strip()
    print(output)
    # A kimenet szétvágása soronként
    lines = output.splitlines()

# Egy üres lista inicializálása a végleges eredmények tárolására
    results = []

# Sorok feldolgozása
    for line in lines:
    # Az idézőjelek eltávolítása
        line_without_quotes = line.replace("'", "").strip()

    # A sor felosztása az egyenlőségjel mentén és a második rész hozzáadása a results listához
        parts = line_without_quotes.split("=")
    if len(parts) == 2:
        results.append(parts[1].strip())

# Eredmények kiírása
    for result in results:
        #print(result[0])
        first_version = str(result[0]).replace("'", " ")
        print(first_version)
        #print(result[1])
        second_version = result[1].strip()
        
        text1_without_quotes = first_version.replace("'", " ")
        #text2_without_quotes = results[1].replace("'", "")
        print(text1_without_quotes)
        text2_without_quotes = second_version.replace("'", " ")
        print(text2_without_quotes)
        command2 = text1_without_quotes
        command3 = text2_without_quotes
        stdin2, stdout2, stderr2 = ssh.exec_command(command2)
        output2 = stdout2.read().decode('utf-8').strip()
        print(output2)

    #print(text1_without_quotes)
    #print(text2_without_quotes)    
        # A kimenet tartalmazza az elérési útvonalat (ha megtalálható)
    #output = stdout1.read().decode('utf-8').strip()
    #print(output)
    #regex = r'^(\w+)-version'
    #matches = re.findall(regex, output, re.MULTILINE)
    #versions = []
    #for match in matches:
    #        versions.append(match)
    #        print(versions)
            
        
    #first_version = versions[0]
    #second_version = versions[1]
    #command1 = first_version
    #print(command1)
    #command2 = second_version
    #print(command2)
    #stdin2, stdout2, stderr2 = ssh.exec_command(str(first_version))
    #stdin2, stdout2, stderr2 = ssh.exec_command(str(second_version))
    #output1 = stdout2.read().decode('utf-8').strip()
    #output2 = stdout2.read().decode('utf-8').strip()
    #print(output1)
    #print(output2)
    #stdin3, stdout3, stderr3 = ssh.exec_command(str(command2))
    #output1 = stdout2.read().decode('utf-8').strip()
    #output2 = stdout3.read().decode('utf-8').strip()
    #print(str(output1))
    #print(str(output2))
    #return str(output1), str(output2)


    #except Exception as e:
    #    print(f"Error: {str(e)}")
        # A kimenet tartalmazza az elérési útvonalat (ha megtalálható)
          # Create an SFTP client
        

        # Download the remote catalina.out file
        

        # Close the SFTP and SSH connections
    
        

   
    #sftp = ssh.open_sftp()
    #sftp = ssh.open_sftp()
    #remote_path = just_fetch_catalina_out_path()

        # Download the remote catalina.out file
    #sftp.get(remote_path, local_path)

        # Close the SFTP and SSH connections
    #sftp.close()
    


add_custom_grep_button = tk.Button(window, text="Fetch /Deployer/Java/Tomcat version", command=check_tomcat_java__deployer_version)
add_custom_grep_button.grid(row=10, column=8)
# Function to add custom grep expressions to the list



# Create a Label
#label = tk.Label(window, text="Select a Grep Expression:")
#label.grid(row=0, column=15)

# Create a list of grep expressions
#grep_options = ["grep pattern1", "grep pattern2", "grep pattern3"]

# Create a Dropdown (Combobox) widget
#grep_dropdown = ttk.Combobox(window, values=grep_options)
#grep_dropdown.grid(row=0, column=16)

# Create a Button to set the selected grep expression to command1_var
#set_button = tk.Button(window, text="Set Command 1", command=set_command1_from_dropdown)
#set_button.grid(row=0, column=17)


# Define Tkinter variables to store user input
ssh_host_var = tk.StringVar()
ssh_username_var = tk.StringVar()
ssh_key_filename_var = tk.StringVar()
ssh_port_var = tk.StringVar()
command1_var = tk.StringVar()
command2_var = tk.StringVar()
local_path = current_directory + "/catalina.out"


# Define the global local_path variable
# Create a Tkinter window
# Készítsd el a Tkinter ablakot
#window = tk.Tk()
#window.title("Log Viewer")

# Hozz létre egy log handler-t, amely a log üzeneteket a Text widget-be küldi

# Hozz létre egy TextWidgetHandler példányt és add hozzá az app_logger-hez


# Most az app_logger.debug, app_logger.info, stb. hívások a Text widget-be is írják a log üzeneteket


# Run the Tkinter main loop


# Create Tkinter variables to store user input
ssh_host_var = tk.StringVar()
ssh_username_var = tk.StringVar()
ssh_key_filename_var = tk.StringVar()
ssh_port_var = tk.StringVar()

# Create a function to save settings
def save_settings():
    config = configparser.ConfigParser()
    config['SSH'] = {
        'host': ssh_host_var.get(),
        'username': ssh_username_var.get(),
        'key_filename': ssh_key_filename_var.get(),
        'port': ssh_port_var.get(),
        'command1': command1_entry.get(),
        'command2': command2_entry.get(),
        'log_file1': log_file1_entry.get(),
        'log_file2': log_file2_entry.get()
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Create a function to load settings
def load_settings():
    config = configparser.ConfigParser()
    config.read('config.ini')
    ssh_settings = config['SSH']
    ssh_host_var.set(ssh_settings.get('host', ''))
    ssh_username_var.set(ssh_settings.get('username', ''))
    ssh_key_filename_var.set(ssh_settings.get('key_filename', ''))
    ssh_port_var.set(ssh_settings.get('port', ''))
    command1_var.set(ssh_settings.get('command1', ''))
    command2_var.set(ssh_settings.get('command2', ''))
    log_file1_entry.delete(0, tk.END)
    log_file1_entry.insert(0, ssh_settings.get('log_file1', ''))
    log_file2_entry.delete(0, tk.END)
    log_file2_entry.insert(0, ssh_settings.get('log_file2', ''))


debug_button = ""
# Modify the download_catalina_out function to use global variables

# Create a Text widget to display the output
text_widget = tk.Text(window, wrap=tk.WORD, width=80, height=20)
text_widget.grid(row=10, columnspan=3)
    # Rest of the function remains the same


#def toggle_debug_mode2():
#    if paramiko.util.log_to_file:
#        paramiko.util.log_to_file = False
#        debug_button.config(text="Enable Debug")
#        print("Debug mode disabled")
#        # Set the logging level to WARNING to disable debugging
#        warning = logging.getLogger("paramiko").setLevel(logging.WARNING)
#        print(warning)
#    else:
#        paramiko.util.log_to_file = True
#        debug_button.config(text="Disable Debug")
#        print("Debug mode enabled")
#        # Set the logging level to DEBUG to enable debugging
#        # Konfiguráld a logger-t
#        logging.basicConfig(filename='paramiko_debug.log', level=logging.INFO)
#
#        # Ha ki szeretnéd írni a log üzeneteket a konzolra is, hozz létre egy konzol loggert
#        console = logging.StreamHandler()
#        console.setLevel(logging.INFO)  # Állítsd be az általad kívánt logszintre
#        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#        console.setFormatter(formatter)
#        app_logger.addHandler(console)
#        text_widget_handler = TextWidgetHandler(log_widget)
#        app_logger.addHandler(text_widget_handler)  # Add hozzá a console loggert az app_logger-hez
#        text_widget.insert(tk.END, "Debug mode enabled\n")
#        text_widget.insert(tk.END, app_logger)
#        text_widget.see(tk.END)
        # Hibaüzenetek logolása
# why is the exctype not defined?
#how can i log every error message? to my text_widget?

        
#def log_errors(exctype, value, tb):
#    error_message = f"Exception: {value}\n"
#    text_widget.insert(tk.END, error_message)
#    text_widget.see(tk.END)

# Set the custom exception handler
#sys.excepthook = log_errors

#def toggle_debug_mode():
#    if paramiko.util.log_to_file:
#        paramiko.util.log_to_file = False
#        debug_button.config(text="Enable Debug")
#        print("Debug mode disabled")
#        # Set the logging level to WARNING to disable debugging
#        warning = logging.getLogger("paramiko").setLevel(logging.WARNING)
#        print(warning)
#    else:
#        paramiko.util.log_to_file = True
#        debug_button.config(text="Disable Debug")
#        print("Debug mode enabled")
#        # Set the logging level to DEBUG to enable debugging
#        # Konfiguráld a logger-t
#        logging.basicConfig(filename='paramiko_debug.log', level=logging.INFO)

#        # Ha ki szeretnéd írni a log üzeneteket a konzolra is, hozz létre egy konzol loggert
#        console = logging.StreamHandler()
#        console.setLevel(logging.INFO)  # Állítsd be az általad kívánt logszintre
#        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#        console.setFormatter(formatter)
#        app_logger.addHandler(console)  # Add hozzá a console loggert az app_logger-hez

#        text_widget.insert(tk.END, "Debug mode enabled\n")
#        text_widget.see(tk.END)
#        #text_widget.insert(tk.END, log_errors)
#        text_widget.see(tk.END)




#debug_button = tk.Button(window, text="Toggle Debug", command=toggle_debug_mode2)
#debug_button.grid(row=9, columnspan=2)
   

def browse_log_file1():
    log_file1_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")])
    log_file1_entry.delete(0, tk.END)  # Törölje az előző értéket az Entry-ből
    log_file1_entry.insert(0, log_file1_path)  # Állítsa be az új fájl elérési útvonalát

def browse_log_file2():
    log_file2_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")])
    log_file2_entry.delete(0, tk.END)  # Törölje az előző értéket az Entry-ből
    log_file2_entry.insert(0, log_file2_path)  # Állítsa be az új fájl elérési útvonalát

def browse_private_key():
    file_path = filedialog.askopenfilename()
    ssh_key_filename_var.set(file_path)

# Create and arrange GUI elements for SSH connection parameters and commands
ssh_host_label = tk.Label(window, text="SSH Host:")
ssh_host_label.grid(row=0, column=0, sticky='w')
ssh_host_entry = tk.Entry(window, textvariable=ssh_host_var, width=40)
ssh_host_entry.grid(row=0, column=1)

ssh_username_label = tk.Label(window, text="Username:")
ssh_username_label.grid(row=1, column=0, sticky='w')
ssh_username_entry = tk.Entry(window, textvariable=ssh_username_var, width=40)
ssh_username_entry.grid(row=1, column=1)

ssh_key_filename_label = tk.Label(window, text="Private Key Location:")
ssh_key_filename_label.grid(row=2, column=0, sticky='w')
ssh_key_filename_entry = tk.Entry(window, textvariable=ssh_key_filename_var,width=40)
ssh_key_filename_entry.grid(row=2, column=1)

browse_button = tk.Button(window, text="Browse Private Key", command=browse_private_key)
browse_button.grid(row=2, column=2)

load_settings_button = tk.Button(window, text="Load Settings", command=load_settings)
load_settings_button.grid(row=0, column=2)

save_settings_button = tk.Button(window, text="Save Settings", command=save_settings)
save_settings_button.grid(row=1, column=2)


status_label = tk.Label(window, text="", fg="red")  # A text és a szín módosítható
status_label.grid(row=12, columnspan=3)  # Sor és oszlop beállítása a megjelenítéshez



def check_ssh_connection():
    global ssh, status_label, local_path
    try:
        command = "hostname"  # Keresd meg a catalina.out fájlt
        stdin, stdout, stderr = ssh.exec_command("hostname")

        # A kimenet tartalmazza az elérési útvonalat (ha megtalálható)
        hostname = stdout.read().decode('utf-8').strip()
        print(hostname)
        
        # Ha az SSH kapcsolat létrejött, akkor connected
        status_label.config(text="You are connected to " + hostname, fg="green")
        ssh.close()
    except Exception as e:
        # Ha bármilyen hiba történik, akkor not connected
        status_label.config(text="Not connected", fg="red")
        print(f"SSH Connection Error: {str(e)}")





check_ssh_connection()

# Define the global local_path variable
local_path = ""

# Function to update the local_path variable
def update_local_path():
    global local_path
    local_path = current_directory + "/catalina.out"

# Call the function to initialize local_path
update_local_path()

# Modify the download_catalina_out function to use parameters
def download_catalina_out(ssh_host, ssh_username, ssh_key_filename, ssh_port, remote_path):
    global ssh, local_path, status_label
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        ssh.connect(
            hostname=ssh_host,
            username=ssh_username,
            key_filename=ssh_key_filename,
            port=int(ssh_port)
        )

        # Create an SFTP client
        sftp = ssh.open_sftp()

        # Download the remote catalina.out file
        sftp.get(remote_path, local_path)

        # Close the SFTP and SSH connections
        sftp.close()
        ssh.close()

        # Inform the user about the successful download
        status_label.config(text=f"catalina.out downloaded: {local_path}", fg="green")

    except Exception as e:
        # Handle any exceptions that may occur during the process
        status_label.config(text=f"Error: {str(e)}", fg="red")


def just_fetch_catalina_out_path():
    global ssh, status_label, local_path
    try:
        command = "find / -name catalina.out 2>/dev/null | head -n 1"  # Keresd meg a catalina.out fájlt
        stdin, stdout, stderr = ssh.exec_command("find / -name catalina.out 2>/dev/null | head -n 1")

        # A kimenet tartalmazza az elérési útvonalat (ha megtalálható)
          # Create an SFTP client
        

        # Download the remote catalina.out file
        

        # Close the SFTP and SSH connections
    
        

        remote_path = stdout.read().decode('utf-8').strip()
        print(remote_path)
          # Create an SFTP client
        return remote_path

    except Exception as e:
        print(f"Error: {str(e)}")



def new_download_link():
    global ssh, local_path, status_label
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
            hostname=ssh_host_var.get(),
            username=ssh_username_var.get(),
            key_filename=ssh_key_filename_var.get(),
            port=int(ssh_port_var.get())
    )
    
    #sftp = ssh.open_sftp()
    sftp = ssh.open_sftp()
    remote_path = just_fetch_catalina_out_path()

        # Download the remote catalina.out file
    sftp.get(remote_path, local_path)

        # Close the SFTP and SSH connections
    sftp.close()
    ssh.close()






def get_catalina_out_path():
    global ssh, status_label, local_path
    try:
        command = "find / -name catalina.out 2>/dev/null | head -n 1"  # Keresd meg a catalina.out fájlt
        remote_path = stdin, stdout, stderr = ssh.exec_command(str(command))
        
        #remote_path= just_fetch_catalina_out_path()

        # A kimenet tartalmazza az elérési útvonalat (ha megtalálható)
        remote_path = stdout.read().decode('utf-8').strip()
        print(str(remote_path))
        
        download_catalina_out(
        ssh_host_var.get(),
        ssh_username_var.get(),
        ssh_key_filename_var.get(),
        ssh_port_var.get(),
        str(remote_path),
        )
        
            
        
        #if remote_path:
        #    download_catalina_out(
        #
        #        ssh_host_var.get(),
        #        ssh_username_var.get(),
        #        ssh_key_filename_var.get(),
        #        ssh_port_var.get(),
        #        local_path
        #    )
        #    print(f"catalina.out path: {remote_path}")
        #else:
        #    print("catalina.out not found on the server")
        
    except Exception as e:
        print(f"Error: {str(e)}")

# Hívjuk meg a függvényt

download_catalina_out_button = tk.Button(window, text="Download catalina.out from the server", command=new_download_link)
download_catalina_out_button.grid(row=4, column=2)


ssh_port_label = tk.Label(window, text="Port:")
ssh_port_label.grid(row=3, column=0, sticky='w')
ssh_port_entry = tk.Entry(window, textvariable=ssh_port_var,width=40)
ssh_port_entry.grid(row=3, column=1)

command1_label = tk.Label(window, text="Command 1:")
command1_label.grid(row=4, column=0, sticky='w')
command1_entry = tk.Entry(window, textvariable=command1_var,width=40)
command1_entry.grid(row=4, column=1)

command2_label = tk.Label(window, text="Command 2:")
command2_label.grid(row=5, column=0, sticky='w')
command2_entry = tk.Entry(window, textvariable=command2_var,width=40)
command2_entry.grid(row=5, column=1)

log_file1_label = tk.Label(window, text="Log File 1 [LOCAL]:")
log_file1_label.grid(row=6, column=0, sticky='w')
log_file1_entry = tk.Entry(window, width=40)
log_file1_entry.grid(row=6, column=1)

log_file1_button = tk.Button(window, text="Browse", command=browse_log_file1)
log_file1_button.grid(row=6, column=2)

log_file2_label = tk.Label(window, text="Log File 2 [LOCAL]:")
log_file2_label.grid(row=7, column=0, sticky='w')
log_file2_entry = tk.Entry(window, width=40)
log_file2_entry.grid(row=7, column=1)

log_file2_button = tk.Button(window, text="Browse", command=browse_log_file2)
log_file2_button.grid(row=7, column=2)

def colorize_aliases_and_logs():
    text = text_widget.get("1.0", tk.END)
    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        if "| grep" in line:
            grep_parts = line.split("| grep", 1)
            command_part = grep_parts[0].strip()
            grep_part = f"| grep{grep_parts[1]}"
            
            # Színezd a 'grep' részt
            grep_part = grep_parts[1].strip()
            formatted_lines.append((command_part, ""))
            formatted_lines.append((grep_part, "grep_result"))
        else:
            formatted_lines.append((line, ""))  # Üres címke, ha nem kell színezni

    #text_widget.delete("1.0", tk.END)  # Törölje a widget tartalmát, hogy újra be tudjuk színezni.

    for line, tag in formatted_lines:
        text_widget.insert(tk.END, line + "\n", tag)

    text_widget.tag_config("grep_result", foreground="red")

    # A beillesztett tartalom görgetése a végére
    #text_widget.insert(tk.END, "")
    #text_widget.see(tk.END)




# Function to start SSH connections and execute commands
# Function to start SSH connections and execute commands
def start_ssh_connections():
    global ssh, ssh2, stop_threads

    # Get the log file paths from the Entry widgets
    log_file1_path = log_file1_entry.get()
    log_file2_path = log_file2_entry.get()

    # Open the log files for writing
    log_file1 = open(log_file1_path, 'a')
    log_file2 = open(log_file2_path, 'a')

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host_var.get(),
            username=ssh_username_var.get(),
            key_filename=ssh_key_filename_var.get(),
            port=int(ssh_port_var.get())
        )

        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(
            hostname=ssh_host_var.get(),
            username=ssh_username_var.get(),
            key_filename=ssh_key_filename_var.get(),
            port=int(ssh_port_var.get())
        )

        text_widget_local = text_widget
        stdin_local = None
        stdout_local = None
        stderr_local = None

        def execute_command(ssh_conn, command, log_file):
            nonlocal text_widget_local, stdin_local, stdout_local, stderr_local
            stdin_local, stdout_local, stderr_local = ssh_conn.exec_command(command)
            while not stop_threads and not stdout_local.channel.exit_status_ready():
                output = stdout_local.channel.recv(4096).decode('utf-8')
                text_widget_local.insert(tk.END, output)
                text_widget_local.see(tk.END)
                log_file.write(output)  # Write the output to the log file

        thread1 = threading.Thread(target=execute_command, args=(ssh, command1_var.get(), log_file1))
        thread2 = threading.Thread(target=execute_command, args=(ssh2, command2_var.get(), log_file2))

        thread1.start()
        thread2.start()

        just_fetch_catalina_out_path()
        check_ssh_connection()
        #execute_command(ssh,check_tomcat_java__deployer_version(), log_file1)
        ##get_catalina_out_path()
        # Most hívjuk meg a grep eredmények színezését
        

    except NoValidConnectionsError as e:
        # Handle SSH connection errors specific to paramiko
        error_message = f"SSH Connection Error: {str(e)}\n"
        text_widget.insert(tk.END, error_message)
        text_widget.see(tk.END)

    except Exception as e:
        # Handle other exceptions
        error_message = f"Exception: {str(e)}\n"
        text_widget.insert(tk.END, error_message)
        text_widget.see(tk.END)

        # Ha szeretnéd, hogy az összes kivétel megjelenjen a text_widget-en,
        # itt kezelheted az általános kivételeket
        # például:
        text_widget.insert(tk.END, f"General Exception: {str(e)}\n")
        text_widget.see(tk.END)

        

# Create a "Start" button that calls start_ssh_connections when clicked
start_button = tk.Button(window, text="Start SSH Connections", command=start_ssh_connections)
start_button.grid(row=8, columnspan=2)

#start_button = tk.Button(window, text="Colorize 'grep'", command=colorize_aliases_and_logs)
#start_button.grid(row=8, columnspan=8)

def stop_ssh_connections():
    global ssh, ssh2, stop_threads
    stop_threads = True
    if ssh:
        ssh.close()
    if ssh2:
        ssh2.close()

stop_button = tk.Button(window, text="Stop SSH Connections", command=stop_ssh_connections)
stop_button.grid(row=8, column=2)


def on_closing():
    global ssh, ssh2
    if ssh:
        ssh.close()
    if ssh2:
        ssh2.close()
    window.destroy()

# ... (a kód többi része)

# ... (a kód többi része)

# Create a Text widget to display the output
text_widget = tk.Text(window, wrap=tk.WORD, width=80, height=20)
text_widget.grid(row=10, columnspan=3)

# Create a Text widget for the constant text
constant_text_widget = tk.Text(window, wrap=tk.WORD, width=80, height=10)
constant_text_widget.grid(row=11, columnspan=3)

# Define a tag for the constant text widget
constant_text_widget.tag_configure("constant_text", font=("Helvetica", 12), foreground="black",background="yellow")

# Add the constant text to the constant_text_widget with the "constant_text" tag
constant_text = """SSH Connection Instructions:
1. Tunnel Connection:
   - FETCHER currently supports SSH connections through tunnels.
   - Ensure that you have access to the SSH server through the specified tunnel configuration.

2. Private Key Format:
   - FETCHER accepts only OpenSSH-compatible private key files (usually with a .pem extension).
   - If you have a PuTTY Private Key (.ppk), you need to convert it to OpenSSH format before use.
   - To convert a PuTTY Private Key to OpenSSH format, you can use the puttygen tool or third-party online converters.

3. Log File Locations:
   - FETCHER allows you to specify where you want to save the log files generated during SSH sessions.
   - "Log File 1" and "Log File 2" represent the paths where you want to save the log outputs for the respective SSH connections.
   - Click the "Browse" button next to each field to select a location for the log file.

Please follow these instructions to set up your SSH connection and enjoy using FETCHER!

If you encounter any issues or have further questions, feel free to reach out for assistance.
"""
constant_text_widget.insert(tk.END, constant_text, "constant_text")

# ... (a kód többi része)


# ... (a kód többi része)



# Set the protocol for closing the window
window.protocol('WM_DELETE_WINDOW', on_closing)

# Run the Tkinter main loop
window.mainloop()
