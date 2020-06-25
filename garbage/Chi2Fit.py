#!/usr/bin/env python
# -*-coding:Latin-1 -*

import atlasplots
from   atlasplots import atlas_style as astyle
from   atlasplots import utils
from   atlasplots import config_reader as config

from   math 	import *
from   array 	import array
from   source	import *

import ROOT
import ROOT as root
from   ROOT import gROOT, TCanvas, TFile, THStack, TH1F, TPad, TLine, TAttFill, TF1, TGraph, gROOT, gRandom

def CorrelationCoefficient(pTlMwToys, mTMwToys):
 
	MwpTlmoy = 0
	MwmTmoy  = 0
	for i in range(0, len(pTlMwToys)):
    	    MwpTlmoy = MwpTlmoy + pTlMwToys[i]
    	    MwmTmoy  = MwmTmoy  + mTMwToys[i]

	mTErrorStat   = 0
	elPtErrorStat = 0
	for i in range(0, len(mTMwToys)):
            mTErrorStat   = mTErrorStat   + (mTMwToys[i]  - (MwmTmoy/len(mTMwToys)))*(mTMwToys[i] - (MwmTmoy/len(mTMwToys)))
    	    elPtErrorStat = elPtErrorStat + (pTlMwToys[i] - (MwpTlmoy/len(mTMwToys)))*(pTlMwToys[i] - (MwpTlmoy/len(mTMwToys)))

	Cor = 0
	for i in range(0, len(mTMwToys)):
            Cor = Cor + (mTMwToys[i]  - (MwmTmoy/len(mTMwToys)))*(pTlMwToys[i] - (MwpTlmoy/len(mTMwToys)))

	print("cor :", Cor/sqrt(mTErrorStat*elPtErrorStat))

	return Cor

def GraphPloting(pTlMwToys, mTMwToys):

	n = len(pTlMwToys)
	x, y = array( 'd' ), array( 'd' )

	for i in range( n ):
    	    print(i)
    	    x.append( pTlMwToys[i] )
    	    y.append( mTMwToys[i]  )

	gr = TGraph(n, x, y)
	axis = gr.GetXaxis()
	axis.SetLimits(80200,80600)             # along X
   	gr.GetHistogram().SetMaximum(80200)  # along          
   	gr.GetHistogram().SetMinimum(80600)  #   Y    

	gr.Draw("P")
	gr.SetLineWidth(0) 
	gr.SetMarkerStyle(20)
	
	output = TFile("ddd.root","recreate")
        gr.Write()
        output.Close()

	return gr

def MwToys(MC, Data, channel, Variable, MassSteps, indice, MwNominal):

        DataNominal    = ReadNominalDistribution(       Data,   channel, Variable, indice)
        MCNominal      = ReadNominalDistribution( 	MC,     channel, Variable, indice)
        DataToys       = GetToys(                      	Data,   channel, Variable, indice) 
        MCTemplates    = ReadMCTemplate(                MC,     channel, Variable, indice)

	for i in range(0, len(DataToys)):
	    for j in range(0, DataToys[i].GetNbinsX()):
                DataToys[i].SetBinError(j+1, sqrt(DataNominal.GetBinContent(j+1)))
                #DataToys[i].SetBinError(j+1, sqrt(DataToys[i].GetBinContent(j+1)))

	'''
        #for i in range(0, len(DataToys)):
        #    for j in range(0, DataToys[i].GetNbinsX()):
        #        print("Toy ",i, "       Bin ",j, DataToys[i].GetBinContent(j+1),  DataToys[i].GetBinError(j+1))

	for i in range(0, len(MCTemplates)):
	    print(i, MCTemplates[i].GetMean())

        MCTemplatesCope = AddNominalDistribution(MCTemplates, DataToys[0])
	
   	for i in range(0, len(MCTemplatesCope)):
            print(i, MCTemplatesCope[i].GetMean())
	'''
	'''
        MwToys = []
	MCTemplatesCope = []
        for i in range(0, len(DataToys)):
	    MCTemplatesCope  = AddNominalDistribution(MCTemplates, DataToys[i])
            Nomresult    = fitmW(MCTemplatesCope, MassSteps, DataToys[i], MwNominal)
            MwToys.append(Nomresult[0])
	    MCTemplatesCope[:] = []

	for i in range(0, len(MwToys)):
	    print("Toy: ",i, MwToys[i])

        return MwToys
	'''
	
def GetToysByHand(fInput, Channel, Variable, indice):

        ToysOfData = []
        director =  fInput.GetDirectory( Channel+"Selection_WeightVariations" )
        i=0
        for key in director.GetListOfKeys():
            hist = key.ReadObj()
            if hist.ClassName() == 'TH1D' :
		if ((hist.GetName()).find(Variable +indice +"_cut8_toy") != -1 and (hist.GetName()).find("truth") != 0):
                    print(hist.GetName())
                    ToysOfData.append(hist)
                    i=i+1
        return ToysOfData

