# Start Mesosphere with atleast 5 slaves required for HDFS 

# Run HDFS inside

```dcos package install hdfs```

# Run marathon-lb inside

```dcos package install marathon-lb```

# UK Traffic Statistic

## Put UK data to hdfs

Launch task in marathon with ```dcos marathon app add uk-data-upload.json```

uk-data-upload.json:

```json
{
      "id": "/uk-data-to-hdfs",
      "instances": 1,
      "cmd": "apt-get update && 
      apt-get install -y unzip && 
      curl -O http://data.dft.gov.uk/road-accidents-safety-data/Stats19-Data1979-2004.zip && 
      unzip -d . Stats19-Data1979-2004.zip Accidents7904.csv && 
      curl -O http://hdfs.marathon.mesos:$(host -t SRV _hdfs._tcp.marathon.mesos | cut -f 7 -d' ')/core-site.xml
cp core-site.xml /conf/core-site.xml && 
      bin/hadoop fs -put Accidents7904.csv hdfs://hdfs/ && 
      curl -X DELETE http://marathon.mesos:8080/v2/apps/uk-data-to-hdfs",
      "cpus": 0.5,
      "mem": 512,
      "container": {
            "type": "DOCKER",
            "docker": {
              "image": "pintostack/hdfs",
      			  "forcePullImage": false,
      			  "network": "BRIDGE",
      			  "privileged": false
            }
      }
}
```

Now ```Accidents7904.csv``` data available on HDFS

## Run Jupiter notebook

Launch task in marathon with ```dcos marathon app add dcos-jupiter.json```

```json
{
    "id": "/jupiter/all-spark-notebook",
    "cpus": 0.5,
    "mem": 1024,
    "requirePorts": true,
    "instances": 1,
    "ports": [ 8888 ],
    "cmd": "/usr/local/bin/start-notebook.sh",
    "container": {
        "type": "DOCKER",
        "docker": {
            "image": "pytnru/all-spark-notebook",
            "forcePullImage": false,
            "network": "HOST",
            "privileged": false,
            "parameters": [
                { "key": "volume", "value": "/opt/mesosphere/:/opt/mesosphere/" }
            ]
        }
    },
    "env":{
"TINI_SUBREAPER": "true",
"PYTHONHASHSEED": "0",
"PYTHONUNBUFFERED":"true",
"PATH": "/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/mesosphere/bin/",
"JAVA_HOME": "/opt/mesosphere/active/java/",
"MESOS_NATIVE_JAVA_LIBRARY": "/opt/mesosphere/lib/libmesos.so",
"MESOS_NATIVE_LIBRARY": "/opt/mesosphere/lib/libmesos.so",
"HDFS_MESOS_CONFIG_PATH": "/opt/mesosphere/etc/hadoop/hdfs-site.xml",
"PYSPARK_PYTHON": "python3",
"PYSPARK_SUBMIT_ARGS": " --master mesos://master.mesos:5050 --conf spark.executor.uri=http://tc.pytn.ru/spark-1.6.1-bin-hadoop2.6.tgz"
    },
    "constraints": [["hostname", "LIKE", "10.0.3.253"]],
    "healthChecks": [
        {
      "protocol": "HTTP",
      "path": "/",
      "portIndex": 0,
      "timeoutSeconds": 10,
      "gracePeriodSeconds": 10,
      "intervalSeconds": 2,
      "maxConsecutiveFailures": 10
        }
    ],
    "labels":{
    "HAPROXY_GROUP":"external"
    }
}
```

## Publish Jupiter port to outside

Launch marathon-ld with ```dcos package install marathon-lb```

Open in browser ```<public-ip>:9090/haproxy?stats```

> INFO: You can find marathon-lb public IP in AWS Console - the host with PublicSlaveSecurityGroup

## Run Example

* Wait while ```jupiter_all-spark-notebook_8888``` in marathon-lb ```<public-ip>:9090/haproxy?stats``` becomes active, it can take up to 10 minutes. 

* Open ```<marathon-lb-public-ip>:8888```

* Create new Python 3 notebook

* Past the example below and run it


```python
import time

start_time = int(round(time.time() * 1000))

# now we have a file
text_file = sc.textFile("hdfs://namenode2.hdfs.mesos:50071/Accidents7904.csv")

# getting the header as an array
header = text_file.first().split(",")

# getting data
data = text_file \
   .map(lambda line: line.split(",")) \
   .filter(lambda w: w[header.index('Date')] != 'Date')
output = data.filter(lambda row: len(row[header.index('Date')].strip().split("/")) == 3) \
   .map(lambda row: (row[header.index('Speed_limit')].strip(), row[header.index('Date')].strip().split("/")[2])) \
   .filter(lambda sl: sl[0] == '50' or sl[0] == '70') \
   .map(lambda x: (x , 1)) \
   .reduceByKey(lambda a, b: a + b) \
   .sortByKey(True) \
   .collect()
for (line, count) in output:
        print("%s: %i" % (line, count))
print ("Duration is '%i' ms" % (int(round(time.time() * 1000)) - start_time))

```


