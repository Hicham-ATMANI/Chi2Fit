#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <stdio.h>      
#include <stdlib.h>     
#include <vector>
#include <string>

#include "TString.h"
#include "TFile.h"
#include "TH1D.h"
#include "TMath.h"
#include "TKey.h"
#include "TF1.h"
#include "TGraph.h"

#include "TCanvas.h"
#include "TLine.h"
#include "TPad.h"
#include "TLegend.h"

#include "TLatex.h"
#include "TMatrixDSym.h"
#include "TH2D.h"



#include "TROOT.h"
#include "TSystem.h"

//use gSystem;

using namespace std;



/* Example analysis scenarios

# ls
output_PDFVar_5TeV.root output_PDFVar_13TeV.root output_muSF_13TeV.root


# ... calculate correlation of PDF uncertainties for mW at 5 and 13 TeV, using the pTl distribution

void mWPDFcorr() {

  TFile* f1 = TFile::Open("output_PDFVar_5TeV.root");
  TFile* f2 = TFile::Open("output_PDFVar_13TeV.root");

  // below:
  // - 1st argument is file pointer
  // - 2nd argument is the name of the nominal histogram
  // - 3rd argument is a substring that the target variations to be retrieved should match. Here we get all CT10 variations (10800+)
  //                (could also pass a vector<string>, more robust but more painful)
  // - vhX[0] = nominal distribution; vhX[1...N] = variations

  vector<TH1*> vh5  = getHistVariations(f1, "pTl", "PDFSet_108");
  vector<TH1*> vh13 = getHistVariations(f2, "pTl", "PDFSet_108");

  // get mW templates
  // - 1st argument is file pointer
  // - 2nd argument is nominal histogram name; template-specific suffixes are assumed known
  // - 3rd argument contains the shifts in mW used for the templates
  // - vtmpX are the corresponding template histograms

  vector<double> bias5, bias13;
  vector<TH1*> vtmp5  = getTemplates(f1, "pTl", bias5);
  vector<TH1*> vtmp13 = getTemplates(f2, "pTl", bias13);
  
  // calculate mW shifts under PDF variations

  vector<double> errPDF5  = deltaMw(vh5, vtmp5, bias5, kValue);
  vector<double> errPDF13 = deltaMw(vh13, vtmp13, bias13, kValue);
  
  // final errors and correlations
  // - 2nd argument switches between offsets and toys (for NNPDF we would use kToys for example); calculation downstream done accordingly
  // - 3rd argument is an error scaling; default = 1, but 1.654 for CT10 etc

  double scale68 = 1./1.654;
  double tot5  = getError(errPDF5, kOffset, scale68);
  double tot13 = getError(errPDF13, kOffset, scale68);
  double rho   = getCorrelation(errPDF5, errPDF13);

}


# ... calculate the muon SF uncertainty in the muon eta distribution. Can be used for plotting with error bands,
#     uncertainties in Cw, etc.

void etaLeptonUnc() {

  TFile* f1 = TFile::Open("output_muSF_13TeV.root");

  // below:
  // - 1st argument is file pointer
  // - 2nd argument is the name of the nominal histogram
  // - 3rd argument is a substring that the target variations to be retrieved should match.
  // - vhX[0] = nominal distribution; vhX[1...N] = variations

  vector<TH1*> vh13 = getHistVariations(f1, "etal", "muTrigSF_");

  // returns "up" or "down" histogram
  // - 2nd argument : kOffset [offsets/hessian -> quad. sum of shifts] / kToys [toy MC -> RMS of variations]
  // - 3rd argument : kAbs [hUp = hNom+hErr], kDiff [hUp=hErr], kRel [hUp=(hNom+hErr)/hNom]

  TH1* hUp = getUpUncertainty(vh13, kOffset, kDiff);
  TH1* hDn = getDnUncertainty(vh13, kOffset, kDiff);

}

*/

// enums

enum VariationType {kOffset, kToys};
enum ErrorType {kAbs, kDiff, kRel};
enum ValueType {kValue, kErr};

// histogram manipulations

vector<TH1*> getTemplates(TFile* f, string dirname, string hname, vector<double>& v);
vector<TH1*> getBootstrapToys(TFile* f, string dirname, string hname);
vector<TH1*> getSysVariations(TFile* f, string dirname, string hname, string suffix);
// numerics

double getError(vector<double> v, VariationType vtype, double scale);
double getCorrelation(vector<double> v1, vector<double> v2);

pair<double,double> fit(TH1* data, vector<TH1*> vtemp, vector<double> vbias);

// chi2 
double compute_chi2(TH1* a, TH1* b); 

// final analysis

// ... mW uncertainties

vector<double> deltaMw(vector<TH1*> vdata, vector<TH1*> vtemp, vector<double> vbias, double mass_nom, ValueType type);

// fit mw 

pair<double,double> fitmW(vector<TH1F*> vtemp, vector<double> vbias, TH1* hdata);

// write to txt file 

int InputCombi(double mass_nom, double err_nom, vector<TH1*> vh, vector<double> sys_var, string inputname);

// ... Cw/z uncertainties

// ... unfolding

// ... etc...