def GetToys(fInput, Channel, Variable, indice):

        MatrixpTlvsmT = fInput.Get( Channel+"Selection/elPt_Reco_vs_mT_cut8")
	
        NToys = 400
        ToysMatrix = []
	
        for k in range(0,  NToys):
            matrix = MatrixpTlvsmT.Clone("matrix")
            for i in range(1, 1 + MatrixpTlvsmT.GetNbinsX() ):
                for j in range(1, 1 + MatrixpTlvsmT.GetNbinsY() ):
                    matrix.SetBinContent(i, j, gRandom.PoissonD(matrix.GetBinContent(i,j)) )
            ToysMatrix.append(matrix)
	
        mTToys  = []
        pTlToys = []
        for k in range(0,  NToys):
            mTToys.append(  (ToysMatrix[k].ProjectionY()).Clone() )
            pTlToys.append( (ToysMatrix[k].ProjectionX()).Clone() )

	if(Variable == "mT"):
        	return mTToys
	if(Variable == "elPt"):
		return pTlToys


def ReadUnfoldeddistribution(Unfolded_Input, itera):
	Nominal   = Unfolded_Input.Get("Unfolded_MC_"+str(itera))
	return Nominal


def fitmW(MCTemplates, MassSteps, MCNominal, MwNominal):

	# define the fit function:
	fpol  = TF1("fpol","(x-[0])*(x-[0])/[1]/[1] + [2]",80300,80500)

	graph = TGraph(len(MCTemplates))
	for i in range(0, len(MCTemplates) ):
	    graph.SetPoint(i, MwNominal+MassSteps[i], MCNominal.Chi2Test(MCTemplates[i], "CHI2WW") )
	    print("Bin : ", i, " Chi2 : ",  MCNominal.Chi2Test(MCTemplates[i], "CHI2WW") )
	
  	fpol.SetParameter(0,MwNominal)
  	fpol.SetParameter(1,10)
  	fpol.SetParameter(2,1.)

  	graph.Fit("fpol","rQ")
	graph.Fit("fpol","rQ")
	graph.Fit("fpol","rQ")

        # print the results.
	print("Nominal : ",   fpol.GetParameter(0))
	print("Stat error : ",fpol.GetParameter(1))	
	
	results = []
	results.append(fpol.GetParameter(0))
	results.append(fpol.GetParameter(1))
	
	#c1 = TCanvas("c1","c1", 800, 600)
	#graph.Draw()
	#c1.Print("ddd.pdf")
	return results

def GetSystematicVariations(IdVariations, MCTemplates, MassSteps, Nomresult, MwNominal):
	
	dmW_val       = []
	SystTemplates = []

	# define the syste
	for i in range(0, len(IdVariations)):
	
	    for k in range(0, len(MCTemplates)):
		HistVar = (IdVariations[i]).Clone("HistVar")
		HistVar.Add(MCTemplates[k])
		SystTemplates.append(HistVar)
	
            fpol  = TF1("fpol","(x-[0])*(x-[0])/[1]/[1] + [2]",80300,80500)
            graph = TGraph(len(MCTemplates))

            for j in range(0, len(MCTemplates)):
       		 graph.SetPoint(j, MwNominal+MassSteps[j], IdVariations[i].Chi2Test(SystTemplates[j], "CHI2WW"))

	    fpol.SetParameter(0,MwNominal)
            fpol.SetParameter(1,10)
            fpol.SetParameter(2,1.)

  	    graph.Fit("fpol","rQ")
		
	    dmW_val.append(fpol.GetParameter(0) - Nomresult)

	    del SystTemplates[:]

	return dmW_val




def Chi2Calculation(MCTemplates, MassSteps, Data, Mw):

        # Calculate the Xhi2:
        Chi2 = []
        for hist in MCTemplates:
            x2 = 0
            for i in range( 0,  100 ):
                if( Data.GetBinError(i) != 0 or hist.GetBinError(i) != 0):
                    x2 = x2 + ((Data.GetBinContent(i) - hist.GetBinContent(i))**2)/( Data.GetBinError(i)**2 +  hist.GetBinError(i)**2 )
            Chi2.append(x2)

        #prepare the graph for Chi2     
        n = len(MassSteps)
        x, y = array( 'd' ), array( 'd' )
        for val in MassSteps:
            x.append(Mw - val*10**-3)
        for chi in Chi2:
            y.append(chi)

        # define the graphe
        gr  = TGraph(n,x,y)
        grS = TGraph(n,x,y)
        gr.SetTitle("Graph")
        grS.SetTitle("GraphVierge")
        gr.SetName("Graph")
        grS.SetName("GraphVierge")

        # prepare the Fit
        f1 = TF1("f1","pol2",80.3,80.5)
        gr.Fit("f1")

        # print the results.
        print("Minimum of the Chi2: %f" %f1.GetMinimum())
        print("Mw corresponding to Minimum of the Chi2: %f" %f1.GetMinimumX())

        # get the stat error
        step=0
        minimum=10
        for i in range(1,10**4) :
                step      = step + 0.00001
                Diff      = abs(f1.Eval( f1.GetMinimumX() + step ) - (f1.GetMinimum()+1))
                if(minimum > Diff):
                        minimum   = Diff
                        stepEval  = 1000*step
        print(" The Stat Error: %f " %stepEval)

        # return the results
        results = []
        results.append(f1.GetMinimum())
        results.append(f1.GetMinimumX())
        results.append(stepEval)

        return results

