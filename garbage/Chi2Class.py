# -*-coding:Latin-1 -* 

from   math import *
from   array import array

import pylab
import numpy as np
import matplotlib.pyplot as plt

import ROOT
import ROOT as root
from   ROOT import TH1F, TH1D, TGraph, TF1, TLatex, TPaveText, TText, TFile, TCanvas

class Chi2:
    """Classe représentant une personne"""

    def __init__(self):
        """Constructeur de notre classe"""

    def Chi2Calculation(self, MCNominal, Data, MCTemplates, MassSteps, Mwmin, Mwmax, Mw, Type):

        print("")
        print("************ Start the Chi2 Calculation ************")
        print("")

        for hist in MCTemplates:
                hist.Add(Data)

        # Normalisation
        Data.Scale(1/Data.Integral())
        for hist in MCTemplates:
                hist.Scale(1/hist.Integral())

        # Calculate the Xhi2:
        Chi2 = []
        for hist in MCTemplates:
            x2 = 0
            for i in range( int(Mwmin/2),  1 + int(Mwmax/2) ):
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
        f1 = TF1("f1","pol2",80.2,80.6)
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


        MyFile  = TFile("Output/FitSummary_"+Type+".root","RECREATE");
        grS.Write()
        gr.Write()
        hmyfunc = f1.GetHistogram()
        hmyfunc.Write()
        MyFile.Close()

        return results
   
    def Chi2Sysematics(self, MCNominal, Data, MCTemplates, MassSteps, Mwmin, Mwmax, Mw, Type):

        print("")
        print("************ Start the Chi2 Calculation ************")
        print("")

	for hist in MCTemplates:
    		hist.Add(Data)

	# Normalisation
	Data.Scale(1/Data.Integral())
	for hist in MCTemplates:
    		hist.Scale(1/hist.Integral())

        # Calculate the Xhi2:
        Chi2 = []
        for hist in MCTemplates:
            x2 = 0
            for i in range( int(Mwmin/2),  1 + int(Mwmax/2) ):
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
        f1 = TF1("f1","pol2",80.2,80.6)
        gr.Fit("f1")

	# print the results.
        print("Minimum of the Chi2: %f" %f1.GetMinimum())
        print("Mw corresponding to Minimum of the Chi2: %f" %f1.GetMinimumX())

	# return the results
	results = []
	results.append(f1.GetMinimum())
	results.append(f1.GetMinimumX())

	MyFile  = TFile("Output/FitSummary_"+Type+".root","RECREATE");
	grS.Write()
        gr.Write()
	hmyfunc = f1.GetHistogram()
	hmyfunc.Write()
	MyFile.Close()
	
        return results

