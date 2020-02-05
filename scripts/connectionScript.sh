#!/usr/bin/expect

#This script connects to the sdi1500059@195.134.67.93 at port 2244 with ssh

set username sdi1500059
set host 195.134.67.93
set password F-Qrfarqh

#exec 'gnome-terminal -x'
spawn ssh -p2244 $username@$host
expect "password"
send "$password\r"
interact