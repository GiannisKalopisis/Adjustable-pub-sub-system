import sys


total_bytes = 500000000
replication = [1, 2, 5]
partition = [1, 2, 5]
message = [100, 500, 1000]


parameterDict = {
    "batch.size": [16384, 50000, 100000, 200000, 500000],
    "buffer.memory": [10000000, 33554432, 100000000, 200000000],
    "linger.ms": [0, 1, 2, 5, 10],
    "max.request.size": [500000, 1048576, 2000000, 5000000, 10000000],
    "message.size": [10, 20, 50, 100, 200, 500, 1000]
}


smallerParameterDict = {
    "batch.size": [16384, 200000, 500000],
    "buffer.memory": [33554432, 100000000, 200000000],
    "linger.ms": [0, 2, 5],
    "max.request.size": [1048576, 5000000, 10000000]
    # "message.size": [10, 20, 50, 100, 200, 500, 1000]
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


def kafkaCommand(part, rf, record_num, mes_size, counter, measurement_size_1, measurement_size_2, folder, is_message_size, multiple):
    # 2 parameters testing
    if multiple:
        print("./bin/kafka-producer-perf-test.sh "
            "--topic test-part-{}-rep-{} "
            "--num-records {} --record-size {} --throughput -1 "
            "--producer.config ../test_properties_files/producer_properties/producer-{}.properties "
            "> {}/{:04d}_{}_{}_{}_{}_{} ; "\
            .format(part, rf, record_num, mes_size, rf, folder, counter, rf, part, mes_size, measurement_size_1, measurement_size_2))
        return

    # 1 parameter testing
    if not is_message_size:
        print("./bin/kafka-producer-perf-test.sh "
            "--topic test-part-{}-rep-{} "
            "--num-records {} --record-size {} --throughput -1 "
            "--producer.config ../test_properties_files/producer_properties/producer-{}.properties "
            "> {}/{:04d}_{}_{}_{}_{} ; "\
            .format(part, rf, record_num, mes_size, rf, folder, counter, rf, part, mes_size, measurement_size_1))
    # message size testing
    else:
        print("./bin/kafka-producer-perf-test.sh "
            "--topic test-part-{}-rep-{} "
            "--num-records {} --record-size {} --throughput -1 "
            "--producer.config ../test_properties_files/producer_properties/producer-{}.properties "
            "> {}/{:04d}_{}_{}_{} ; "\
            .format(part, rf, record_num, mes_size, rf, folder, counter, rf, part, mes_size))


def wrongArgumentsFunc():
    print("Couldn't match your input parameter to any test case.")
    print("Test cases are:  1) batch.size")
    print("                 2) buffer.memory")
    print("                 3) linger.ms")
    print("                 4) max.request.size")
    print("                 5) message.size")
    print("Multiple parameters: combination of previous parameters (2 parameters)\n")


def printUsage():
    print("Single parameter: python3 command_creator.py <parameter> folder")
    print("Multiple parameters: python3 command_creator.py -m <parameter1+parameter2> folder")


def noArgumentsFunc():
    print("Error while trying to run command_creator.py. Not enough parameters.")
    print("Example: $python3 command_creator.py 'parameter' 'folder'")


#measurement_type = "batch.size"
#parameter_type = "producer/server"
def printCommands(parameter_list, measurement_type , parameter_type, folder, is_message_size):

    parameter = parameter_list

    counter = 1
    for rf in replication:
        printBrokers(replication[0], rf)
        for part in partition:
            if counter == (len(replication)*len(partition)*len(message)*len(parameter)*replication.index(rf) + 1):
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, True)
            else:
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, False)
            # not message size, needs to change parameter to check
            if not is_message_size:
                counter = singleParameters(parameter, measurement_type, parameter_type, rf, part, counter, folder, is_message_size)
            # message size is the parameter we check
            else:
                counter = messageSizeParameter(parameter, part, rf, counter, folder, is_message_size)


# commands for testing message.size parameter
# message is parameter
def messageSizeParameter(parameter, part, rf, counter, folder, is_message_size):
    for mes in parameter:
        for i in range(1,4):
            kafkaCommand(part, rf, int(total_bytes/mes), mes, counter, None, None, folder, is_message_size, False)
            counter += 1
    return counter


# commands for testing single parameters, except message.size
def singleParameters(parameter, measurement_type, parameter_type, rf, part, counter, folder, is_message_size):
    for mes in message:    
        for par in parameter:
            parameterChange(measurement_type, par, parameter_type, rf)
            for i in range(1,4):
                kafkaCommand(part, rf, int(total_bytes/mes), mes, counter, par, None, folder, is_message_size, False)
                counter += 1
    return counter


#measurement_type = parameter1 + parameter2 
#parameter_type = "producer/server"
def multipleParametersPrintCommands(first_parameter_list, second_parameter_list, first_measurement_type, second_measurement_type, parameter_type, folder):

    first_parameter = first_parameter_list
    second_parameter = second_parameter_list

    counter = 1
    for rf in replication:
        printBrokers(replication[0], rf)
        for part in partition:
            if counter == (len(replication)*len(partition)*len(message)*len(first_parameter)*len(second_parameter)*replication.index(rf) + 1):
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, True)
            else:
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, False)
            counter = twoParameters(first_parameter, second_parameter, first_measurement_type, second_measurement_type, parameter_type, rf, part, counter, folder)


def twoParameters(first_parameter, second_parameter, first_measurement_type, second_measurement_type, parameter_type, rf, part, counter, folder):
    for mes in message:    
        for par1 in first_parameter:
            parameterChange(first_measurement_type, par1, parameter_type, rf)
            for par2 in second_parameter:
                parameterChange(second_measurement_type, par2, parameter_type, rf)
                for i in range(1,4):
                    kafkaCommand(part, rf, int(total_bytes/mes), mes, counter, par1, par2, folder, False, True)
                    counter += 1
    return counter


def removeLastBackslash(folder):
    if folder[-1] == '/':
        folder = folder[:-1]
    return folder


def checkParametersExistence(parameters):
    for param in parameters:
        if not param in smallerParameterDict:
            print("Error at multiple parameters.")
            wrongArgumentsFunc()
            sys.exit()


if __name__ == '__main__':

    #
    # Parameters for single variable:   1) test_parameter
    #                                   2) folder
    #
    # Parameters for multiple variables: 1) -m
    #                                    2) test_parameter
    #                                    3) folder
    #

    if len(sys.argv) <= 2:
        noArgumentsFunc()
        sys.exit(1)

    test_parameter = sys.argv[1]

    if test_parameter in parameterDict:
        printCommands(parameterDict[test_parameter], test_parameter, "producer", removeLastBackslash(sys.argv[2]), test_parameter == "message.size")
    elif test_parameter == "-m":
        parameters = sys.argv[2].split('+')
        checkParametersExistence(parameters)
        multipleParametersPrintCommands(smallerParameterDict[parameters[0]], smallerParameterDict[parameters[1]], parameters[0], parameters[1], "producer", removeLastBackslash(sys.argv[3]))
    else:
        wrongArgumentsFunc()
        printUsage()
    
