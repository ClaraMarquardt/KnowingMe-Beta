# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         system_check
# Purpose:      Check platform on which application is being executed
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Python 2.7
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Initialisation
# ------------------------------------------------------------------------ #

# Dependencies
import os, sys

# ------------------------------------------------------------------------ #
# Test Plaform
# ------------------------------------------------------------------------ #

# obtain platform
platform  = sys.platform
print(platform)

# windows/non-windows
if bool(re.match("win", platform))==True:
	print("windows")
else: 
	print("non-windows")

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
