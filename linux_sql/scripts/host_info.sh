#!/bin/bash

psql_host=$1
psql_port=$2
db_name=$3
psql_user=$4
psql_password=$5

# Check # of args
if [ "$#" -ne 5 ]; then
  echo "Illegal number of parameters"
  exit 1
fi

hostname=$(hostname -f)
lscpu=$(lscpu)
meminfo=$(cat /proc/meminfo)

cpu_number=$(echo "$lscpu" | awk -F: '/^CPU\(s\)/{gsub(/ /,"",$2); print $2}')
cpu_architecture=$(echo "$lscpu" | awk -F: '/^Architecture/{gsub(/ /,"",$2); print $2}')
cpu_model=$(echo "$lscpu" | awk -F: '/^Model name/{gsub(/^[ \t]+/,"",$2); print $2}')
cpu_mhz=$(echo "$lscpu" | awk -F: '/^CPU MHz/ {gsub(/^[ \t]+/,"",$2); print $2}')
cpu_mhz=${cpu_mhz:-0}
l2_cache=$(echo "$lscpu" | awk -F: '/^L2 cache/ {gsub(/[^0-9]/,"",$2); print $2}')
total_mem=$(echo "$meminfo" | awk '/^MemTotal/ {print $2}')
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

insert_stmt="
INSERT INTO host_info(
  hostname,
  cpu_number,
  cpu_architecture,
  cpu_model,
  cpu_mhz,
  l2_cache,
  total_mem,
  \"timestamp\"
)
VALUES (
  '$hostname',
  $cpu_number,
  '$cpu_architecture',
  '$cpu_model',
  $cpu_mhz,
  $l2_cache,
  $total_mem,
  '$timestamp'
);
"

export PGPASSWORD=$psql_password 
psql -h $psql_host -p $psql_port -d $db_name -U $psql_user -c "$insert_stmt" 
exit $?
