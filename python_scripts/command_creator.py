
if __name__ == '__main__':

    total_bytes = 500000000

    replication = [1, 2, 5]
    partirion = [1, 2, 5]
    message = [100, 500, 1000]

    batch = [16384, 100000, 500000]

    counter = 1
    for rf in replication:
        print("Open broker: {}".format(rf))
        for part in partirion:
            if partirion.index(part) is 0:
                if counter == (len(partirion)*len(message)*len(batch)*3*replication.index(rf) + 1) and counter != 1:
                    print("./bin/kafka-topics.sh --delete --zookeeper 195.134.67.93:2181 " 
                    "--topic test-part-5-rep-{} ; ".format(replication.index(rf)))
                print("./bin/kafka-topics.sh --create --zookeeper 195.134.67.93:2181 " 
                    "--topic test-part-1-rep-{} --partitions 1 --replication-factor {} ; ".format(rf, rf))
            elif partirion.index(part) is 1:
                print("./bin/kafka-topics.sh --delete --zookeeper 195.134.67.93:2181 " 
                    "--topic test-part-1-rep-{} ; ".format(rf))
                print("./bin/kafka-topics.sh --create --zookeeper 195.134.67.93:2181 " 
                    "--topic test-part-2-rep-{} --partitions 2 --replication-factor {} ; ".format(rf, rf))
            elif partirion.index(part) is 2:
                print("./bin/kafka-topics.sh --delete --zookeeper 195.134.67.93:2181 " 
                    "--topic test-part-2-rep-{} ; ".format(rf))
                print("./bin/kafka-topics.sh --create --zookeeper 195.134.67.93:2181 " 
                    "--topic test-part-5-rep-{} --partitions 5 --replication-factor {} ; ".format(rf, rf))
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