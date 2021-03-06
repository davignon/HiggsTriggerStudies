import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
process = cms.Process("TagAndProbe")

isMC = False
#isMC = True
#is2016 = True
is2016 = False

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

#### handling of cms line options for tier3 submission
#### the following are dummy defaults, so that one can normally use the config changing file list by hand etc.

options = VarParsing.VarParsing ('analysis')
options.register ('skipEvents',
                  -1, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Number of events to skip")
options.register ('JSONfile',
                  "", # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "JSON file (empty for no JSON)")
options.outputFile = 'NTuple_MC.root'
options.inputFiles = []
options.maxEvents  = -999
options.parseArguments()

if not isMC: # will use 80X
    from Configuration.AlCa.autoCond import autoCond
    #process.GlobalTag.globaltag = '80X_dataRun2_Prompt_v8'
    process.GlobalTag.globaltag = '92X_dataRun2_HLT_v7'
    process.load('HiggsTriggerStudies.VBFHinv.VBFMETNtuplizer_cff')
    #process.load('TauTagAndProbe.TauTagAndProbe.tagAndProbe_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            #'file:00080C61-E17E-E711-B88E-02163E01441B.root',
            'file:/data_CMS/cms/davignon/TauTagAndProbe_WithSeptember2017Calibrations/CMSSW_9_2_8/src/TauTagAndProbe/TauTagAndProbe/test/1A710040-BD7E-E711-A401-02163E011DE8.root',
            #'/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/282/092/00000/DE499C8E-1B8B-E611-8C93-02163E014207.root'
        ),
    )
else:
    process.GlobalTag.globaltag = '92X_upgrade2017_TSG_For90XSamples_V2' #MC 25 ns miniAODv2
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2' #MC 25 ns miniAODv2
    # process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'
    process.load('TauTagAndProbe.TauTagAndProbe.MCanalysis_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(            
            '/store/mc/PhaseIFall16MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/00000/182AC7D1-661B-E711-BA96-0242AC130006.root'
        )
    )

if is2016 and not isMC:
    process.patTriggerUnpacker.patTriggerObjectsStandAlone = cms.InputTag("selectedPatTrigger","","RECO")


if options.JSONfile:
    print "Using JSON: " , options.JSONfile
    process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
    process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.p = cms.Path(
    process.TAndPseq +
    process.NtupleSeq
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
