#!/bin/bash
echo $PATH
export PATH=/home/gwlin/anaconda2/bin:/home/gwlin/usr/local/jdk1.8.0_101/bin:/home/gwlin/usr/local/apache-ant-1.9.7/bin:/home/gwlin/anaconda2/bin:/home/gwlin/usr/local/jdk1.8.0_101/bin:/home/gwlin/usr/local/apache-ant-1.9.7/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/jdk1.7.0_45/bin:/usr/local/jdk1.7.0_45/jre/bin:/home/hadoop/hadoop-2.2.0/bin:/home/hadoop/hadoop-2.2.0/sbin
echo $PATH
TIMESTAMP=$(date -d "1 day ago" "+%Y%m%d")
#TIMESTAMP=20170317
QSS_JSON_FILE="data/qss-$TIMESTAMP.json"
BQS_JSON_FILE="data/bqs-$TIMESTAMP.json"
ALL_JSON_FILE="data/all-$TIMESTAMP.json"
QSS_WS_TYPE="qss"
BQS_WS_TYPE="bqsjds"
ALL_WS_TYPE="all"
QSS_DATA_DIR="data/qss_data/"
BQS_DATA_DIR="data/bqs_data/"
ALL_DATA_DIR="data/all_data/"

# args: ws_type, date, json_file_name, save_dir
function scratch_ws()
{
    if [ -f "$3" ]; then
        rm $3
    fi
    scrapy crawl -a ws_type=$1  zjxflws -o $3
    #scrapy crawl -a ws_type=$1 -a date=$2 zjxflws -o $3
    scrapy crawl -a json_path=$3 -a save_dir=$4 ws_details
}

function main()
{
    pushd `dirname $0` >/dev/null
    scratch_ws $QSS_WS_TYPE $TIMESTAMP $QSS_JSON_FILE $QSS_DATA_DIR
    scratch_ws $BQS_WS_TYPE $TIMESTAMP $BQS_JSON_FILE $BQS_DATA_DIR
    popd >/dev/null
}

main
