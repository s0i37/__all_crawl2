 #!/bin/bash

opts='-type f -size -10M ! -iname "*.wav" ! -iname "*.mp3"'

[[ $# -lt 1 ]] && {
	echo "$0 index_local_path [/usr/bin/find options]"
	echo "example: $0 /mnt/share/ -type f -size -10M ! -iname '*.wav' ! -iname '*.mp3'"
	exit
}

function session_file_done(){
	path="$1"
	echo "$path" >> "$session_file"
}

function session_is_file_done(){
	path="$1"
	grep "$path" "$session_file" 1> /dev/null 2> /dev/null && echo 1 || echo 0
}

function session_create(){
	session_file="$1"
	stat "$session_file" 1> /dev/null 2> /dev/null && echo 1 || {
		touch "/dev/shm/$session_file"
		ln -s "/dev/shm/$session_file" "$session_file"
		echo 0
	}
}

function session_close(){
	rm "$session_file"
	rm "/dev/shm/$session_file"
}

index="$(basename $1).txt"
session_file=".$(basename $1).sess"
is_resume=$(session_create $session_file)

find $1 $opts -print | 
while read path
do
	[[ $is_resume = 1 && $(session_is_file_done $path) = 1 ]] && {
		echo "(skip $path)"
		continue
	}
	echo "$path"
	echo ">>>$path" >> "$index"
	mime=$(xdg-mime query filetype "$path")
	ext=${path##*.}
	case $mime in
		*/xml)
			echo "<<<xml" >> "$index"
			cat "$path" >> "$index"
			;;
		text/html)
			echo "<<<html" >> "$index"
			lynx -nolist -dump "$path" >> "$index"
			;;
		text/*|*/*script)
			echo "<<<text" >> "$index"
			cat "$path" >> "$index"
			;;
		application/msword)
			echo "<<<doc" >> "$index"
			catdoc "$path" >> "$index"
			;;
		application/vnd.openxmlformats-officedocument.wordprocessingml.document)
			echo "<<<doc" >> "$index"
			unzip -p "$path" | grep '<w:r' | sed 's/<w:p[^<\/]*>/ /g' | sed 's/<[^<]*>//g' | grep -v '^[[:space:]]*$' | sed G >> "$index"
			;;
		application/vnd.ms-excel|application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
			echo "<<<xls" >> "$index"
			xls2csv -x "$path" >> "$index"
			;;
		application/pdf)
			echo "<<<pdf" >> "$index"
			pdf2txt -t text "$path" >> "$index"
			;;
		application/x-executable|application/x-ms-dos-executable)
			echo "<<<exe" >> "$index"
			/opt/radare2/bin/rabin2 -z "$path" | sed -rn "s/vaddr=[^\s]+.*string=(.*)/\1/p" >> "$index"
			;;
		application/*compressed*|application/*zip*|application/*rar*|application/*tar*|application/*gzip*)
			echo "<<<zip" >> "$index"
			#7z l "$path" | tail -n +13 >> "$index"
			temp=$(tempfile)
			rm $temp && mkdir -p "$temp/$path"
			7z x "$path" -o"$temp/$path"
			ln -s "$(realpath $0)" "$temp/$(basename $0)"
			ln -s "$(realpath $index)" "$temp/$index"
			( cd "$temp"; "./$(basename $0)" "${index%.*}"; )
			rm -r $temp
			;;
		image/*)
			echo "<<<image" >> "$index"
			identify -verbose "$path" >> "$index"
			#tesseract "$path" stdout -l eng >> "$index"
			#tesseract "$path" stdout -l rus >> "$index"
			;;
		application/octet-stream)
			echo "<<<raw" >> "$index"
			strings "$path" >> "$index"
			;;
		application/x-raw-disk-image)
			echo "<<<disk" >> "$index"
			binwalk "$path" >> "$index"
			;;
		*)
			echo "<<<$mime" >> "$index"
			file "$path" | grep text > /dev/null && cat "$path" >> "$index" || echo "$path $mime" >> unknown_mime.log
			;;
	esac
	printf "\n" >> "$index"
	session_file_done $path
done

session_close