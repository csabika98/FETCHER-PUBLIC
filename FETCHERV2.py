import tkinter
import tkinter.messagebox
import customtkinter
from customtkinter import filedialog  # Import filedialog from customctkinter
import os
import paramiko
import paramiko.util
import logging
import configparser
import smtplib
from paramiko.ssh_exception import NoValidConnectionsError
import sys
import threading
from paramiko import Transport
from scp import SCPClient
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import re
import pexpect
import os
import stat
import shutil
import errno


from email import encoders
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        

                # configure window
        #1547x988
        self.title("Fetcher Log-Fetcher alpha release")
        self.geometry(f"{1920}x{1080}")
        self.email_schedule = None  # A variable to keep track of the scheduled email task
        self.email_schedule_interval = 600  # Default interval is 10 minutes (in seconds)
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        logging.basicConfig(filename="error.log", level=logging.ERROR)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=20, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(20, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Download catalina.out from the server", command=self.download_catalina_out)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Backup MySQL database",command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Restart Tomcat (APP&UM)",command=self.restart_tomcats)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Fetch Tomcat//Deployer version",command=self.Fetch_tomcat__deployer_version)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Edit  configuration properties",command=self.sidebar_button_event)
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Set email notifications/alerts",command=self.open_email_toplevel)
        self.toplevel_window = None
        self.sidebar_button_6.grid(row=6, column=0, padx=20, pady=10)
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.logo_label_2 = customtkinter.CTkLabel(self.sidebar_frame, text="SSH credentials", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_2.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.entry_ssh_host_var = customtkinter.StringVar(value="SSH Host")
        self.entry_ssh_host = customtkinter.CTkEntry(self.sidebar_frame, textvariable=self.entry_ssh_host_var , placeholder_text="SSH Host")
        self.entry_ssh_host.grid(row=8, column=0, padx=20, pady=10)
       
        self.entry_username_var = customtkinter.StringVar(value="SSH Username")
        self.entry_username = customtkinter.CTkEntry(self.sidebar_frame, textvariable=self.entry_username_var, placeholder_text="SSH Username")
        self.entry_username.grid(row=9, column=0, padx=20, pady=10)
        self.entry_ssh_port_var = customtkinter.StringVar(value="SSH Port")
        self.entry_ssh_port = customtkinter.CTkEntry(self.sidebar_frame, textvariable=self.entry_ssh_port_var  , placeholder_text="SSH port")
        self.entry_ssh_port.grid(row=10, column=0, padx=20, pady=10)
        self.entry_private_key_var = customtkinter.StringVar(value="Private key location")
        self.entry_private_key = customtkinter.CTkEntry(self.sidebar_frame, textvariable=self.entry_private_key_var, placeholder_text="SSH Private Key")
        self.entry_private_key.grid(row=11, column=0, padx=20, pady=10)
        self.browse_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Browse", command=self.browse_private_key)
        self.browse_button_1.grid(row=12, column=0, padx=20, pady=10)
        #self.entry_private_key_var = customtkinter.StringVar()
        self.logo_label_3 = customtkinter.CTkLabel(self.sidebar_frame, text="Saving options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_3.grid(row=13, column=0, padx=20, pady=(10, 0))
        self.entry_log_file_1_var = customtkinter.StringVar(value="Log file")
        self.entry_log_file_1 = customtkinter.CTkEntry(self.sidebar_frame, textvariable=self.entry_log_file_1_var, placeholder_text="Log File 1")
        self.entry_log_file_1.grid(row=14, column=0, padx=20, pady=10)
        self.browse_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Browse", command=self.browse_log_file1)
        self.browse_button_2.grid(row=15, column=0, padx=20, pady=10)
    
        
        
        #self.main_button_2 = customtkinter.CTkButton(master=self.sidebar_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        #self.main_button_2.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=16, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=17, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=18, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=19, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry_var = customtkinter.StringVar()
        self.entry = customtkinter.CTkEntry(master=self, textvariable=self.entry_var, placeholder_text="Command")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), stick="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Execute", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.start_ssh_connections)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=800, height=650)
        self.textbox.grid(row=0, column=1,padx=(20, 10), pady=(10, 10), sticky="ew")

        # create tabview
        #self.tabview = customtkinter.CTkTabview(self, width=250)
        #self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #self.tabview.add("CTkTabview")
        #self.tabview.add("Tab 2")
        #self.tabview.add("Tab 3")
        #self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        #self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        #self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        #values=["Value 1", "Value 2", "Value Long Long Long"])
        #self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        #self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    #values=["Value 1", "Value 2", "Value Long....."])
        #self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        #self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           #command=self.open_input_dialog_event)
        #self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        #self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        #self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Load & Save Settings:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkButton(master=self.radiobutton_frame, text="Load Settings", command=self.load_settings)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkButton(master=self.radiobutton_frame, text="Save Settings", command=self.save_settings)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        #self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        #self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Not Connected",text_color="red", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=2, column=0, padx=20, pady=(20, 10))
        #self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        #self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.grep_mode_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Predefined Greps", anchor="w")
        self.grep_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.grep_mode_optionemenu = customtkinter.CTkOptionMenu(self.slider_progressbar_frame, values=["'DEBUG'", "'TRACE'", "'INFO'", "'WARN'", "'ERROR'", "'Excel'", "'Executing excel'" , "'with input'", "'log'", "'Event'", "'event-attribute'", "'Event handling for event'", "'Summary report of SetValues event'", "'Number of successfully found implementations:'definenumber'", "'Number of implementations with inconsistencies (ignored):'definenumber'", "'Number of implementations with error while updating:'definenumber'", "'fire event 'defineeventname'", "'fire event'", "'Export triggered by event'", "'Http request:'", ],
                                                                       )
        self.grep_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="n")
        self.add_grep_1 = customtkinter.CTkButton(master=self.slider_progressbar_frame, text="Add", command=self.set_command1_from_dropdown)
        self.add_grep_1.grid(row=6, column=0, pady=10, padx=20, sticky="n")
        #self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        #self.progressbar_2.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        #self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        #self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        #self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        #self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        #self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        #self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        #self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #self.scrollable_frame.grid_columnconfigure(0, weight=1)
        #self.scrollable_frame_switches = []
        #for i in range(100):
        #    switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
        #    switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        #    self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Debug mode")
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        

        #self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        #self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        #self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        #self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        #self.checkbox_3.configure(state="disabled")
        #self.checkbox_1.select()
        #self.scrollable_frame_switches[0].select()
        #self.scrollable_frame_switches[4].select()
        #self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        #self.optionmenu_1.set("CTkOptionmenu")
        #self.combobox_1.set("CTkComboBox")
        #self.slider_1.configure(command=self.progressbar_2.set)
        #self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.constant_text = """SSH Connection Instructions:
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
        self.textbox.insert("0.0", self.constant_text)
        #self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        #self.seg_button_1.set("Value 2")

        self.current_directory = os.getcwd()
        self.ssh_key_filename_var = customtkinter.StringVar()
        self.ssh_host_var = customtkinter.StringVar()
        self.ssh_username_var = customtkinter.StringVar()
        self.ssh_port_var = customtkinter.StringVar()
        self.command1_var = customtkinter.StringVar()
        self.command2_var = customtkinter.StringVar()
    
    def include_logs_as_attachment(self):
        #send_email_window = Email_Top_Level_Window(self)
        log_file_path = self.entry_log_file_1_var.get()
        log_file_name = os.path.basename(log_file_path)
        return log_file_path, log_file_name

    #def create_send_email_window(self):
    #    send_email_window = Email_Top_Level_Window(self)  # Pass the App instance
        # Other logic to show the send_email_window

    def open_email_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            #self.toplevel_window = Email_Top_Level_Window(self)
            self.toplevel_window = Email_Top_Level_Window(self)
            self.toplevel_window.focus()
            self.toplevel_window.grab_set()  # create window if its None or destroyed
        else:
            self.toplevel_window = Email_Top_Level_Window(self)
            self.toplevel_window.focus()
            self.toplevel_window.grab_set()
            
        #self.save_button = customtkinter.CTkButton(self, text="Save Email Settings", command=lambda: self.save_email_settings(email_entry.get(), schedule_entry.get()))
        #self.save_button.pack(padx=10, pady=10)  # if window exists focus it
            
    # if window exists focus it
    # Create labels, entry fields, and buttons for email settings
    # Modify your GUI creation code to add a button to trigger email sending
    #def create_gui(self):
    # ... (Your existing code)

    # Add a button to send email
    #    self.send_email_button = customtkinter.CTkButton(self, text="Send Email", command=self.send_email)
    #    self.send_email_button.grid(row=6, column=1, padx=(20, 0), pady=10)
    def Fetch_tomcat__deployer_version(self):
        self.textbox.delete("0.0", customtkinter.END)
        self.textbox.insert("0.0", "Fetching Tomcat//Deployer version...")
        
        def run_commands():
            command = "find / -name webapps 2>/dev/null"
            stdin, stdout, stderr = self.open_connection().exec_command(command)
            result = stdout.read().decode('utf-8').strip()
        
            version_patterns = ["9.0.41", "7.0.67"] 

            tomcat_app = None
            tomcat_um = None
            _part = None
            um_part = None

            # Az eredmény sorain végigiterálunk
            lines = result.splitlines()

            for line in lines:
            # A reguláris kifejezés segítségével kinyerjük a köztes részt
                match = re.search(r'/opt/(apache-tomcat-(?:' + '|'.join(version_patterns) + r')_[^/]+)/webapps', line)
                if match:
                    tomcat_name = match.group(1)
                    if "1a" in tomcat_name or "app" in tomcat_name:
                        tomcat_app = tomcat_name
                      
                    elif "1u" in tomcat_name or "um" in tomcat_name:
                        tomcat_um = tomcat_name
                       
            match__part = re.search(r'apache-tomcat-\d+\.\d+\.\d+_(\w+)', tomcat_app)
            match_um_part = re.search(r'apache-tomcat-\d+\.\d+\.\d+_(\w+)', tomcat_um)
            if match__part:
                _part = match__part.group(1)
            else:
                _part = None
            
            if match_um_part:
                um_part = match_um_part.group(1)
            else:
                um_part = None
            
            command = "alias "+ _part +"-version"
           
            stdin, stdout, stderr = self.open_connection().exec_command(command)
            result = stdout.read().decode('utf-8').strip()
            parts = result.split("=", 1)  # Split at the first "="
            if len(parts) == 2:
                result = parts[1]
            result = result.strip("'")
            to_run__version = result
            
            command = to_run__version
            stdin, stdout, stderr = self.open_connection().exec_command(command)
            result__version = stdout.read().decode('utf-8').strip()
            
            command = "grep -w version /opt/puppetlabs/puppet/modules//metadata.json"
            stdin, stdout, stderr = self.open_connection().exec_command(command)
            deployer_version = stdout.read().decode('utf-8').strip()
            #print("Tomcat version: " + " " + tomcat_app + " " + tomcat_um)
            #print(" version: " + _version)
            
            self.textbox.delete("0.0", customtkinter.END)
            self.textbox.insert("0.0", "Tomcat version: " + " " + tomcat_app + " " + tomcat_um + "\n" + "\n" + " version: " + result__version + "\n" + "\n" + "Deployer version: " + deployer_version)
            self.textbox.see(customtkinter.END)
            
        thread4 = threading.Thread(target=run_commands)
        thread4.start()
        #self.textbox.update()
    def restart_tomcats(self):
        self.textbox.delete("0.0", customtkinter.END)
        self.textbox.insert("0.0", "We are restarting APP & UM Tomcat..... This could take up to 5 minutes... you can use the application in the meantime, you will get a notification when the restart is done..")
        def run_restart_tomcats():    
            command = "find / -name webapps 2>/dev/null"
            stdin, stdout, stderr = self.open_connection().exec_command(command)
            result = stdout.read().decode('utf-8').strip()
        
            version_patterns = ["9.0.41", "7.0.67"] 

            tomcat_app = None
            tomcat_um = None
            _part = None
            um_part = None

            # Az eredmény sorain végigiterálunk
            lines = result.splitlines()

            for line in lines:
            # A reguláris kifejezés segítségével kinyerjük a köztes részt
                match = re.search(r'/opt/(apache-tomcat-(?:' + '|'.join(version_patterns) + r')_[^/]+)/webapps', line)
                if match:
                    tomcat_name = match.group(1)
                    if "1a" in tomcat_name or "app" in tomcat_name:
                        tomcat_app = tomcat_name
                      
                    elif "1u" in tomcat_name or "um" in tomcat_name:
                        tomcat_um = tomcat_name
                       
            match__part = re.search(r'apache-tomcat-\d+\.\d+\.\d+_(\w+)', tomcat_app)
            match_um_part = re.search(r'apache-tomcat-\d+\.\d+\.\d+_(\w+)', tomcat_um)
            if match__part:
                _part = match__part.group(1)
            else:
                _part = None
            
            if match_um_part:
                um_part = match_um_part.group(1)
            else:
                um_part = None
            
            command = "alias "+ _part +"-start"
            command_2 = "alias "+ _part +"-stop"

            command_3 = "alias "+ um_part +"-start"
            command_4 = "alias "+ um_part +"-stop"

            stdin, stdout, stderr = self.open_connection().exec_command(command)
            result_1 = stdout.read().decode('utf-8').strip()
            stdin, stdout, stderr = self.open_connection().exec_command(command_2)
            result_2 = stdout.read().decode('utf-8').strip()
            parts = result_1.split("=", 1)  # Split at the first "="
            if len(parts) == 2:
                result = parts[1]
            result = result.strip("'")
            splitted_1 = result
            parts_2 = result_2.split("=", 1)
            if len(parts_2) == 2:
                result = parts_2[1]
            result_2 = result.strip("'")
            splitted_2 = result_2
           
            stdin, stdout, stderr = self.open_connection().exec_command(command_3)
            result_3 = stdout.read().decode('utf-8').strip()
            stdin, stdout, stderr = self.open_connection().exec_command(command_4)
            result_4 = stdout.read().decode('utf-8').strip()
            #print(result_3)
            #print(result_4)
            parts = result_3.split("=", 1)
            if len(parts) == 2:
                result =parts[1]
            result = result.strip("'")
            splitted_3 =result
            
            parts = result_4.split("=", 1)
            if len(parts) == 2:
                result =parts[1]
            result = result.strip("'")
            splitted_4 =result
           
            app_start = splitted_1
            app_stop = splitted_2
            um_start = splitted_3
            um_stop = splitted_4
            command = app_stop + " &&  " + app_start + " &&  " + um_stop + " && " + um_start
            run_comm = stdin, stdout, stderr = self.open_connection().exec_command(command)
            #self.textbox.delete("0.0", customtkinter.END)
            #self.textbox.insert("0.0", run_comm)
            #self.textbox.insert("0.0", stdout.read().decode('utf-8').strip())
            stdout.read().decode('utf-8').strip()
            
            #print(final_res)
            #self.textbox.delete("0.0", customtkinter.END)
            #self.textbox.insert("0.0", final_res)
            time.sleep(300)
            self.textbox.insert("0.0", "Stage is up and ready!")
            #result__version = stdout.read().decode('utf-8').strip()
        thread4 = threading.Thread(target=run_restart_tomcats)
        thread4.start()   



    def connector_change(self):
        self.logo_label.destroy()
        command = "hostname"
        host_name = stdin, stdout, stderr = self.open_connection().exec_command(command)
        host_name = stdout.read().decode('utf-8').strip()
        
        text_there = "Connected to: " + host_name
        self.logo_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text=text_there ,text_color="green", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=2, column=0, padx=20, pady=(20, 10))    
    
    def handleRemoveReadonly(self, func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(path)

    try:
        folder_path = os.getcwd()  # Replace with the actual folder path
        os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # Change permissions (0777)
    except PermissionError as e:
        handleRemoveReadonly(os.chmod, folder_path, e)


    def set_command1_from_dropdown(self):
        selected_grep = self.grep_mode_optionemenu.get()
        existing_word = self.entry.get()
        print(selected_grep)
        self.entry_var.set(existing_word + " | grep" + " " + selected_grep)
        #self.entry_var.initialize(self.entry_var.set("     |" + selected_grep))
        print(self.entry_var.get())
        #self.entry_var.set("     |" + selected_grep)
        print(self.entry_var.get())        


    def open_connection(self):
        #proxy_command = f"ssh -W %h:%p -p {jump_host['port']} {jump_host['username']}@{jump_host['hostname']}"

        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname=self.entry_ssh_host.get(),
                username=self.entry_username.get(),
                key_filename=self.entry_private_key_var.get(),
                port=str(self.entry_ssh_port.get()),
                #sock=paramiko.ProxyCommand("ssh ")

            )
            return self.ssh
        except Exception as e:
            logging.error(str(e))
            self.textbox.delete("0.0", customtkinter.END)
            self.textbox.insert("0.0", f"Error: {str(e)}")
            self.textbox.see(customtkinter.END)

    def download_file_with_scp(self,remote_path, local_path, chunk_size=1024):
        
        
        ssh = self.open_connection()
        transport = ssh.get_transport()
        try:
            with SCPClient(transport) as scp:
                with open(local_path, 'wb') as local_file:
                    scp.get(remote_path, local_file.write, preserve_times=True)
            print("Downloaded catalina.out to: " + local_path)
        except Exception as e:
            print("Error:", str(e))
            #self.textbox.insert("0.0", "Downloaded catalina.out to: " + local_path)
            #self.textbox.see(customtkinter.END)
            #self.textbox.update()


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def browse_private_key(self):
        self.file_path = filedialog.askopenfilename()
        print(self.file_path)
        self.entry_private_key_var.set(self.file_path)
        print(self.entry_ssh_host.get())
        print(self.entry_ssh_port.get())
        print(self.entry_private_key_var.get())
        #self.ssh_key_filename_var.set(self.file_path)
    
    def browse_log_file1(self):
        self.log_file1_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log, *.txt")])
        self.entry_log_file_1.delete(0, customtkinter.END)  # Törölje az előző értéket az CTkEntry-ből
        self.entry_log_file_1.insert(0, self.log_file1_path)  # Állítsa be az új fájl elérési útvonalát
    
    def download_catalina_out(self):
        self.textbox.delete("0.0", customtkinter.END)
        self.textbox.insert("0.0", "PLEASE WAIT UNTIL THE DOWNLOAD IS FINISHED! IN THE MEANTIME YOU CAN USE THE APPLICATION AS USUAL!")
        def fetch_catalina_out():
            command = "find / -name catalina.out 2>/dev/null | head -n 1"  # Keresd meg a catalina.out fájlt
            remote_path = stdin, stdout, stderr = self.open_connection().exec_command(command)
            current_directory = os.getcwd()
            local_path = current_directory + "/catalina.out"
            #remote_path= just_fetch_catalina_out_path()

            # A kimenet tartalmazza az elérési útvonalat (ha megtalálható)
            remote_path = stdout.read().decode('utf-8').strip()
            ssh = self.open_connection()
            transport = ssh.get_transport()
            with SCPClient(transport) as scp:
                scp.get(remote_path, local_path)
            print("Downloaded catalina.out to: " + local_path)
            self.textbox.delete("0.0", customtkinter.END)
            self.textbox.insert("0.0", "Downloaded catalina.out to: " + local_path)
            self.textbox.see(customtkinter.END)
            #self.textbox.update()
        thread2 = threading.Thread(target=fetch_catalina_out)
        thread2.start()
        

    def start_ssh_connections(self):
       
        
        # Wait for the SSH hosts list and read the response
        #response = shell.recv(4096).decode('utf-8')

        # Print the available hosts
        #print(response)
        #command = 'ssh '
        #stdin, stdout, stderr = self.open_connection().exec_command(command)
        #output = stdout.read().decode('utf-8').strip()
        #print(output)
        #proxy_command = f"ssh -W %h:%p -p {jump_host['port']} {jump_host['username']}@{jump_host['hostname']}"
    # Get the log file paths from the CTkEntry widgets
        log_file1_path = self.entry_log_file_1.get()
    

    # Open the log files for writing
        log_file1 = open(log_file1_path, 'a')
    
        #text_widget_local = self.textbox.insert("")
        stdin_local = None
        stdout_local = None
        stderr_local = None
        stop_threads = False
        self.textbox.delete("0.0", customtkinter.END)
        def execute_command(ssh_conn, command, log_file):
            nonlocal stdin_local, stdout_local, stderr_local
            stdin_local, stdout_local, stderr_local = ssh_conn.exec_command(command)
            while not stop_threads and not stdout_local.channel.exit_status_ready():
                output = stdout_local.channel.recv(4096).decode('utf-8')
                self.textbox.insert(customtkinter.END, output)
                self.textbox.see(customtkinter.END)
                log_file.write(output)
        thread1 = threading.Thread(target=execute_command, args=(self.open_connection(), self.entry.get(), log_file1))
        thread1.start()
        #thread3 = threading.Thread(target=execute_command, args=(self.open_connection(), self.entry.get(), log_file1))
        #thread3.start()
        #thread1.start()
        #thread1.join()
        #thread3.join()
        self.connector_change() # Change the label to "Connected to: <hostname>"

    # Create a function to save settings
    def save_settings(self):
            config = configparser.ConfigParser()
            config['SSH'] = {
                'host': self.entry_ssh_host.get(),
                'username': self.entry_username.get(),
                'key_filename': self.entry_private_key_var.get(),
                'port': str(self.entry_ssh_port.get()),
                'command1': self.entry.get(),
                'log_file1': self.entry_log_file_1_var.get()
            }
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            self.textbox.delete("0.0", customtkinter.END)
            self.textbox.insert("0.0", "Settings saved successfully!")
            self.textbox.see(customtkinter.END)


    def load_settings(self):
            config = configparser.ConfigParser()
            config.read('config.ini')
            ssh_settings = config['SSH']
            self.entry_ssh_host_var.set(ssh_settings.get('host', ''))
            self.entry_username_var.set(ssh_settings.get('username', ''))
            self.entry_private_key_var.set(ssh_settings.get('key_filename', ''))
            self.entry_ssh_port_var.set(ssh_settings.get('port', ''))
            self.entry_var.set(ssh_settings.get('command1', ''))
            print(self.entry_var.get())

            #self.entry_log_file_1_var.delete(0, customtkinter.END)
            self.entry_log_file_1_var.set(ssh_settings.get('log_file1', ''))
            self.textbox.delete("0.0", customtkinter.END)
            self.textbox.insert("0.0", "Settings loaded successfully!")

