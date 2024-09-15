#!/bin/bash

cmssw=$1
gcc=$2
genfrag=$3

toLogDir="Configuration/GenProduction/python/"
fromLogDir="/home/cms-opendata/GenPro/"
genDir="Configuration/GenProduction/python/SevenTeV/" #change to NineHundredGeV
#fragDir="/afs/desy.de/user/z/zulaiha/public/CMS/gen/frag/ref_frag/mein/finalize/7TeV/"
fragDir="/home/cms-opendata/GenPro/gen_frag/SevenTeV/" #change to NineHundredGeV
messageLog="customise_SilentMessageLogger.py"


if [[ -z "$3" ]]; then
    echo "Please provide 4 arguments"
    echo "Usage: source setup.sh <CMSSW> <gcc> <genfragment.py> <com>" 
    echo "Eg.: source setup.sh CMSSW_4_2_10_patch2 slc5_amd64_gcc434 MinB_TuneZ2star_7TeV_pythia6_cff.py"
    echo "Please do ls ${fragDir} for the list of fragments"
    echo "Please do scram list CMSSW_X for CMSSW release you want and gcc"
    return 1
fi
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=$gcc
if [ -r $cmssw/src ] ; then 
    echo "Release $1 already exists"
else
    echo "Creating CMSSW...."
    scram p CMSSW $cmssw
fi
cd $cmssw/src
eval `scram runtime -sh`

myDir=`pwd`
if [ -r $genDir ] ; then
    echo "$genDir directory is already exists"
else
    echo "$genDir directory is not yet exists"
    echo "Creating $genDir directory..."
    mkdir -p $genDir
    echo "Successfully created $genDir!"
fi
if [ -f $genDir/$3 ]; then
    echo "Fragment $3 is already exists in $genDir"
else
    echo "Fragment $3 is not yet exists in $genDir"
    echo "Copying the fragment...."
    cp $fragDir/$3 $myDir/$genDir
    if [ $? -eq 0 ]; then
	echo "Successfully copied $3"
    else
	echo "Could not copied $3"
	return 1
    fi    
fi
if [ -f $toLogDir/$messageLog ]; then
    echo "Message Logger is already exists"
else
    echo "MessageLogger is not yet exists"
    echo "Copying MessageLogger...."
    cp $fromLogDir/$messageLog $toLogDir
    if [ $? -eq 0 ]; then
	echo "Successfully copied $messageLog"
    else
	echo "Could not copied $messageLog"
	return 1
    fi
fi


echo "Compiling...."
scram b -j 8
if [ $? -eq 0 ]; then
    echo "Setup done!"
else
    echo "Errors in compiling"
fi

cd ../../
