#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "No arguments provided. Give topic and a producer-x.properties file for arguments."
    exit 2
fi

if [[ -f "$2" ]]; then
	TOPIC=$1
	PROPERTIES=$2
else
 	echo "$2 is not file"
 	exit 1
fi 

PATH="./bin/kafka-producer-perf-test.sh"

for i in 10 100 1000 10000 100000; do
	echo ""
 	echo "Number of Records: $((1000*1024*1024/$i)), record size: $i"
 	#./bin/kafka-run-class.sh org.apache.kafka.tools.ProducerPerformance 
	SCRIPT="${PATH} --topic ${TOPIC} --num-records $((1000*1024*1024/${i})) --record-size ${i} --throughput -1 --producer.config ${PROPERTIES}"
 	#echo $SCRIPT
 	"$SCRIPT"
 	echo "----------------------------------------------------------------------------------------------------"
done;
