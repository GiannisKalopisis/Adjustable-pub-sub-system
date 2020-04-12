import sys


total_bytes = 500000000
replication = [1, 2, 5]
partition = [1, 2, 5]
message = [100, 500, 1000]


parameterDict = {
    "batch.size": [16384, 50000, 100000, 200000, 500000],
    "buffer.memory": [10000000, 33554432, 100000000, 200000000, 500000000]
}


def printBrokers(from_broker, to_broker):
    print("\n\n##########################")
    print("# Open brokers from: {}-{} #".format(from_broker, to_broker))
    print("##########################\n")


def partitionCommands(previous_part, previous_rf, rf, part, first):

    if first:
        print("./bin/kafka-topics.sh --delete --zookeeper 195.134.67.93:2181 " 
            "--topic test-part-{}-rep-{} ; ".format(previous_part, previous_rf))
    else:
        print("./bin/kafka-topics.sh --delete --zookeeper 195.134.67.93:2181 " 
            "--topic test-part-{}-rep-{} ; ".format(previous_part, rf))
    print("./bin/kafka-topics.sh --create --zookeeper 195.134.67.93:2181 " 
        "--topic test-part-{}-rep-{} --partitions {} --replication-factor {} ; ".format(part, rf, part, rf))


def parameterChange(parameter, size, config_type, rf):
    print("python3 ../python_scripts/change_parameter.py {}={} " 
        "../test_properties_files/{}_properties/{}-{}.properties ; ".format(parameter, size, config_type, config_type,rf))


def kafkaCommand(part, rf, record_num, mes_size, counter, measurement_size):
    print("./bin/kafka-producer-perf-test.sh "
        "--topic test-part-{}-rep-{} "
        "--num-records {} --record-size {} --throughput -1 "
        "--producer.config ../test_properties_files/producer_properties/producer-{}.properties "
        "> ../python_scripts/metrics_folder/{:04d}_{}_{}_{}_{} ; "\
        .format(part, rf, record_num, mes_size, rf, counter, rf, part, mes_size, measurement_size))


#measurement_type = "batch.size"
#parameter_type = "producer/server"
def printCommands(parameter_list, measurement_type , parameter_type):

    parameter = parameter_list

    counter = 1
    for rf in replication:
        printBrokers(replication[0], rf)
        for part in partition:
            if counter == (len(replication)*len(partition)*len(message)*len(parameter)*replication.index(rf) + 1):
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, True)
            else:
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, False)
            for mes in message:
                for par in parameter:
                    parameterChange(measurement_type, par, parameter_type, rf)
                    for i in range(1,4):
                        kafkaCommand(part, rf, int(total_bytes/mes), mes, counter, par)
                        counter += 1


def bufferMemory():
    print("buffer.memory is not implemented yet.")


def wrongArgumentsFunc():
    print("Couldn't match your input parameter to any test case.")
    print("Test cases are:  1) batch.size")
    print("                 2) buffer.memory")

def noArgumentsFunc():
    print("Error while trying to run command_creator.py. Not enough parameters.")
    print("Example: $python3 command_creator.py 'parameter'")


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        noArgumentsFunc()
        sys.exit(1)

    test_parameter = sys.argv[1]

    if test_parameter == "batch.size":
        printCommands(parameterDict["batch.size"], "batch.size", "producer")
    elif test_parameter == "buffer.memory":
        printCommands(parameterDict["buffer.memory"], "buffer.memory", "producer")
    else:
        wrongArgumentsFunc()
    