#!/bin/bash


#
#count and test arguments
#
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


#
#get script directory
#
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

PATH="${DIR}/bin/kafka-run-class.sh org.apache.kafka.tools.ProducerPerformance"



#
#execute script :( 
#

if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx512M"
fi

for i in 10 100 1000 10000 100000; do
	echo ""
 	echo "Number of Records: $((1000*1024*1024/$i)), record size: $i"
 	#./bin/kafka-run-class.sh org.apache.kafka.tools.ProducerPerformance 
	SCRIPT="${PATH} --topic ${TOPIC} --num-records $((1000*1024*1024/${i})) --record-size ${i} --throughput -1 --producer.config ${PROPERTIES}"
	echo $SCRIPT
	eval $SCRIPT
 	echo "----------------------------------------------------------------------------------------------------"
done;