class Email_Top_Level_Window(customtkinter.CTkToplevel):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.app = app
        self.include_logs_in_body = False
        self.include_logs_as_attachment = False
        #self.include_logs_in_body = False
        #self.include_as_attachment = False  # A variable to track if logs should be included in the email body
        self.log_file_path = ""  # Initialize as an empty string
        self.log_file_name = ""  # Initialize as an empty string  # Store log_file_name as an instance variable
        self.geometry("818x839")
        self.title("Set email and notifications/alert")
        
        email_label = customtkinter.CTkLabel(self, text="Email:")
        email_entry = customtkinter.CTkEntry(self)
        email_label.pack(padx=10, pady=10)
        email_entry.pack(padx=10, pady=10)

        schedule_label = customtkinter.CTkLabel(self, text="Schedule (minutes):")
        schedule_entry = customtkinter.CTkEntry(self)
        schedule_label.pack(padx=10, pady=10)
        schedule_entry.pack(padx=10, pady=10)

        custom_body_label = customtkinter.CTkLabel(self, text="Custom message:")
        custom_body_text = customtkinter.CTkTextbox(self, wrap="word", width=300, height=400)  # Adjust width and height as needed
        custom_body_label.pack(padx=10, pady=10)
        custom_body_text.pack()

        self.checkbox_2 = customtkinter.CTkCheckBox(master=self, text="Include logs as an attachment")
        self.checkbox_2.pack(padx=10, pady=10)

        self.checkbox_3 = customtkinter.CTkCheckBox(master=self, text="Include logs in the email body")
        self.checkbox_3.pack(padx=10, pady=10)

        save_button = customtkinter.CTkButton(self, text="Save Email Settings/Send email", command=lambda: self.save_email_settings(email_entry.get(), schedule_entry.get(), custom_body_text.get("1.0", "end-1c")))
        save_button.pack(padx=10, pady=10)

    def save_email_settings(self, recipient_email, schedule_minutes, custom_body):
        # Implement the logic to save email settings here
        # email and schedule are the values entered by the user
        # Email configuration
        print(recipient_email)
        print(schedule_minutes)
        include_logs_in_body = 0
        include_logs_as_attachment = 0

        include_logs_as_attachment = self.checkbox_2.get()
        include_logs_in_body = self.checkbox_3.get()
        print(include_logs_as_attachment)
        print(include_logs_in_body)

        if (include_logs_as_attachment==1 and include_logs_in_body==0) or (include_logs_in_body==1 and include_logs_as_attachment==1):
            #app.create_send_email_window()
            self.log_file_path, self.log_file_name = self.app.include_logs_as_attachment()
            print(self.log_file_path, self.log_file_name)
            smtp_server = ''
            smtp_port = 587  # Update to your SMTP server's port
            sender_email = ''
            #sender_username = 'apikey'
            sender_password = ''
        
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = 'Log File Attachment'
            attachment = open(self.log_file_path, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={self.log_file_name}')
            message.attach(part)
        
            # Add the body of the email as plain text
            body = custom_body
            message.attach(MIMEText(body, 'plain'))

            try:
                # Connect to the SMTP server and send the email
                self.smtp_server = smtplib.SMTP(smtp_server, smtp_port)
                self.smtp_server.starttls()
                self.smtp_server.login(sender_email, sender_password)
                self.smtp_server.sendmail(sender_email, recipient_email, message.as_string())
                self.smtp_server.quit()

            # Close the pop-up
                self.destroy()  # Close the pop-up window

            except Exception as e:
            # Handle email sending error
                print("Error sending email:", str(e))

        if (include_logs_in_body==1 and include_logs_as_attachment==0) or (include_logs_in_body==1 and include_logs_as_attachment==1):
            self.log_file_path, self.log_file_name = self.app.include_logs_as_attachment()
            print(self.log_file_path, self.log_file_name)
            smtp_server = ''
            smtp_port = 587  # Update to your SMTP server's port
            sender_email = ''
            #sender_username = 'apikey'
            sender_password = ''
            with open(self.log_file_path, 'r') as log_file:
                log_content = log_file.read()
             # Create an email message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = 'Log'

            # Set the log file content as the email body
            body = custom_body + "\n\n" + log_content
            message.attach(MIMEText(body, 'plain'))

            try:
                # Connect to the SMTP server and send the email
                self.smtp_server = smtplib.SMTP(smtp_server, smtp_port)
                self.smtp_server.starttls()
                self.smtp_server.login(sender_email, sender_password)
                self.smtp_server.sendmail(sender_email, recipient_email, message.as_string())
                self.smtp_server.quit()

                # Close the pop-up
                self.destroy()  # Close the pop-up window

            except Exception as e:
                # Handle email sending error
                print("Error sending email:", str(e))


        if(include_logs_in_body==0 and include_logs_as_attachment==0):
            smtp_server = ''
            smtp_port = 587  # Update to your SMTP server's port
            sender_email = ''
            #sender_username = 'apikey'
            sender_password = ''

            # Create an email message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = 'Log'
        
            # Add the body of the email as plain text
            body = custom_body
            message.attach(MIMEText(body, 'plain'))

            # Attach any files, configure the email content, etc.

            try:
                # Connect to the SMTP server and send the email
                self.smtp_server = smtplib.SMTP(smtp_server, smtp_port)
                self.smtp_server.starttls()
                self.smtp_server.login(sender_email, sender_password)
                self.smtp_server.sendmail(sender_email, recipient_email, message.as_string())
                self.smtp_server.quit()

                # Close the pop-up
                self.destroy()  # Close the pop-up window

            except Exception as e:
                # Handle email sending error
                print("Error sending email:", str(e))
        


if __name__ == "__main__":
    app = App()
    app.mainloop()
