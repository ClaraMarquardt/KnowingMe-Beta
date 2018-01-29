## KnowingMe - Manual Setup

### Requirements

```

# Python (2.7) & pip

## For instruction on how to set up Python/pip (Mac / Windows) - see the below instructions:
https://github.com/ClaraMarquardt/KnowingMe/blob/master/documentation/setup/Getting%20Setup.pdf

## To check that python and pip are correctly configured (Terminal command)
python -V # should return: ~ which 'Python 2.7.13'
pip  -V   # should return: ~ 'pip 9.0.1 from .....'

```

### Installation

```
# Notes: 
* All commands are to be entered into e.g. Terminal (Mac) / Anaconda Prompt (Windows)
* All executables (e.g. 'exec_launch') need to be executed from their location within 
  the 'KnowingMe' directory (i.e. cannot be moved/copied to another location)

# [1] Obtain the repository (Note: Need to have collaborator access to the repository)
cd [...]
git clone https://github.com/ClaraMarquardt/KnowingMe.git

# [2] Install & verify the installation
* Open the 'KnowingMe' directory
* Execute (double-click) 'codebase/setup_manual/exec_install'
  > A terminal window will open and will remain open until the setup is complete. 
  > Alternative if e.g. on windows: Execute with the commands 
    cd [Path to KnowingMe Directory]/KnowingMe
    source codebase/setup_manual/exec_install
* Verify that the installation was successful by checking the 
  generated log file ('codebase/setup_manual/exec_install.log'). A sample log file for a successful 
  installation is located at './documentation/setup/exec_install_success_sample' 

```

### Execution

```
# Launch the application
* Open the 'KnowingMe' directory 
* Execute (double-click) 'codebase/setupmanual/exec_launch'
  > A terminal window will open (and remain open). Soon after the app will open in 
  a browser window. Note that the launch process may take some time. 
  > Alternative if e.g. on windows: Execute with the commands
    cd [Path to KnowingMe Directory]/KnowingMe
    source codebase/setup_manual/exec_launch
* The app should automatically open in a browser window (http://localhost:8000/)
* NOTE (1):
  (i)  Use http _not_ https
  (ii) Open all links/new pages in the same tab 
* NOTE (2): Problems can arise if the app is not properly shut-down. To avoid problems it is recommended that 
  (i) the application is closed using 'CTRL+C' (rather than by simply closing the browser tab) and 
  (ii) that the computer is plugged in prior to app launch in case it is running low on battery

```


### Miscellaneous

```

[1] Python/Pip Executable Choice: 
The app will by default use the 'python'/'pip' executables (which python / which pip). The 
executable choicecan be modified by changing the python_custom, pip_custom paths 
in 'codebase/setup_manual/exec_setting.sh'

```

### Common Problems

```

### 'socket.error: [Errno 48] Address already in use' when trying to (re)start the application

* An instance of the application is still running in the background > the port/address is 
not available (this can happen if e.g. the application is not shut down properly / the computer 
shut down while the application was running)

# [Solution #1]
Check process not running on another terminal window. Close if running.

# [Solution #2]
Launch the app on another port by copying the file './codebase/setup/app_setting.json' to 
~/Desktop/KnowingMe_Data/app_setting_user.json and modifying the 'app_port' field in this copied file 
before restarting the app

# [Solution #3]
[1] Execute the following command:
ps -fA | grep python

[2] Inspect the output to identify the process ids of the still-running processes 

[3] Kill the problematic processes
kill -s SIGKILL [process_id]

(See the below screen shot for an illustration)

```
![here](/documentation/debug/screenshot/socket.error_debug.png?raw=true "Optional Title")

### Error upon starting the application '....HttpAccessTokenRefreshError: invalid_grant ...'

* The application's access to your gmail account has been revoked (this can happen if e.g. you manually 
removed the access from the 'Your Applications' page and/or if you reset your gmail password)

# [Solution #1]
[1] Restart the application and open the URL in a new incognito browser window > Re-authenticate

[2] Upon having received the email informing you that access has been granted to the 'KnowingMe' 
    application > Clear your browser cache

[3] Restart the application (in a normal browser window)



