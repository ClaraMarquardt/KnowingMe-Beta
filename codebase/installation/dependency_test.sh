# ----------------------------------------------------------------------- #

# KnowingMe 

# File:         dependency_test   
# Purpose:      Test installation of dependencies
# Maintainer:   Clara Marquardt
# Last Updated: 2018-01-09
# Language:     Shell
# Notes:

# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Intialize - Dependency List
# ------------------------------------------------------------------------ #
filename="installation/dependency.txt"

# ------------------------------------------------------------------------ #
# Loop Over Dependencies - Test Installation
# ------------------------------------------------------------------------ #
while read -r line; do
	
	echo "----------------"
	echo "## "$line
	
	line_mod=${line%%==*}
	install_test=$(${pip_custom} show $line_mod)
	echo $install_test
	
	install_test_success=${#install_test}

	if [ "$install_test_success" = '0' ]; then
		echo ">> Error"
	else
		echo ">> Success"
	fi

done < "$filename"

# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #
