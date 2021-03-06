import FWCore.ParameterSet.Config as cms

#from RecoMET.METProducers.PFMET_cfi import pfMet
from JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff import *
from JetMETCorrections.Configuration.DefaultJEC_cff import *
##from RecoMET.METPUSubtraction.mvaPFMET_leptons_cfi import *
## CV: importing mvaPFMET_leptons_cfi breaks produceAndDiscriminateHPSPFTaus sequence
##    (hpsPFTauDiscriminationByDecayModeFinding module gets overwritten by None,
##     in case RecoTauTag/Configuration/python/RecoPFTauTag_cff.py is loaded by
##     by top-level cfg.py file before RecoMET/METPUSubtraction/python/mvaPFMET_cff.py gets loaded)
##from RecoJets.JetProducers.PileupJetIDCutParams_cfi import full_53x_wp

calibratedAK4PFJetsForPFMVAMEt = cms.EDProducer('PFJetCorrectionProducer',
    src = cms.InputTag('ak4PFJets'),
    correctors = cms.vstring("ak4PFL1FastL2L3") # NOTE: use "ak5PFL1FastL2L3" for MC / "ak5PFL1FastL2L3Residual" for Data
)

from RecoJets.JetProducers.pileupjetidproducer_cfi import pileupJetIdEvaluator
from RecoJets.JetProducers.PileupJetIDParams_cfi import JetIdParams
puJetIdForPFMVAMEt = pileupJetIdEvaluator.clone(
    algos = cms.VPSet(
        cms.PSet(
        tmvaVariables = cms.vstring(
            "nvtx",
            "jetPt",
            "jetEta",
            "jetPhi",
            "dZ",
            "beta",
            "betaStar",
            "nCharged",
            "nNeutrals",
            "dR2Mean",
            "ptD",
            "frac01",
            "frac02",
            "frac03",
            "frac04",
            "frac05"
            ),
        tmvaWeights = cms.string("RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_MET_53X_Dec2012.weights.xml.gz"),
        tmvaMethod = cms.string("JetID"),
        tmvaSpectators = cms.vstring(),
        JetIdParams = JetIdParams,                  
        impactParTkThreshold = cms.double(0.),
        version = cms.int32(-1),
        cutBased = cms.bool(False), 
        label = cms.string("full")
        )
        ),
    produceJetIds = cms.bool(True),
    runMvas = cms.bool(True),
    jets = cms.InputTag("calibratedAK4PFJetsForPFMVAMEt"),#calibratedAK4PFJetsForPFMVAMEt
    applyJec = cms.bool(True),
    inputIsCorrected = cms.bool(True),
    jec     = cms.string("AK4PF"),
)




pfMVAMEt = cms.EDProducer("PFMETProducerMVA",
    srcCorrJets = cms.InputTag('calibratedAK4PFJetsForPFMVAMEt'),
    srcUncorrJets = cms.InputTag('ak4PFJets'),
    srcMVAPileupJetId = cms.InputTag('puJetIdForPFMVAMEt','fullDiscriminant'),
    srcPFCandidates = cms.InputTag('particleFlow'),
    srcVertices = cms.InputTag('offlinePrimaryVertices'),
    srcLeptons = cms.VInputTag(),#"isomuons","isoelectrons","isotaus") # NOTE: you need to set this to collections of electrons, muons and tau-jets
                                 #                                             passing the lepton reconstruction & identification criteria applied in your analysis
    minNumLeptons = cms.int32(0),                     
    permuteLeptons = cms.bool(False),
    srcRho = cms.InputTag('fixedGridRhoFastjetAll'),
    globalThreshold = cms.double(-1.),#pfMet.globalThreshold,
    minCorrJetPt = cms.double(-1.),
    inputFileNames = cms.PSet(
        U     = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmet_53_Sep2013_type1.root'),
        DPhi  = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
        CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
        CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
          ),
    loadMVAfromDB = cms.bool(False),                             

    corrector = cms.string("ak4PFL1Fastjet"),
    useType1  = cms.bool(True), 
    dZcut     = cms.double(0.1),
       
    verbosity = cms.int32(0)
)



pfMVAMEtSequence  = cms.Sequence(
    #(isomuonseq+isotauseq+isoelectronseq)*
    calibratedAK4PFJetsForPFMVAMEt*
    puJetIdForPFMVAMEt*
    pfMVAMEt
)
