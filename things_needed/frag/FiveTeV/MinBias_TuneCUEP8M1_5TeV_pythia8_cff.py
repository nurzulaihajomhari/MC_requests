import FWCore.ParameterSet.Config as cms

# https://github.com/cms-sw/cmssw/blob/CMSSW_7_1_X/Configuration/Generator/python/Pythia8CommonSettings_cfi.py
# https://github.com/cms-sw/cmssw/blob/CMSSW_7_1_X/Configuration/Generator/python/Pythia8CUEP8M1Settings_cfi.py
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         comEnergy = cms.double(5020.0),
                         PythiaParameters = cms.PSet(
                             pythia8CommonSettingsBlock,
		             pythia8CUEP8M1SettingsBlock,
                             processParameters = cms.vstring(
                                 'SoftQCD:nonDiffractive = on',
                                 'SoftQCD:singleDiffractive = on',
                                 'SoftQCD:doubleDiffractive = on'),
                             # This is a vector of ParameterSet names to be read, in this order
                             parameterSets = cms.vstring(
                                 'pythia8CommonSettings',
                                 'pythia8CUEP8M1Settings',
                                 'processParameters')
                         )
)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision$'),
    name = cms.untracked.string('$Source$'),
    annotation = cms.untracked.string('PYTHIA8-MinBias TuneCUEP8M1 at 5TeV 2015')
)

ProductionFilterSequence = cms.Sequence(generator)
