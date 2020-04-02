#!/bin/bash

#url=$1

function main(){
	app_port=3000
    name="git_server"
	check $@
    server_install_check 
    
	exit 0
}


function check(){
    #local OPTIND opt i
    while getopts p:u: opt; do
    	case "${opt}" in
    		p) app_port=$OPTARG;;
            u) url=$OPTARG;;
            \?) help;;
        esac
    done
    #shift $((OPTIND -1))

    if [ "$url" = "" ]; then

        echo "D: you did not supply a url!"
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
    npm i
    if [ "$app_port" != 3000 ]; then
        export PORT="$app_port"
        printf '%s\n' "Starting server on port $app_port..."
    else
        printf '%s\n' "Starting server on default port 3000..."
    fi
    
    server="http://127.0.0.1:$app_port"
    echo "Enter in your browser: $server"

    npm start 

    cd ..

    (echo "BASH" && echo "$server") | python3 WEBSCRAPER.py &
}

main $@
