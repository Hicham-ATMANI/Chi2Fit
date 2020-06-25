# -*-coding:Latin-1 -* 

from   math import *
from   array import array
import ROOT
import ROOT as root

from   ROOT import TFile, TH1F, TH1D, TGraphErrors

def makeLegend(hists, xmin, ymin, xmax, ymax):
    legend = root.TLegend(xmin, ymin, xmax, ymax)
    legend.SetTextSize(0.04)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetBorderSize(0)
    legend.SetLineWidth(2)
    i=1
    for hist in hists:
        hist.SetLineColor(i)
        legend.AddEntry(hist, hist.GetName())
        i=i+1
    return legend

def CompareToys(MwValuemT, MwValuemTStat):
    	print(len(MwValuemT), len(MwValuemTStat))

	n = len(MwValuemT)
	x, y   = array( 'd' ), array( 'd' )
        ex, ey = array( 'd' ), array( 'd' )

	for i in range( 0, n ):
    		x.append( i+1 )
		ex.append( 0 )
    		y.append( MwValuemT[i]  ) 
		ey.append( MwValuemTStat[i])

        gr = TGraphErrors(n,x,y,ex,ey);
	gr.Draw("P")
	gr.SetLineWidth(0)
	gr.SetMarkerStyle(20)
	gr.SetMarkerSize(1)

	xax = gr.GetXaxis()
        for i in range( 0, n ):
	    binIndex = xax.FindBin(i)
    	    xax.SetBinLabel(binIndex,"toys")

	Output = ROOT.TFile.Open("Matrix.root","RECREATE")
	gr.Write("gr")

def Comparedistributions(self, MCNominal, Data, MCTemplates):
	print("")
	print("************ Show the nominal plot ************")
	print("")
        # add the nominal plot to variations
        i=0
        for hist in MCTemplates:
            hist.Add(MCNominal)

        for hist in MCTemplates:
            hist.SetLineWidth(2)
            for i in range(1,101) :
                hist.SetBinError(i,0)

        legend = makeLegend(MCTemplates,0.65, 0.35,0.92,0.77)

        # define the Canvas output
        c1 = root.TCanvas("c1", "CompareNominalPlots", 0, 0, 800, 600)
        c1.Draw()
        c1.cd()

        #define the pad
        pad1 = root.TPad("pad1", "pad1", 0, 0.33, 1, 1.0)
        pad1.SetBottomMargin(0.)
        pad1.Draw()
        pad1.SetFillStyle(4000)
        pad1.cd()

        MCNominal.SetStats(0)
        MCNominal.SetTitle("")
        MCNominal.GetYaxis().SetTitle("Events")
        MCNominal.GetXaxis().SetRangeUser(50,120)
        MCNominal.GetXaxis().SetTitle("m_{w}^{T} [GeV]")
        MCNominal.GetYaxis().SetTitleOffset(1.4)
        MCNominal.GetXaxis().SetTitleOffset(1.4)
        MCNominal.Draw("same")

        for hist in MCTemplates:
            hist.Draw("same")
        legend.Draw("same")

        c1.cd()
        pad2 = root.TPad("pad2", "pad2", 0, 0.0, 1, 0.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        pad2.Draw()
        pad2.SetFillStyle(4000)
        pad2.cd()

        #Define the ratio Plot

        ratioplots = []
        for hist in MCTemplates:
            ratiohist = MCNominal.Clone("ratiohist")
            ratiohist.Divide(hist)
            for i in range(1,101):
                ratiohist.SetBinError(i,0)
            ratiohist.GetXaxis().SetRangeUser(50,120)
            ratiohist.GetYaxis().SetRangeUser(0.961,1.039)
            ratiohist.SetLineWidth(2)
            ratioplots.append(ratiohist)

        ratioplots[0].GetYaxis().SetNdivisions(5)
        ratioplots[0].GetYaxis().SetTitle("Nominal/Var")
        ratioplots[0].GetXaxis().SetTitle("m_{w}^{T} [GeV]")
        ratioplots[0].GetXaxis().SetLabelSize(0.1)
        ratioplots[0].GetXaxis().SetTitleSize(0.13)
        ratioplots[0].GetXaxis().SetTitleOffset(0.6)

        ratioplots[9].GetYaxis().SetTitleOffset(0.6)
        ratioplots[0].GetYaxis().SetTitleSize(0.1)
        ratioplots[0].GetYaxis().SetLabelSize(0.1)
        ratioplots[0].GetYaxis().CenterTitle()

        i=0
        for hist in ratioplots:
            hist.SetLineColor(i)
            hist.Draw("same")
            i=i+1

        c1.Print("Output/Plot1.pdf")

