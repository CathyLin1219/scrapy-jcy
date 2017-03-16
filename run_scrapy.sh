#!/bin/bash

TIMESTAMP=$(date -d "1 day ago" "+%Y%m%d")
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
    scrapy crawl -a ws_type=$1 -a date=$2 zjxflws -o $3
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