#!/usr/bin/expect

#This script transfer file or directory to the sdi1500059@195.134.67.93 at port 2244 with scp
#Arguments: 1)file or directory
#			2)destination directory

# set username to server
set host 195.134.67.93
# set password to server

#get file or directory from command line
set tranferData [lindex $argv 0];
set path [lindex $argv 1];


if {[file exists "$tranferData"]} { 
	if {[file isdirectory "$tranferData"]} {
		set type "directory"
	} else {
		set type "file"
	}
} else {
	send_user "Error: $tranferData is not file or directory...\n"
	exit 1
}

if {"$type" == "directory"} {
	spawn scp -P 2244 -r $tranferData $username@$host:$path
	expect {
		"Are you sure you want to continue connecting*" {
			send yes\r
			exp_continue
		}
		"*password:*" {
			send $password\r
			interact
		}
	}
} else {
	spawn scp -P 2244 $tranferData $username@$host:$path
	expect {
		"Are you sure you want to continue connecting*" {
			send yes\r
			exp_continue
		}
		"*password:*" {
			send $password\r
			interact
		}
	}
}


