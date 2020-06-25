#!/usr/bin/env python
# -*-coding:Latin-1 -*
from math import *
import sys
import ROOT
import ROOT as root
from   ROOT import TFile, gSystem, TGraph
import libPyROOT

import yaml
from   source.PlotsClass  import *
from   source.Chi2Fit     import *
from   source.LatexTable  import *
from   source.source	  import *


with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile)

# read config file:
print("")
print("************ read config file ************")
print("")
print("MASSSTEPS       : %s" %cfg['MASSSTEPS'])
print("Wminusenu_MCFile: %s" %cfg['Wminusenu_MCFile'])
print("")

# read MC file:
print("")
print("************ read Input files ************")
print("")
MCWminusenu5     = root.TFile(cfg['Wminusenu_MCFile'])			
MCWminusenu5B    = root.TFile(cfg['Wminusenu_MC_B_File'])
DataWminusenu5   = root.TFile(cfg['Wminusenu_DataFile'])
DataWminusenu5B  = root.TFile(cfg['Wminusenu_Data_B_File'])
MCWminusmunu5    = root.TFile(cfg['Wminusmunu_MCFile'])
MCWminusmunu5B   = root.TFile(cfg['Wminusmunu_MC_B_File'])
DataWminusmunu5  = root.TFile(cfg['Wminusmunu_DataFile'])
DataWminusmunu5B = root.TFile(cfg['Wminusmunu_Data_B_File'])
MCWplusenu5      = root.TFile(cfg['Wplusenu_MCFile'])
MCWplusenu5B     = root.TFile(cfg['Wplusenu_MC_B_File'])
DataWplusenu5    = root.TFile(cfg['Wplusenu_DataFile'])
DataWplusenu5B   = root.TFile(cfg['Wplusenu_Data_B_File'])
MCWplusmunu5     = root.TFile(cfg['Wplusmunu_MCFile'])
MCWplusmunu5B    = root.TFile(cfg['Wplusmunu_MC_B_File'])
DataWplusmunu5   = root.TFile(cfg['Wplusmunu_DataFile'])
DataWplusmunu5B  = root.TFile(cfg['Wplusmunu_Data_B_File'])
print("Done")

# read MC file:
print("")
print("************ Creat List For DAta and MC ************")
print("")
MC5TeV    = []
MC5TeVB   = [] 
DATA5TeV  = []
DATA5TeVB = []

MC5TeV.append(MCWminusenu5)
MC5TeV.append(MCWplusenu5)
MC5TeV.append(MCWminusmunu5)
MC5TeV.append(MCWplusmunu5)

MC5TeVB.append(MCWminusenu5B)
MC5TeVB.append(MCWplusenu5B)
MC5TeVB.append(MCWminusmunu5B) 
MC5TeVB.append(MCWplusmunu5B)

DATA5TeV.append(DataWminusenu5)
DATA5TeV.append(DataWplusenu5)
DATA5TeV.append(DataWminusmunu5)
DATA5TeV.append(DataWplusmunu5)

DATA5TeVB.append(DataWminusenu5B)
DATA5TeVB.append(DataWplusenu5B)
DATA5TeVB.append(DataWminusmunu5B)
DATA5TeVB.append(DataWplusmunu5B)
print("Done")
print("***************************************************")

#Unf_MC = root.TFile(cfg['Wminusenu_Unfolded'])

channel      = ["Wminusenu", "Wplusenu", "Wminusmunu", "Wplusmunu"]
MassSteps    = cfg['MASSSTEPS']
indice 	     = ["","_eta1", "_eta2", "_eta3", "_eta4"]
Variable     = ["mT", "elPt"]
kindice      = 0
MwNominal    = 80400

