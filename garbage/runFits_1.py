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


with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile)

# read config file:
print("")
print("************ read config file ************")
print("")
print("Channel         : %s" %cfg['Channel'])
print("MASSSTEPS       : %s" %cfg['MASSSTEPS'])
print("Wminusenu_MCFile: %s" %cfg['Wminusenu_MCFile'])
print("")

# read MC file:
print("")
print("************ read Input files ************")
print("")

MC     = root.TFile(cfg['Wminusenu_MCFile'])
MC_B   = root.TFile(cfg['Wminusenu_MC_B_File'])
Data   = root.TFile(cfg['Wminusenu_DataFile'])
Data_B = root.TFile(cfg['Wminusenu_Data_B_File'])

#MCID  = root.TFile(cfg['MCFileId'])
#MCRe  = root.TFile(cfg['MCFilere'])
#MCIs  = root.TFile(cfg['MCFileIs'])
#MCTr  = root.TFile(cfg['MCFileTr'])

print("MC              : %s "%MC)
print("MC - Boostrap   : %s "%MC_B)
print("Data            : %s "%Data)
print("Data - Boostrap : %s "%Data_B)

print("")

# define the region: eta1(<0.6), eta2(<1.2 and >0.6), eta3(<1.8 and >1.2) and eta4(<2.4 and >1.8)

# read the data and tamplate distributions:
channel      = cfg['Channel']
MassSteps    = cfg['MASSSTEPS']
indice 	     = ["","_eta1", "_eta2", "_eta3", "_eta4"]
kindice      = 0
Variable     = "mT"
MwNominal    = 80400


#*******************************************************************************************************
# calulate the mass using toys of MC with mT:
#*******************************************************************************************************
'''
Variable     = "mT"
MCToys       = ReadToysMC(MC_B, channel, Variable, indice[kindice])
MCTemplates  = ReadMCTemplate(MC, channel, Variable, indice[kindice])
MCNominal    = ReadMCFiles(MC, channel, Variable, indice[kindice])

# add nominal to toys
#for i in range(0, 10):
for i in range(0, len(MCToys)):
    MCToys[i].Add(MCNominal)
    print(" toy : ",i,"     Mean : ", MCToys[i].GetMean())

MwValuemT     = []
MwValuemTStat = []

for i in range(0, 50):
#for i in range(0, len(MCToys)):
    Nomresult    = fitmW(MCTemplates, MassSteps, MCToys[i], MwNominal)
    MwValuemT.append(Nomresult[0])
    MwValuemTStat.append(Nomresult[1])

CompareToys(MwValuemT, MwValuemTStat)
'''

#*******************************************************************************************************
# calulate the mass using toys of MC wth pTl:
#*******************************************************************************************************
'''
Variable    = "elPt"
MCToys      = ReadToysMC(MC_B, channel, Variable, indice[kindice])
MCTemplates = ReadMCTemplate(MC, channel, Variable, indice[kindice])
MCNominal   = ReadMCFiles(MC,  channel, Variable, indice[kindice])

# creat a clone of the Template Variations:
MCTemplatesClone = []
for i in range(0, len(MCTemplates)):
    MCTemplatesClone.append( MCTemplates[i] )

# add nominal distribution to bootstrap variation to creat Toys:
for i in range(0, len(MCToys)):
    MCToys[i].Add(MCNominal)

# change the error in the toys to error on the Nominal distribution:
for i in range(0, len(MCToys)):
    for j in range(0, MCToys[0].GetNbinsX()):
    	MCToys[i].SetBinError(j+1, MCNominal.GetBinError(j+1))



MwValuepTl = []
#for i in range(0, len(MCToys)):
for i in range(0, 10):

    for j in range(0, len(MCTemplates) ):
        MCTemplates[i].Add(MCToys[i])

    for j in range(0, len(MCTemplates) ):
	for j in range(0, MCTemplates[0].GetNbinsX()):
            MCTemplates[i].SetBinError(j+1, MCTemplatesClone[i].GetBinError(j+1))

    Nomresult    = fitmW(MCTemplates, MassSteps, MCToys[i], MwNominal)
   
    for i in range(0, len(MCTemplates)):
	MCTemplates[i] = MCTemplatesClone[i]
    #MwValuepTl.append(Nomresult[0])

'''


# transverse mass distribution

MwValuepTl = []
MwValuepTlStat = []

Variable    = "elPt"
MCToys      = ReadToysMC(MC_B, channel, Variable, indice[kindice])
MCTemplates = ReadMCTemplate(MC, channel, Variable, indice[kindice])
MCNominal   = ReadMCFiles(MC,  channel, Variable, indice[kindice])

MCTemplatesO = []
for i in range(0, len(MCTemplates)):
    MCTemplatesO.append( MCTemplates[i].Clone() )

MCToysO = []
for i in range(0, len(MCToys)):
    MCToysO.append( MCToys[i].Clone() )



