#!/usr/bin/env python

import sys
import subprocess
import fileinput

if len(sys.argv) < 5:
    print "Usage: ./CmsDriv.py <genfragment w/o .py> <nevents> <1 for GEN, 2 for GEN-SIM> <COM, default 7TeV2010>"
    print "Eg.: ./CmsDriv.py MinB_TuneZ2star_7TeV_pythia6_cff 1000 1 7TeV2010"
    print "Do ls CMSSW_X_X_X/src/Configuration/GenProduction/python/XTeV/ for the fragment "
    exit(-1)
    
genfrag = sys.argv[1]
nev = sys.argv[2]
type = sys.argv[3]
COM = sys.argv[4]

# Ref: https://github.com/cms-sw/cmssw/blob/CMSSW_4_2_X/Configuration/AlCa/python/autoCond.py
# Ref: https://github.com/cms-sw/cmssw/blob/CMSSW_4_2_X/Configuration/StandardSequences/python/VtxSmeared.py
# This is for 7TeV2010 which is the default atm
globalTag = 'auto:startup'
#genDir = 'Configuration/GenProduction/python/7TeV/'
genDir = 'Configuration/GenProduction/python/SevenTeV/'
beamSpot = 'Realistic7TeVCollision'

# For other COM
if COM == '900GeV':
    globalTag = 'auto:startup'
    genDir = 'Configuration/GenProduction/python/NineHundredGeV/'
    beamspot = 'Realistic900GeVCollision'
if COM == '7TeV2011':
    globalTag = 'auto:startup'
    genDir = 'Configuration/GenProduction/python/SevenTeV/'
    beamSpot = 'Realistic7TeV2011Collision'
if COM == '8TeV2012':
    globalTag = 'auto:startup'
    genDir = 'Configuration/GenProduction/python/EightTeV/'
    beamSpot = 'Realistic8TeVCollision'
if COM == '5TeV2015':
    globalTag = 'auto:run2_mc'
    genDir = 'Configuration/GenProduction/python/FiveTeV/'
    beamSpot = 'Nominal5TeVpp2015Collision'
if COM == '13TeV2016':
    globalTag = 'auto:run2_mc'  #MCRUN2_71_V1::All auto:run2_mc
    genDir = 'Configuration/GenProduction/python/ThirteenTeV/'
    beamSpot = 'Realistic50ns13TeVCollision' #Not sure:Realistic50ns13TeVCollision or Realistic25ns13TeV2016Collision
    
if type == '1':
    subprocess.call('cmsDriver.py ' + genDir + genfrag + '.py --fileout file:' + genfrag + '_GEN.root --mc --conditions ' + globalTag + ' --eventcontent RAWSIM --datatier GEN-SIM-RAW --step GEN --python_filename ' + genfrag + '_cfg_GEN.py --customise Configuration/GenProduction/customise_SilentMessageLogger.customise --beamspot ' + beamSpot + ' --no_exec -n ' + nev, shell=True)
elif type == '2':
    subprocess.call('cmsDriver.py ' + genDir + genfrag + '.py --fileout file:' + genfrag + '_GEN-SIM.root --mc --conditions ' + globalTag + ' --eventcontent RAWSIM --datatier GEN-SIM --step GEN,SIM --python_filename ' + genfrag + '_cfg_GEN-SIM.py --customise Configuration/GenProduction/customise_SilentMessageLogger.customise,Configuration/DataProcessing/Utils.addMonitoring --beamspot ' + beamSpot + ' --no_exec -n ' + nev, shell=True)
else:
    print 'Wrong type specifier. Use 1 for GEN, 2 for GEN-SIM.'
    exit(-1)
