#!/bin/bash

[[ $# -lt 1 ]] && {
	echo "$0 imap://server.com user:pass"
	echo "example: $0 imaps://imap.gmail.com someuser:somepass"
	exit
}

SERVER=$1
CREDS=$2

function get_folders(){
	curl -s --insecure --user "$CREDS" "$SERVER" |
	sed -rn 's/.* ([^\s]+)/\1/p'
}

function get_messages_count(){
	folder=$1
	curl -s --insecure --user "$CREDS" "$SERVER" -X "EXAMINE $folder" |
	grep EXISTS |
	sed -rn 's/\* ([0-9]+) .*/\1/p'
}

function get_message(){
	folder=$1
	message_id=$2
	curl -s --insecure --user "$CREDS" "$SERVER/$folder;UID=$message_id" -o "$folder/$message_id"
}

for folder in $(get_folders)
do
	folder=$(echo $folder | tr -d '\r')
	echo "[*] $folder"
	mkdir "$folder"
	max=$(get_messages_count "$folder")
	for ((id=max; id>0; id--))
	do
		echo "[+] $id"
		get_message $folder $id
	done
done