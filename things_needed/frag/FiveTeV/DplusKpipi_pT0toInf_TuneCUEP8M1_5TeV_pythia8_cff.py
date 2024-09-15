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
                                     user_decay_embedded= cms.vstring(
"""
# This is the decay file for the decay D+ -> Kaon pion pion
Alias myD+      D+
Alias myD-      D-
ChargeConj myD- myD+
#
Decay myD+
  1.00 K-      pi+     pi+                             PHSP; #[Reconstructed PDG2011]
Enddecay
CDecay myD-
#
End
"""
),
                                     #in principle, want D+->K-pi+pi+ including intermediate resonances, but hard to implement
                                     #thus settle for D+->K-pi+pi+ direct decays (lower branching fraction!)
                                     #user_decay_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/Dplus_Kpipi.dec'),
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

Dplusfilter = cms.EDFilter("PythiaDauFilter",
                        ParticleID = cms.untracked.int32(411),
                        DaughterIDs = cms.untracked.vint32(-321, 211, 211),
                        ChargeConjugation = cms.untracked.bool(True),
                        NumberDaughters = cms.untracked.int32(3)
)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision$'),
    name = cms.untracked.string('$Source$'),
    annotation = cms.untracked.string('PYTHIA8-Dplus pT0toInf noparton filter TuneCUEP8M1 at 5TeV 2015')
)

#ProductionFilterSequence = cms.Sequence(generator*partonfilter*Dplusfilter)
ProductionFilterSequence = cms.Sequence(generator*Dplusfilter)