#*******************************************************************************************************
# Calculate the W mass using Unfolded distribution of Data:
#*******************************************************************************************************
'''
DataNominal     = ReadNominalDistribution( DATA5TeV[0],   channel[0], Variable[1], indice[0]	)
MCNominal       = ReadNominalDistribution( MC5TeV[0],     channel[0], Variable[1], indice[0]	)
MCTemplates     = ReadMCTemplate(          MC5TeV[0],     channel[0], Variable[1], indice[0]	)
MCTemplatesFin  = AddNominalDistributionToTemplates(  MCTemplates, MCNominal		    	)

Nomresult       = fitmW(  	    MCTemplatesFin, MassSteps, MCNominal,   MwNominal		)
Nomresult       = Chi2Calculation(  MCTemplatesFin, MassSteps, MCNominal,   MwNominal, 0, 100	)
Nomresult       = fitmW(  	    MCTemplatesFin, MassSteps, DataNominal, MwNominal		)
Nomresult       = Chi2Calculation(  MCTemplatesFin, MassSteps, DataNominal, MwNominal, 0, 100	)
'''
'''
TableDATAmT  = []
TableDATAlpT = []

for i in range(0, len(MC5TeV)):
    if(channel[i].find("munu") != -1):
	print(channel[i])
for i in range(0, len(MC5TeV)):
    for j in range(0, len(indice)):
    	DataNominal  = ReadNominalDistribution( DATA5TeV[i],   channel[i], Variable[0], indice[j])
    	MCNominal    = ReadNominalDistribution( MC5TeV[i],     channel[i], Variable[0], indice[j])
    	MCTemplates  = ReadMCTemplate( 	    	MC5TeV[i],     channel[i], Variable[0], indice[j])
    	MCTemplates  = AddNominalDistribution(MCTemplates, MCNominal)
    	Nomresult    = fitmW(MCTemplates, MassSteps, DataNominal, MwNominal)
    	TableDATAmT.append(Nomresult[1])

for i in range(0, len(MC5TeV)):
    for j in range(0, len(indice)):
        if(channel[i].find("munu") != -1): Variable[1] = "muPt"
        if(channel[i].find("enu") != -1):  Variable[1] = "elPt"
	print(i, j, channel[i], DATA5TeV[i], Variable[1])
    	DataNominal  = ReadNominalDistribution( DATA5TeV[i],   channel[i], Variable[1], indice[j])
    	MCNominal    = ReadNominalDistribution( MC5TeV[i],     channel[i], Variable[1], indice[j])
    	MCTemplates  = ReadMCTemplate(          MC5TeV[i],     channel[i], Variable[1], indice[j])
    	MCTemplates  = AddNominalDistribution(MCTemplates, MCNominal)
    	Nomresult    = fitmW(MCTemplates, MassSteps, DataNominal, MwNominal)
    	TableDATAlpT.append(Nomresult[1])

print(TableDATAlpT)
print(TableDATAmT)
TableListMC(TableDATAlpT, TableDATAmT, channel[0], "$W^{-}\\rightarrow e^{-}\\nu,   5TeV$")
'''

#*******************************************************************************************************
# define the correlation between pt(l) and mT(w) Using MC
#*******************************************************************************************************

# calculate the vector of Mw from toys of pT(l) and mT(W):

plTMwToys   = MwToys(MC5TeV[0],  MC5TeVB[0], channel[0], Variable[1], MassSteps, indice[0], MwNominal)
#mTMwToys    = MwToys(MC5TeV[1],  MC5TeVB[1], channel[1], Variable[0], MassSteps, indice[0], MwNominal)
#graph       = GraphPloting(plTMwToys, mTMwToys)
#Corr        = CorrelationCoefficient(plTMwToys, mTMwToys)

'''
Variable       = "elPt"
pTlMwToys      = MwToys(MC, MC_B, channel, Variable, MassSteps, indice[0], MwNominal)

#define the graph
graph       = GraphPloting(pTlMwToys, mTMwToys)
Corr        = CorrelationCoefficient(pTlMwToys, mTMwToys)

# Save the graph in output 
Output = ROOT.TFile.Open("Output.root","RECREATE")
graph.Write("graph")
'''


#*******************************************************************************************************
# Calculate the W mass using Unfolded MC:
#*******************************************************************************************************
'''
Variable     = "mT"
itera 	     = 1

# read unfolded MC
UnfolMCNominal  = ReadUnfoldeddistribution( Unf_MC, itera)

# Read the unfolded Templates:
UnfoMCTemplates = ReadMCUnfoldedTemplate( Unf_MC, itera)

# define the fit:
Nomresult    = fitmW(UnfoMCTemplates, MassSteps, UnfolMCNominal, MwNominal)
'''

