#!/bin/bash

cfgfrag=$1

if [[ -z "$1" ]]; then
    echo "Please provide 1 argument"
    echo "Usage: ./CmsRun.sh <generated cfg file w/o .py>"
    echo "Eg.: ./CmsRun.sh MinB_TuneZ2star_7TeV_pythia6_cff_cfg_GEN"
    exit 1
fi
cmsRun -e -j ${cfgfrag}_rt.xml ${cfgfrag}.py || exit $? ; 
grep "TotalEvents" ${cfgfrag}_rt.xml
if [ $? -eq 0 ]; then
    grep "Timing-tstoragefile-write-totalMegabytes" ${cfgfrag}_rt.xml 
    if [ $? -eq 0 ]; then
        events=$(grep "TotalEvents" ${cfgfrag}_rt.xml | tail -1 | sed "s/.*>\(.*\)<.*/\1/")
        size=$(grep "Timing-tstoragefile-write-totalMegabytes" ${cfgfrag}_rt.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
        if [ $events -gt 0 ]; then
            echo "McM Size/event: $(bc -l <<< "scale=4; $size*1024 / $events")"
        fi
    fi
fi
grep "EventThroughput" ${cfgfrag}_rt.xml
if [ $? -eq 0 ]; then
  var1=$(grep "EventThroughput" ${cfgfrag}_rt.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
  echo "McM time_event value: $(bc -l <<< "scale=4; 1/$var1")"
fi
echo CPU efficiency info:
grep "TotalJobCPU" ${cfgfrag}_rt.xml
grep "TotalJobTime" ${cfgfrag}_rt.xml
