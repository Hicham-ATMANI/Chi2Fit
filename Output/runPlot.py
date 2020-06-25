# -*-coding:Latin-1 -* 

from   math import *
from   array import array
import ROOT
import ROOT as root

from   ROOT import TFile, TH1F, TH1D, TCanvas, TGraph, TF1, gStyle, TLine, TPaveText, TLatex, TPad

# ****************************************************************************************************************************************************************************************************
# *************************************************************************************** Stat error plot  *******************************************************************************************
# ****************************************************************************************************************************************************************************************************

# Get the Graph
FitSummary_Stat = TFile("FitSummary_Stat.root")
Graph 		= FitSummary_Stat.Get("GraphVierge")
Graph.SetTitle("")

func            = FitSummary_Stat.Get("Func")
func1		= func.Clone("func1")

# Prepare the fite
f1 = TF1("f1","pol2",80.2,80.6)
Graph.Fit("f1")

# change the range of the axes Y
Graph.GetYaxis().SetRangeUser(-1,5)
Graph.GetXaxis().SetRangeUser(80.36,80.44)
Graph.GetXaxis().SetTitle("Mw")
Graph.GetYaxis().SetTitle("X^{2}")

# Get the stat error   
step=0  
minimum=10        
for i in range(1,10**4) :
	step      = step + 0.00001
	Diff      = abs(f1.Eval( f1.GetMinimumX() + step ) - (f1.GetMinimum()+1))
	if(minimum > Diff):
		minimum   = Diff
		stepEval  = 1000*step
print(" The Stat Error: %f " %stepEval)

# add line to plot
Min   = f1.GetMinimum()
XMin  = f1.GetMinimumX()

line1 = TLine(80.358, Min,  80.442, Min)
line2 = TLine(80.358, Min+1,80.442, Min+1)

line3 = TLine(XMin, 	     	   -1, XMin,          	    Min+1)
line4 = TLine(XMin+0.001*stepEval, -1, XMin+0.001*stepEval, Min+1)
line5 = TLine(XMin-0.001*stepEval, -1, XMin-0.001*stepEval, Min+1)

# Save the plot
c = TCanvas("c","c", 800, 600)
gStyle.SetPadBorderMode(1)
gStyle.SetOptFit(1)
Graph.Draw("AC*")
line1.Draw("same")
line2.Draw("same")
line3.Draw("same")
line4.Draw("same")
line5.Draw("same")
   
pt = TPaveText(0.14,0.7,0.4,0.85,"NDC")
pt.SetTextSize(0.04)
pt.SetFillColor(0)
pt.SetTextAlign(12)
mwstring   = "Mw = " + str(f1.GetMinimumX())
Statstring = "#delta^{Stat} = " + str(stepEval)+" MeV"
pt.AddText(mwstring)
pt.AddText(Statstring)
pt.Draw("same")

c.SaveAs("Chi2_Stat.pdf")



