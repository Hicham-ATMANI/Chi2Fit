#!/usr/bin/env python
# -*-coding:Latin-1 -*


from math import *

import ROOT
import ROOT as root
from   ROOT import gROOT, TCanvas, TFile, THStack, TH1F, TPad, TLine, TAttFill, TF1, TGraph

def TableListMC(TableMClpT, TableMCmT, channel, ChannelName):

	latexFile = open("Output/Table/Table_MCTest_"+channel+".tex","w+")
        latexFile.write("\\documentclass[12pt]{article} \n")
        latexFile.write("\\usepackage{amsmath}\n")
        latexFile.write("\\usepackage{graphicx}\n")
        latexFile.write("\\usepackage{hyperref}\n")
        latexFile.write("\\usepackage{hyperref}\n")
        latexFile.write("\\usepackage{multirow}\n")
        latexFile.write("\\usepackage[latin1]{inputenc}\n")
        latexFile.write("\\begin{document}\n")
        latexFile.write("\\begin{table}[]\n")
	latexFile.write("\\resizebox{\\textwidth}{!}{  \n")
	latexFile.write("\\begin{tabular}{ccccccccccc} \n")
	latexFile.write("\\hline  \\hline \n")
	latexFile.write("$\eta_{l}$ range       & \multicolumn{2}{c}{{[}0, 0.6{]}} & \multicolumn{2}{c}{{[}0.6, 1.2{]}} & \multicolumn{2}{c}{{[}1.2, 1.8{]}} & \multicolumn{2}{c}{{[}1.8, 2.4{]}} & \multicolumn{2}{c}{{[}0, 2.4{]}} \\\ \n")
	latexFile.write("Kinematic distribution & $p_{T}^{l}$     & $m_{T}^{W}$    & $p_{T}^{l}$      & $m_{T}^{W}$     & $p_{T}^{l}$      & $m_{T}^{W}$     & $p_{T}^{l}$      & $m_{T}^{W}$     & $p_{T}^{l}$     & $m_{T}^{W}$    \\\ \\hline \\hline \n")

	latexFile.write("channel                & \multicolumn{10}{c}{$W^{-}\\rightarrow e^{-}\\nu,   5TeV$}                                                                                                                         \\\	 \n")
	latexFile.write("Stat{[}MeV{]}          &       %3.2f     &      %3.2f     &      %3.2f       &    %3.2f        &       %3.2f      &    %3.2f        &  %3.2f           &  %3.2f          &     %3.2f       &   %3.2f        \\\	 \n"%(abs(TableMClpT[1]), abs(TableMCmT[1]), abs(TableMClpT[2]),  abs(TableMCmT[2]), abs(TableMClpT[3]), abs(TableMCmT[3]), abs(TableMClpT[4]), abs(TableMCmT[4]), abs(TableMClpT[0]), abs(TableMCmT[0])))
	latexFile.write("Correlation            & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\ 	 \n")
	latexFile.write("Combined               & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\ \\hline \\hline \n")

        latexFile.write("channel                & \multicolumn{10}{c}{$W^{+}\\rightarrow e^{+}\\nu,   5TeV$}                                                                                                                         \\\         \n")
        latexFile.write("Stat{[}MeV{]}          &       %3.2f     &      %3.2f     &      %3.2f       &    %3.2f        &       %3.2f      &    %3.2f        &  %3.2f           &  %3.2f          &     %3.2f       &   %3.2f        \\\         \n"%(abs(TableMClpT[6]), abs(TableMCmT[6]), abs(TableMClpT[7]),  abs(TableMCmT[7]), abs(TableMClpT[8]), abs(TableMCmT[8]), abs(TableMClpT[9]), abs(TableMCmT[9]), abs(TableMClpT[5]), abs(TableMCmT[5])))
        latexFile.write("Correlation            & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\         \n")
        latexFile.write("Combined               & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\ \\hline \\hline \n")

        latexFile.write("channel                & \multicolumn{10}{c}{$W^{-}\\rightarrow \\mu^{-}\\nu,   5TeV$}                                                                                                                     \\\         \n")
        latexFile.write("Stat{[}MeV{]}          &       %3.2f     &      %3.2f     &      %3.2f       &    %3.2f        &       %3.2f      &    %3.2f        &  %3.2f           &  %3.2f          &     %3.2f       &   %3.2f        \\\         \n"%(abs(TableMClpT[11]), abs(TableMCmT[11]), abs(TableMClpT[12]),  abs(TableMCmT[12]), abs(TableMClpT[13]), abs(TableMCmT[13]), abs(TableMClpT[14]), abs(TableMCmT[14]), abs(TableMClpT[10]), abs(TableMCmT[10])))
        latexFile.write("Correlation            & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\         \n")
        latexFile.write("Combined               & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\ \\hline \\hline \n")

        latexFile.write("channel                & \multicolumn{10}{c}{$W^{+}\\rightarrow \\mu^{+}\\nu,   5TeV$}                                                                                                                      \\\         \n")
        latexFile.write("Stat{[}MeV{]}          &       %3.2f     &      %3.2f     &      %3.2f       &    %3.2f        &       %3.2f      &    %3.2f        &  %3.2f           &  %3.2f          &     %3.2f       &   %3.2f        \\\         \n"%(abs(TableMClpT[16]), abs(TableMCmT[16]), abs(TableMClpT[17]),  abs(TableMCmT[17]), abs(TableMClpT[18]), abs(TableMCmT[18]), abs(TableMClpT[19]), abs(TableMCmT[19]), abs(TableMClpT[15]), abs(TableMCmT[15])))
        latexFile.write("Correlation            & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\         \n")
        latexFile.write("Combined               & \multicolumn{2}{c}{}             & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}               & \multicolumn{2}{c}{}             \\\ \\hline \\hline \n")

	latexFile.write("\\end{tabular}\n")
	latexFile.write("}\n")
        latexFile.write("\\end{table}\n")
        latexFile.write("\\end{document}\n")
        latexFile.close()

