#!/usr/bin/env python
# -*-coding:Latin-1 -*

#import atlasplots
#from   atlasplots import atlas_style as astyle
#from   atlasplots import utils
#from   atlasplots import config_reader as config

from math import *
from   array import array

import ROOT
import ROOT as root
from   ROOT import gROOT, TCanvas, TFile, THStack, TH1F, TPad, TLine, TAttFill, TF1, TGraph, gROOT, gRandom

def AddNominalDistributionToToys(Toys, Nominal):

        ToysS   = []
        for i in range(0, len(Toys)):
            ToysS.append( Toys[i].Clone() )

        for i in range(0, len(Toys)):
            for j in range(0, Nominal.GetNbinsX()):
                ToysS[i].SetBinContent( j+1, ToysS[i].GetBinContent(j+1) + Nominal.GetBinContent(j+1) )
                #ToysS[i].SetBinError(   j+1,                               Nominal.GetBinError(j+1)   )

        return ToysS

def AddNominalDistributionToTemplates(Templates, Nominal):

        TemplatesS = []
        TemplatesO = []
        for i in range(0, len(Templates)):
            TemplatesO.append( Templates[i].Clone() )
            TemplatesS.append( Templates[i].Clone() )

        for i in range(0, len(Templates)):
            for j in range(0, Nominal.GetNbinsX()):
                TemplatesS[i].SetBinContent( j+1, 	TemplatesS[i].GetBinContent(j+1) + Nominal.GetBinContent(j+1) 	)
                print( Nominal.GetBinError(j+1)   )
		#TemplatesS[i].SetBinError(   j+1, 	Nominal.GetBinError(j+1)  					)
                #TemplatesS[i].SetBinError(   j+1, sqrt( pow(TemplatesO[i].GetBinError(j+1),2) + pow(Nominal.GetBinError(j+1),2))   )

	

        return TemplatesS

def ReadMCUnfoldedTemplate(Unfolded_Input, itera):
	MCTemplates=[]
        for keyAsObs in Unfolded_Input.GetListOfKeys():
            hist = keyAsObs.ReadObj()
            if( hist.ClassName() == "TH1D"):
                if ((hist.GetName()).find( 'dG000') != -1 and (hist.GetName()).find("_"+str(itera)) != -1 ):
                    MCTemplates.append( hist )
                    print(hist.GetName(),"  ",hist.GetMean())
        return MCTemplates


def ReadNominalDistribution(inputs, channel, Variable, indice):
	Nominal   = inputs.Get( channel+"Selection/"+Variable+indice+"_cut8")
	print(inputs, Nominal.GetName(), Nominal.GetMean())
        return Nominal

def ReadToys(inputs, channel, Variable, indice):
        MCTemplates=[]
        MCdirectory = inputs.Get(channel+"Selection_WeightVariations")
        for keyAsObs in MCdirectory.GetListOfKeys():
            hist = keyAsObs.ReadObj()
            if( hist.ClassName() == "TH1F"):
                if ((hist.GetName()).find( Variable + indice + '_cut8_toy') != -1 and (hist.GetName()).find('truthmT') == -1 ):
                    MCTemplates.append( hist )
                    print(hist.GetName(),"  ",hist.GetMean())
        return MCTemplates


def ReadMCTemplate(MC, channel, Variable, indice):
        MCTemplates=[]
        MCdirectory = MC.Get(channel+"Selection_WeightVariations")
        for keyAsObs in MCdirectory.GetListOfKeys():
            hist = keyAsObs.ReadObj()
            if( hist.ClassName() == "TH1D"):
                if ((hist.GetName()).find(Variable+indice+'_cut8_dM') != -1 and (hist.GetName()).find('truthmT') == -1 and (hist.GetName()).find('dG000') != -1):
                    MCTemplates.append( hist )
		    print(hist.GetName(),"  ",hist.GetMean())
        return MCTemplates


def getHistVariations(MC, channel, indice):
        MCTemplates=[]
        MCdirectory = MC.Get(channel+"Selection_WeightVariations")
        for keyAsObs in MCdirectory.GetListOfKeys():
            hist = keyAsObs.ReadObj()
            if( hist.ClassName() == "TH1F"):
                if ((hist.GetName()).find(indice+'_cut8_') != -1 and (hist.GetName()).find('truthmT') == -1 and (hist.GetName()).find('down') == -1):
                    MCTemplates.append( hist )
		    print(hist)
        return MCTemplates