for toy in range(0, len(MCToys)):
	
	# Add Nominal distribution to Toys:
	for i in range(0, MCNominal.GetNbinsX()):
	    MCToys[toy].SetBinContent( i+1, MCToysO[toy].GetBinContent(i+1)  + MCNominal.GetBinContent(i+1)  )
	    MCToys[toy].SetBinError(   i+1, MCToysO[toy].GetBinError(i+1)  )

	# add nominal distribution to bootstrap variation to creat Toys:
	for i in range(0, len(MCTemplates)):
	    for j in range(0, MCNominal.GetNbinsX()):
	        MCTemplates[i].SetBinContent( j+1, MCTemplatesO[i].GetBinContent(j+1) + MCToys[toy].GetBinContent(j+1)  )
                MCTemplates[i].SetBinError(   j+1, MCTemplatesO[i].GetBinError(j+1) )

	Nomresult    = fitmW(MCTemplates, MassSteps, MCToys[toy], MwNominal)

	MwValuepTl.append(Nomresult[0])
	MwValuepTlStat.append(Nomresult[1])

for i in range(0, len(MwValuepTl)):
    	print(MwValuepTl[i], MwValuepTlStat[i])

# pT lepton distribution

MwValuemT = []
MwValuemTStat = []

Variable    = "mT"
MCToys      = ReadToysMC(MC_B, channel, Variable, indice[kindice])
MCTemplates = ReadMCTemplate(MC, channel, Variable, indice[kindice])
MCNominal   = ReadMCFiles(MC,  channel, Variable, indice[kindice])

MCTemplatesO = []
for i in range(0, len(MCTemplates)):
    MCTemplatesO.append( MCTemplates[i].Clone() )

MCToysO = []
for i in range(0, len(MCToys)):
    MCToysO.append( MCToys[i].Clone() )



for toy in range(0, len(MCToys)):

        # Add Nominal distribution to Toys:
        for i in range(0, MCNominal.GetNbinsX()):
            MCToys[toy].SetBinContent( i+1, MCToysO[toy].GetBinContent(i+1)  + MCNominal.GetBinContent(i+1)  )
            MCToys[toy].SetBinError(   i+1, MCToysO[toy].GetBinError(i+1)  )

        # add nominal distribution to bootstrap variation to creat Toys:
        for i in range(0, len(MCTemplates)):
            for j in range(0, MCNominal.GetNbinsX()):
                MCTemplates[i].SetBinContent( j+1, MCTemplatesO[i].GetBinContent(j+1) + MCToys[toy].GetBinContent(j+1)  )
                MCTemplates[i].SetBinError(   j+1, MCTemplatesO[i].GetBinError(j+1) )

        Nomresult    = fitmW(MCTemplates, MassSteps, MCToys[toy], MwNominal)

        MwValuemT.append(Nomresult[0])
        MwValuemTStat.append(Nomresult[1])

for i in range(0, len(MwValuepTl)):
        print(MwValuemT[i], MwValuemTStat[i])


''' 
Nominal:
# add nominal distribution to bootstrap variation to creat Toys:
for i in range(0, len(MCTemplates)):
    MCTemplates[i].Add(MCNominal)

# change the error in the toys to error on the Nominal distribution:
for i in range(0, len(MCTemplates)):
    for j in range(0, MCTemplates[0].GetNbinsX()):
        MCTemplates[i].SetBinError(j+1, MCNominal.GetBinError(j+1))
'''

#*******************************************************************************************************
# Calculate the Covariance matrix::
#*******************************************************************************************************

print(len(MwValuepTl))

n = 400
x, y = array( 'd' ), array( 'd' )
 
for i in range( n ):
    print(i)
    x.append( MwValuepTl[i] )
    y.append( MwValuemT[i]  ) 

gr = TGraph(400,x, y)
gr.Draw("P")
gr.SetLineWidth(0)
gr.SetMarkerSize(2)
print("Marker size", gr.GetMarkerSize())
#CovMatrix = TH2D("CovMatrix", "CovMatrix" , 100, 0, 100, 100, 0, 200)

Output = ROOT.TFile.Open("Matrix.root","RECREATE")
gr.Write("gr")


#*******************************************************************************************************
# Calculate the correlation factor::
#*******************************************************************************************************
MwpTlmoy = 0
MwmTmoy  = 0
for i in range(0, len(MwValuepTl)):
    MwpTlmoy = MwpTlmoy + MwValuepTl[i]
    MwmTmoy  = MwmTmoy  + MwValuemT[i]

mTErrorStat   = 0
elPtErrorStat = 0
for i in range(0, len(MwValuepTl)):
    mTErrorStat   = mTErrorStat   + (MwValuemT[i]  - (MwmTmoy/len(MwValuepTl)))*(MwValuemT[i] - (MwmTmoy/len(MwValuepTl)))
    elPtErrorStat = elPtErrorStat + (MwValuepTl[i] - (MwpTlmoy/len(MwValuepTl)))*(MwValuepTl[i] - (MwpTlmoy/len(MwValuepTl)))

Cor = 0
for i in range(0, len(MwValuepTl)):
    Cor = Cor + (MwValuemT[i]  - (MwmTmoy/len(MwValuepTl)))*(MwValuepTl[i] - (MwpTlmoy/len(MwValuepTl)))

print("cor :", Cor/sqrt(mTErrorStat*elPtErrorStat))

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