'''
#*******************************************************************************************************
# Calculate the ID systematics:
#*******************************************************************************************************
IdVariations = getHistVariations(MCID, channel, indice[kindice])
IdVarNominal = ReadMCFiles(MCID, channel, indice[kindice])

# Add nominal hist to templates:
for i in range(0, len(IdVariations) ):
    IdVariations[i].Add(IdVarNominal)

# Get the Systematics:
IdVariation  = GetSystematicVariations(IdVariations, MCTemplates, MassSteps, Nomresult[0], MwNominal)
IdSystematic = 0
for i in range(0, len(IdVariation)):
    IdSystematic = IdSystematic + IdVariation[i]*IdVariation[i]


#*******************************************************************************************************
# Calculate the reco systematics:
#*******************************************************************************************************
recoVariations = getHistVariations(MCRe, channel, indice[kindice])
recoVarNominal = ReadMCFiles(MCRe, channel, indice[kindice])

# Add nominal hist to templates:
for i in range(0, len(recoVariations) ):
    recoVariations[i].Add(recoVarNominal)

# Get the Systematics:
recoVariation  = GetSystematicVariations(recoVariations, MCTemplates, MassSteps, Nomresult[0], MwNominal)
recoSystematic = 0
for i in range(0, len(recoVariation)):
    recoSystematic = recoSystematic + recoVariation[i]*recoVariation[i]


#*******************************************************************************************************
# Calculate the iso systematics:
#*******************************************************************************************************
isoVariations = getHistVariations(MCIs, channel, indice[kindice])
isoVarNominal = ReadMCFiles(MCIs, channel, indice[kindice])

# Add nominal hist to templates:
for i in range(0, len(isoVariations) ):
    isoVariations[i].Add(isoVarNominal)

# Get the Systematics:
isoVariation  = GetSystematicVariations(isoVariations, MCTemplates, MassSteps, Nomresult[0], MwNominal)
isoSystematic = 0
for i in range(0, len(isoVariation)):
    isoSystematic = isoSystematic + isoVariation[i]*isoVariation[i]


#*******************************************************************************************************
# Calculate the Trigger systematics:
#*******************************************************************************************************
triggerVariations = getHistVariations(MCTr, channel, indice[kindice])
triggerVarNominal = ReadMCFiles(MCTr, channel, indice[kindice])

# Add nominal hist to templates:
for i in range(0, len(triggerVariations) ):
    triggerVariations[i].Add(triggerVarNominal)

# Get the Systematics:
triggerVariation  = GetSystematicVariations(triggerVariations, MCTemplates, MassSteps, Nomresult[0], MwNominal)
triggerSystematic = 0
for i in range(0, len(triggerVariation)):
    triggerSystematic = triggerSystematic + triggerVariation[i]*triggerVariation[i]


#*******************************************************************************************************
# Calculate the calibration systematics:
#*******************************************************************************************************

CalibSyst1  = open('SystematicVariations/ElCalibVariations/Calib_Variation_Wminusenu5_Alpha.list','r') 
CalibTotal1 = 0

for line in CalibSyst1.readlines():
    Calibroot    =  ROOT.TFile.Open(line.strip(),'read')
    MCNominal    =  ReadMCFiles(Calibroot, channel, indice[kindice])
    MCTemplates  =  ReadMCTemplate(Calibroot, channel, indice[kindice])
    Calibresult  =  fitmW(MCTemplates, MassSteps, MCNominal, MwNominal)
    CalibTotal1  =  CalibTotal1 + (Calibresult[0]**2 - Nomresult[0]**2)
    

CalibSyst2  = open('SystematicVariations/ElCalibVariations/Calib_Variation_Wminusenu5_C.list','r')
CalibTotal2 = 0

for line in CalibSyst2.readlines():
    Calibroot    =  ROOT.TFile.Open(line.strip(),'read')
    MCNominal    =  ReadMCFiles(Calibroot, channel, indice[kindice])
    MCTemplates  =  ReadMCTemplate(Calibroot, channel, indice[kindice])
    Calibresult  =  fitmW(MCTemplates, MassSteps, MCNominal, MwNominal)
    CalibTotal2  =  CalibTotal2 + (Calibresult[0]**2 - Nomresult[0]**2)


#*******************************************************************************************************
# Calculate the recoil systematics:
#*******************************************************************************************************

HRSyst  = open('SystematicVariations/RecoilVariations/Recoil_Variation_Wminusenu5.list','r')
HRTotal = 0

for line in HRSyst.readlines():
    HRroot       =  ROOT.TFile.Open(line.strip(),'read')
    MCNominal    =  ReadMCFiles(HRroot, channel, indice[kindice])
    MCTemplates  =  ReadMCTemplate(HRroot, channel, indice[kindice])
    Recoilresult =  fitmW(MCTemplates, MassSteps, MCNominal, MwNominal)
    HRTotal      =  HRTotal + (Recoilresult[0]**2 - Nomresult[0]**2)

#*******************************************************************************************************
# Print all the systematics
#*******************************************************************************************************

print(" eta region          	: ", indice[kindice]        )
print(" Centre value        	: ", Nomresult[0]      	    )
print(" Stat error          	: ", Nomresult[1]      	    )
print(" Calib alpha Systematic  : ", sqrt(CalibTotal1)      )
print(" Calib c Systematic    	: ", sqrt(CalibTotal2)      )
print(" Recoil  Systematic      : ", sqrt(HRTotal)          )
print(" Id Systematic       : ", sqrt(IdSystematic)      )
print(" reco Systematic     : ", sqrt(recoSystematic)    )
print(" Iso Systematic      : ", sqrt(isoSystematic)     )
print(" Trigger Systematic  : ", sqrt(triggerSystematic) )

#*******************************************************************************************************
# Make the Latex table
#*******************************************************************************************************
'''
#CreatLatexTable(channel)
print("end")










