#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "No arguments provided. Give path, topic and a server.properties file for arguments."
    exit 2
fi

if [[ -f "$3" ]]; then
	PATH=$1
	TOPIC=$2
	PROPERTIES=$3
else
 	echo "$3 is not file"
 	exit 1
fi 

PATH="${PATH}bin/kafka-producer-perf-test.sh"

for i in 10 100 1000 10000 100000; do
	echo ""
 	echo "Number of Records: $((1000*1024*1024/$i)), record size: $i"
 	COMMAND="${PATH} --topic ${TOPIC} --num-records $((1000*1024*1024/${i})) --record-size ${i} --throughput -1 --producer.config ${PROPERTIES}"
 	#$PATH --topic $TOPIC --num-records $((1000*1024*1024/$i)) --record-size $i --throughput -1 --producer.config $PROPERTIES
 	echo $COMMAND
 	eval "$COMMAND"
 	echo "----------------------------------------------------------------------------------------------------"
done;