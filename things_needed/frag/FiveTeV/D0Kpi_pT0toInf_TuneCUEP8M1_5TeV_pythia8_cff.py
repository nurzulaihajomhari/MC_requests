import FWCore.ParameterSet.Config as cms

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
                             ExternalDecays = cms.PSet(
                                 EvtGen = cms.untracked.PSet(
                                     operates_on_particles = cms.vint32(0),
                                     use_default_decay = cms.untracked.bool(False),
                                     decay_table = cms.FileInPath('GeneratorInterface/ExternalDecays/data/DECAY_NOLONGLIFE.DEC'),
                                     #particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
                                     particle_property_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/evt.pdl'), #compatible with all CMSSW
                                     user_decay_embedded= cms.vstring(),
                                     user_decay_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/D0_Kpi.dec'),
                                     #list_forced_decays = cms.vstring('myD0','myanti-D0')
                                     list_forced_decays = cms.vstring()
                                 ),
                                 parameterSets = cms.vstring('EvtGen')
                             ),   
                             
                             # This is a vector of ParameterSet names to be read, in this order
                             parameterSets = cms.vstring(
                                 'pythia8CommonSettings',
                                 'pythia8CUEP8M1Settings',
                                 'processParameters')
                         )
)

#partonfilter = cms.EDFilter("PythiaFilter",
#                            ParticleID = cms.untracked.int32(4) # 4 for prompt D0 and 5 for non-prompt D0
#)

D0filter = cms.EDFilter("PythiaDauFilter",
                        ParticleID = cms.untracked.int32(421),
                        DaughterIDs = cms.untracked.vint32(-321, 211),
                        ChargeConjugation = cms.untracked.bool(True),
                        NumberDaughters = cms.untracked.int32(2)
)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision$'),
    name = cms.untracked.string('$Source$'),
    annotation = cms.untracked.string('PYTHIA8-D0 pT0toInf noparton filter TuneCUEP8M1 at 5TeV 2015')
)

#ProductionFilterSequence = cms.Sequence(generator*partonfilter*D0filter)
ProductionFilterSequence = cms.Sequence(generator*D0filter)
