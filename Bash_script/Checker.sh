#!/bin/bash

#url=$1

function main(){
	app_port=0
	check $@
    echo $app_port
    echo $url
	#exit 0

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

    if curl --output /dev/null --silent --head --fail "$url"; then
        printf '%s\n' "$url exist"
    else
        printf '%s\n' "$url does not exist"
    fi

}

main $@