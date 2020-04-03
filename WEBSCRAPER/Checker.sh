#!/bin/bash
#===============================================================================
#
#          FILE:  Checker.sh
#
#         USAGE:  ./Checker.sh -u <github url> -p <port number> [optional]
#
#   DESCRIPTION:  This script ckecks the web pages of the locally inastalled node server
#         NOTES:  Link for testing: https://github.com/xileftenurb/polymtl-inf8007-site-exemple
#        AUTHOR:  Dmytro Humeniuk and Mahmood Vahedi (dmytro.humeniuk@polymtl.ca)
#       COMPANY:  Polytechnique Montreal
#       VERSION:  1.0
#       CREATED:  03/04/2020
#===============================================================================

function main(){

    app_port=3000  # save default port number
    name="git_server"  # create a folder for storing the server
    check $@  # check user input

    server_install_check  #install and test the server


}


function check(){
    while getopts p:u: opt; do
    	case "${opt}" in
    	    p) app_port=$OPTARG;;
            u) url=$OPTARG;;
        esac
    done

    if [ "$url" = "" ]; then

        echo "You did not supply a url!" 
        exit 1
    fi

    if git ls-remote "$url" == 0; then
        printf '%s\n' "Your url is valid!"
    else 
        printf '%s\n' "$url does not exist" 
        exit 1
    fi

}


function server_install_check(){
    git clone $url $name 
    cd $name 
    npm i 1> error.txt
    if [ "$app_port" > 0 ]; then
        export PORT="$app_port"
        printf '%s\n' "Starting server on port $app_port..."
    else
        printf '%s\n' "Starting server on default port 3000..."
    fi
    
    server="http://127.0.0.1:$app_port"
    echo "Enter in your browser: $server"

    npm start & 

    sleep 3

    cd .. 
    
    (echo "BASH" && echo "$server") | python3 WEBSCRAPER.py

    killall node

}

errlog=error.txt

main $@ 2> error.txt 

if [[ -s "$errlog" ]]; then
    echo "If the program wasn't executed completely, search for errors in error.txt"
fi