def CreatLatexTable(channel):
        latexFile = open("Output/Table_"+channel+".tex","w+")
        latexFile.write("\\documentclass[12pt]{article} \n")
        latexFile.write("\\usepackage{amsmath}\n")
        latexFile.write("\\usepackage{graphicx}\n")
        latexFile.write("\\usepackage{hyperref}\n")
        latexFile.write("\\usepackage{hyperref}\n")
	latexFile.write("\\usepackage{multirow}\n")
        latexFile.write("\\usepackage[latin1]{inputenc}\n")
        latexFile.write("\\begin{document}\n")


 	latexFile.write("\\begin{table}[]\n")
 	latexFile.write("\\begin{tabular}{|l|l|l|l|l|l|l|l|}\n")
 	latexFile.write("\\hline\n")
	latexFile.write("\\multicolumn{1}{|c|}{}                    &                             & \multicolumn{6}{c|}{Channels}                                                                                     \\\ \\hline \n")
	latexFile.write("\\multicolumn{1}{|c|}{Systematic}          & \multicolumn{1}{c|}{method} & \multicolumn{3}{c|}{eta 1} & \multicolumn{1}{c|}{eta 2} & \multicolumn{1}{c|}{eta 3} & \multicolumn{1}{c|}{eta 4} \\\ \\hline     \n")
	latexFile.write("\\multicolumn{1}{|c|}{\multirow{2}{*}{Id}} &                             & \multicolumn{3}{l|}{}      &                            &                            &                            \\\ \cline{2-8} \n")
	latexFile.write("\\multicolumn{1}{|c|}{}                    &                             & \multicolumn{3}{l|}{}      &                            &                            &                            \\\ \\hline\n") 
	latexFile.write("\\multirow{2}{*}{}                         &                             & \multicolumn{3}{l|}{}      &                            &                            &                            \\\ \cline{2-8} \n")
        latexFile.write("                                  &                         & \multicolumn{3}{l|}{}       &                            &                            &                            \\\ \\hline \n")
	latexFile.write("\\multirow{2}{*}{}                         &                             & \multicolumn{3}{l|}{}      &                            &                            &                            \\\ \cline{2-8}\n")
        latexFile.write("                                  &                         & \multicolumn{3}{l|}{}       &                            &                            &                            \\\ \\hline \n")
	latexFile.write("\\multirow{2}{*}{}                         &                             & \multicolumn{3}{l|}{}      &                            &                            &                            \\\ \cline{2-8} \n")
	latexFile.write("                                  &                         & \multicolumn{3}{l|}{}       &                            &                            &                            \\\ \\hline \n")
	latexFile.write("\\end{tabular}\n")
	latexFile.write("\\end{table}\n")


        latexFile.write("\\end{document}\n")
        latexFile.close()
