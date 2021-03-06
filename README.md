### Greyfish: portable cloud-based filesystem
Greyfish is a simple, out-of-the-box software for provisioning a multi-user, filesystem in the cloud. If you are building a web-application for which you need to support multiple users, having their personal space on a shared storage, then Greyfish can be useful in this scenario. It helps in creating a data "vault" with appropriate access privileges for the users. It provides the functionality for file-management - file/folder upload, file/folder download, and data persistence. It is built using Docker and currently runs as a single Docker container. However, shortly, we will release a distributed version of Greyfish such that it can leverage the storage space on multiple Virtual Machines (VMs) for load-balancing. The container technology helps in creating a portable service that can be started on or moved to any VM/system that supports Docker.


Greyfish is a WSGI application (powerd by a WSGI server), and uses multi-threading.

Data stored in Greyfish can be easily monitored/visualized using grafana or any other app.  

Greyfish provides single-use tokens for specifc actions. These tokens are stored within an attached Redis server on port 6379, and can be accessed, created, or deleted from  another server or container within the same machine.


#### Installation  

```bash
git clone https://github.com/noderod/greyfish
cd greyfish
# Change the influxdb log credentials
vi credentials.yml
# Set the appropriate passwords and base URL (without / and http(s)://
# Define the number of threads using "greyfish_threads", default is set to 4
REDIS_AUTH="examplepass" URL_BASE=example.com greyfish_key="examplegrey" docker-compose up -d
```


#### Instructions  

To activate or switch off the APIs, enter the docker container and do:  

```bash
# Enter container
docker exec -it greyfish_greyfish_1 bash
cd /grey
# Start the needed databases and assign permission (APIs will not be started)
/grey/setup.sh
# Activate (change the number of threads if needed, standard is 4)
./API_Daemon.sh -up
# Deactivate
./API_Daemon.sh -down
```

Note: deactivating the APIs will not change or delete any data, it will simply no longer be able to accept communications from outside.


**Partial installations**  

* Installation without Redis temporary tokens: Set *redis_command* to a different Linux command.
* Installation without InfluxDB logs: Set *influx_command* to a a different Linux command.

Note: Greyfish can be setup without Redis and InfluxDB.




#### Usage 

The Greyfish APIs can be called from any system as long as the greyfish key is known.  


```bash
	
gk=$Greyfish_Key # Set up in the docker-compose.yml

# Create a new user
curl http://$SERVER_IP:2003/grey/create_user/$gk/$USER_ID
# Delete a user
curl http://$SERVER_IP:2003/grey/delete_user/$gk/$USER_ID

# Get a JSON object of all user files
curl http://$SERVER_IP:2000/grey/all_user_files/$gk/$USER_ID
curl http://$SERVER_IP:2001/grey/all_user_files/$gk/$USER_ID

# Get contents of an entire directory in JSON (using ++ instead of / for paths)
curl http://$SERVER_IP:2000/grey/user_files/$gk/$USER_ID/PATH++TO++DIR
# Upload one file (will create the directory if needed
curl -F file=@$LOCAL_PATH_TO_FILE http://$SERVER_IP:2000/grey/upload/$gk/$USER_ID/PATH++TO++DIR
# Deletes a file
curl http://$SERVER_IP:2000/grey/delete_file/$gk/$USER_ID/$FILENAME/PATH++TO++DIR
# Deletes a directory (recursive)
curl http://$SERVER_IP:2000/grey/delete_dir/$gk/$USER_ID/PATH++TO++DIR
# Returns a file
curl http://$SERVER_IP:2000/grey/grey/$gk/$USER_ID/$FILENAME/PATH++TO++DIR
# Uploads a directory (must be compressed into .tgz or .tar.gz),
# if it already exists, it substitutes all files inside
curl -F file=@$LOCAL_PATH_TO_TAR http://$SERVER_IP:2000/grey/upload_dir/$gk/$USER_ID/PATH++TO++DIR
# Downloads a directory as a .tar.gz file
curl http://$SERVER_IP:2000/grey/grey_dir/$gk/$USER_ID/PATH++TO++DIR

# Gets all the data currently in the user directory
curl http://$SERVER_IP:2001/grey/get_all/$gk/$USER_ID
# Replaces all current data
curl -F file=@$TARRED_CONTENT  http://$SERVER_IP:2002/grey/push_all/$gk/$USER_ID

# Checksum actions
# Download a directory as a checksum file (first 8 characters of SHA256 checksum + tar.gz)
# This will move the tar file to a temporary checksum directory in case it needs to be checked later
# and delete the constituent directory files
# Both the -O and -J flags are required
curl -O -J http://$SERVER_IP:2000/grey/download_checksum_dir/$gk/$USER_ID/PATH++TO++DIR
# Or using wget:
wget --content-disposition http://$SERVER_IP:2000/grey/download_checksum_dir/$gk/$USER_ID/PATH++TO++DIR
# Delete a checksum file given its full name (i.e. FILENAME=y78t4jha.tar.gz) 
curl http://$SERVER_IP:2000/grey/delete_checksum_file/$gk/$USER_ID/$FILENAME


# Admin actions

# self_ID refers to how the admin wishes to refer to itself, useful in case of using temporary tokens
# Check all available usernames
curl -X POST -H "Content-Type: application/json" -d '{"key":"examplegrey", "self_ID":"admin1"}' http://$SERVER_IP:2004/grey/admin/users/usernames/all
# Purges all files older than Xsec seconds
curl -X POST -H "Content-Type: application/json" -d '{"key":"examplegrey", "self_ID":"admin1"}' http://$SERVER_IP:2004/grey/admin/purge/olderthan/$Xsec
``` 



#### Testing

The [speed-testing](./speed-testing) subdirectory contains a series of python scripts to test upload and download speeds for a Greyfish server.

#### Additional Notes
The docker-compose.yml file (https://github.com/ritua2/greyfish/blob/master/docker-compose.yml) has the specification for creating Docker volumes. These volumes help in persisting the data on the hard-disk even after the container is brought down. One volume is for the influxdb database for storing logs, and the other one is for saving users' data.


