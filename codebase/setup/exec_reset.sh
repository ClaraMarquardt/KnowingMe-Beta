
# directory
echo $(dirname -- "$BASH_SOURCE")
cd -- "$(dirname -- "$BASH_SOURCE")"
cd ..
cd ..

# check that in correct directory (KnowingMe)
current_path=$(pwd)
echo $current_path

# if ! [ -e ${current_path}/codebase ]; then
 # echo "Not in KnowingMe directory > Exiting"
 # sleep 3
 # exit;
# fi

# if ! [ -e ${current_path}/documentation ]; then
 # echo "Not in KnowingMe directory > Exiting"
 # sleep 3
 # exit;
# fi

# if ! [ "${PWD##*/}" = "KnowingMe" ]; then
 # echo "Not in KnowingMe directory > Exiting"
 # sleep 3
 # exit;
# fi

# reset-app
find . -type f -name '*pyc' -exec mv {} ~/.Trash \;
find . -type f -name '.DS_Store' -exec mv {} ~/.Trash \;
