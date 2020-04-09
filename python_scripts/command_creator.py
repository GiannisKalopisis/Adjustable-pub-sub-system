
import sys

def batchSize():

    total_bytes = 500000000

    replication = [1, 2, 5]
    partition = [1, 2, 5]
    message = [100, 500, 1000]

    batch = [16384, 50000, 100000, 200000, 500000]

    counter = 1
    for rf in replication:
        print("\n\n##########################")
        print("# Open brokers from: {}-{} #".format(replication[0], rf))
        print("##########################\n")
        for part in partition:
            if counter == (len(replication)*len(partition)*len(message)*len(batch)*replication.index(rf) + 1):
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, True)
            else:
                partitionCommands(partition[partition.index(part) - 1], replication[replication.index(rf) - 1], rf, part, False)
            for mes in message:
                for b in batch:
                    print("python3 ../python_scripts/change_parameter.py batch.size={} " 
                    "../test_properties_files/producer_properties/producer-{}.properties ; ".format(b, rf))
                    for i in range(1,4):
                        print("./bin/kafka-producer-perf-test.sh "
                            "--topic test-part-{}-rep-{} "
                            "--num-records {} --record-size {} --throughput -1 "
                            "--producer.config ../test_properties_files/producer_properties/producer-{}.properties "
                            "> ../python_scripts/metrics_folder/{:04d}_{}_{}_{}_{} ; "\
                            .format(part, rf, int(total_bytes/mes), mes, rf, counter, rf, part, mes, b))
                        counter += 1




def partitionCommands(previous_part, previous_rf, rf, part, first):

    if first:
        print("./bin/kafka-topics.sh --delete --zookeeper 195.134.67.93:2181 " 
            "--topic test-part-{}-rep-{} ; ".format(previous_part, previous_rf))
    else:
        print("./bin/kafka-topics.sh --delete --zookeeper 195.134.67.93:2181 " 
            "--topic test-part-{}-rep-{} ; ".format(previous_part, rf))
    print("./bin/kafka-topics.sh --create --zookeeper 195.134.67.93:2181 " 
        "--topic test-part-{}-rep-{} --partitions {} --replication-factor {} ; ".format(part, rf, part, rf))


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
        batchSize()
    elif test_parameter == "buffer.memory":
        bufferMemory()
    else:
        wrongArgumentsFunc()
    