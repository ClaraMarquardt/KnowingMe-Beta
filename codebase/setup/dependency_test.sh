# Test Dependency Setup 

# initialize
filename="setup/dependency.txt"

# loop over dependencies & test
while read -r line; do
	
	echo "----------------"
	echo "## "$line
	
	line_mod=${line%%==*}
	install_test=$(${pip_custom} show $line_mod)
	echo $install_test
	
	install_test_success=${#install_test}

	if [ "$install_test_success" = '0' ]; then
		echo ">> (!) ERROR"
	else
		echo ">> Success"
	fi
done < "$filename"