# Getting Set-Up

##### Section 1 - Github
_(Skip if you are already set-up with Github/Access to the 'KnowingMeTester' Repository)_

```
# [1] Create a free Github account
Visit <https://github.com/> > 'Sign up'

Notes: 
- The tester application will be updated regularly (as new NLP modules are shipped) and as such it 
probably makes the most sense for us to pull new versions directly from Github as they are uploaded 
- * Should this be a problem - can also think of some other solution!

# [2] Obtain access to the 'KnowingMeTester' Repository
- Email me (Clara) your Github username > Will send you an invite
- You can then access the repository at: <github.com/ClaraMarquardt/KnowingMeTester/blob/master/README.md>

```

##### Section 2 - Python
_(Skip if you are already set-up with Python 2.7)_

```
# [1] Install Python (2.7) (with commandline support)

## Mac: 
- Open the Terminal (search for 'Terminal') - enter all below commands into the Terminal window

- Install Homebrew (Note: this step may take longer if Xcode is not yet installed):
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

- Install Python and pip:
brew install python

- Confirm that Python and pip have been correctly configured:

python -V  # should return ~ 'Python 2.7.13'
pip -V     # should return ~ 'pip 9.0.1 from /usr/local/lib/python2.7/site-packages (python 2.7)' 

## Windows 

- Note: There are different options - the below described setup process is recommended as it is 
easy to setup (and does not require administrator privileges / command line integrations)

- Install anaconda for windows (python 2.7 version): https://www.anaconda.com/download/

- Execute the installer (keeping all default settings)

- Confirm that Python and pip have been correctly configured. Launch the 'Anaconda Prompt' 
(from the start menu) and type in the below commands: 

python -V  # should return ~ 'Python 2.7.13 :: Anaconda 4.4.0'
pip -V     # should return ~ 'pip 9.0.1 from C:\Users\...\Continuum\Anaconda2\lib\site-packages (python 2.7)' 


```