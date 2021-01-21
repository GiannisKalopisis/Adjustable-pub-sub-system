#!/usr/bin/expect

#This script connects to the sdi1500059@195.134.67.93 at port 2244 with ssh

# set username to server
set host 195.134.67.93
# set password to server

#exec 'gnome-terminal -x'
spawn ssh -p2244 $username@$host
expect "password"
send "$password\r"
interact
