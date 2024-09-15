import FWCore.ParameterSet.Config as cms

pythiaUESettingsBlock = cms.PSet(
    pythiaUESettings = cms.vstring(
	'MSTU(21)=1     ! Check on possible errors during program execution', 
	'MSTJ(22)=2     ! Decay those unstable particles', 
	'PARJ(71)=10 .  ! for which ctau  10 mm', 
	'MSTP(33)=0     ! no K factors in hard cross sections', 
	'MSTP(2)=1      ! which order running alphaS', 
        'MSTP(51)=10042 ! structure function chosen (external PDF CTEQ6L1)',
        'MSTP(52)=2     ! work with LHAPDF',
        
	'PARP(82)=1.921 ! pt cutoff for multiparton interactions', 
	'PARP(89)=1800. ! sqrts for which PARP82 is set', 
	'PARP(90)=0.227 ! Multiple interactions: rescaling power', 
        
        'MSTP(95)=6     ! CR (color reconnection parameters)',
       	'PARP(77)=1.016 ! CR',
        'PARP(78)=0.538 ! CR',
        
	'PARP(80)=0.1   ! Prob. colored parton from BBR',
        
	'PARP(83)=0.356 ! Multiple interactions: matter distribution parameter', 
	'PARP(84)=0.651 ! Multiple interactions: matter distribution parameter', 
        
	'PARP(62)=1.025 ! ISR cutoff', 
        
	'MSTP(91)=1     ! Gaussian primordial kT', 
	'PARP(93)=10.0  ! primordial kT-max', 
        
	'MSTP(81)=21    ! multiple parton interactions 1 is Pythia default', 
	'MSTP(82)=4     ! Defines the multi-parton model', 
    )
)

generator = cms.EDFilter("Pythia6GeneratorFilter",
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         comEnergy = cms.double(7000.0),
                         PythiaParameters = cms.PSet(
                             pythiaUESettingsBlock,
                             processParameters = cms.vstring(
                                 'MSEL=0         ! User defined processes', 
                                 'MSUB(11)=1     ! Min bias process', 
                                 'MSUB(12)=1     ! Min bias process', 
                                 'MSUB(13)=1     ! Min bias process', 
                                 'MSUB(28)=1     ! Min bias process', 
                                 'MSUB(53)=1     ! Min bias process', 
                                 'MSUB(68)=1     ! Min bias process', 
                                 'MSUB(92)=1     ! Min bias process, single diffractive', 
                                 'MSUB(93)=1     ! Min bias process, single diffractive', 
                                 'MSUB(94)=1     ! Min bias process, double diffractive', 
                                 'MSUB(95)=1     ! Min bias process'),
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
                                 'pythiaUESettings', 
                                 'processParameters')
                         )
)

#partonfilter = cms.EDFilter("PythiaFilter",
#                            ParticleID = cms.untracked.int32(4) # 4 for prompt D0 and 5 for non-prompt D0
#)

D0filter = cms.EDFilter("PythiaMomDauFilter",
                        ParticleID = cms.untracked.int32(421),
                        DaughterIDs = cms.untracked.vint32(-321, 211),
                        ChargeConjugation = cms.untracked.bool(True),
                        MomMinPt = cms.untracked.double(0.),
                        NumberDaughters = cms.untracked.int32(2),
                        NumberDescendants = cms.untracked.int32(0),
                        
)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision$'),
    name = cms.untracked.string('$Source$'),
    annotation = cms.untracked.string('PYTHIA6-D0 pT0toInf noparton filter TuneZ2star at 7TeV 2010')
)

#ProductionFilterSequence = cms.Sequence(generator*partonfilter*D0filter)
ProductionFilterSequence = cms.Sequence(generator*D0filter)
