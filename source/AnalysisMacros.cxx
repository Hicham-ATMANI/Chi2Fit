#include "AnalysisMacros.h"
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include "TString.h"
#include "TMath.h"
#include <map>
#include <stdio.h>      
#include <stdlib.h>     
using namespace std;

vector<TH1*> getHistVariations(TFile* f, string dirname, string hname, string suffix){
   
  f->cd((dirname).c_str());
  TDirectory *current_dir = gDirectory;
  TList* list = current_dir->GetListOfKeys() ;
  if (!list) { printf("<getHistVar> No keys found in file\n") ; exit(1) ; }
  TIter next(list) ;
  TKey* key ;
  TObject* obj ;
  vector<TH1*> vTemp;
  
  while ( (key = (TKey*)next()) ) {
    string histoname = ((TH1*)key->ReadObj())->GetName(); 
    if (histoname.find((hname+"_cut8_").c_str())!= std::string::npos)   
      { 
	if (histoname.find("2muPt")     != std::string::npos) continue; 
        if (histoname.find("truth")     != std::string::npos) continue;
        if (histoname.find("elPt_Reco") != std::string::npos) continue;

	//cout << histoname << endl;
	// mstw 2008 
	if (histoname.find((hname+"_cut7_PDFset2115").c_str())!= std::string::npos || histoname.find((hname+"_cut7_PDFset2116").c_str())!= std::string::npos || histoname.find((hname+"_cut7_PDFset2117").c_str())!= std::string::npos || histoname.find((hname+"_cut7_PDFset2118").c_str())!= std::string::npos || histoname.find((hname+"_cut7_PDFset2119").c_str())!= std::string::npos) continue;  //{
	cout << histoname << endl;     
	vTemp.push_back( (TH1*)key->ReadObj()); 	
	//} // mstw 
      }
  }
  return vTemp; 
}



vector<TH1*> getTemplates(TFile* f, string dirname, string hname, vector<double>& v){
  
  f->cd((dirname).c_str());
  TDirectory *current_dir = gDirectory;
  TList* list = current_dir->GetListOfKeys() ;
  if (!list) { printf("<getTemplates> No keys found in file\n") ; exit(1) ; }
  TIter next(list) ;
  TKey* key ;
  TObject* obj ;
  vector<TH1*> vTemp;
  
  while ( (key = (TKey*)next()) ) {
    string histoname = ((TH1*)key->ReadObj())->GetName();
    
    if ( (histoname.find((hname+"_cut8_").c_str())!= std::string::npos) && (histoname.find("dG000")!= std::string::npos))
      { 
	if (histoname.find("2muPt")     != std::string::npos) continue;         
	if (histoname.find("truth")     != std::string::npos) continue;
        if (histoname.find("elPt_Reco") != std::string::npos) continue;

	vTemp.push_back( (TH1*)key->ReadObj());
	std::string start_delim = "dM";
	std::string stop_delim = "_dG000";

	unsigned first_delim_pos = histoname.find(start_delim);
	unsigned end_pos_of_first_delim = first_delim_pos + start_delim.length();
	unsigned last_delim_pos = histoname.find(stop_delim);

	string partbias = histoname.substr(end_pos_of_first_delim,
					   last_delim_pos - end_pos_of_first_delim); 
	std::string::size_type sz; 
	double bias = stod(partbias,&sz); 

	v.push_back(bias);
      }
  }
  return vTemp;

}



double compute_chi2(TH1* a, TH1* b)
{
  int nb_bins = a->GetNbinsX();
  if(nb_bins != b->GetNbinsX()) {
    cout << "Issue : only support same nb of bins" << endl;
    exit(1);
  }

  double chi2res = 0;

  for(int id = 0 ; id < nb_bins ; id++) {
    double cent = a->GetBinCenter(id+1);
    if (cent> 50000 || cent <30000) continue;
    double diff = a->GetBinContent(id+1)-b->GetBinContent(id+1);
    double err2 = (a->GetBinError(id+1)*a->GetBinError(id+1));
    err2 += (b->GetBinError(id+1)*b->GetBinError(id+1));
    if (err2==0) {cout << " cent " << cent << " bin " << id+1 << " diff " << diff << " error 1 " << a->GetBinError(id+1) << " error 2 " << b->GetBinError(id+1) << endl; continue;}
    double curr = diff*diff/err2;
    chi2res += curr;
    
  }

  return chi2res;
}

pair<double,double> fitmW(vector<TH1*> vtemp, vector<double> vbias, TH1* hdata) {

  TF1 fpol("fpol","(x-[0])*(x-[0])/[1]/[1] + [2]",80300,80500);
  //TF1 fpol("fpol","pol2",80300,80500);

  pair<double,double> pdd;
  
  TGraph graph(vtemp.size());

  for(unsigned int i=0; i<vtemp.size(); i++){
    graph.SetPoint(i, 80400+vbias[i], hdata->Chi2Test(vtemp[i], "CHI2WW"));
    //    if (i==0) cout << " chi 2 test " << hdata->Chi2Test(vtemp[i], "CHI2WW") << endl; 
    //graph.SetPoint(i, 80400+vbias[i],compute_chi2(hdata, vtemp[i])); 
    //    if (i==0) cout << " chi 2 test " << hdata->Chi2Test(vtemp[i], "CHI2WW") <<  " chi2 a la main " << compute_chi2(hdata, vtemp[i]) << endl;    
  }
  
  fpol.SetParameter(0,80400);
  fpol.SetParameter(1,10);
  fpol.SetParameter(2,1.);

  graph.Fit("fpol","rQ");
  graph.Fit("fpol","rQ");
  graph.Fit("fpol","rQ");

  pdd.first  = fpol.GetParameter(0);
  pdd.second = fpol.GetParameter(1);

  cout<<"Nominal : "<<fpol.GetParameter(0)<<endl;
  cout<<"Stat error : "<<fpol.GetParameter(1)<<endl;

  return pdd;
}


vector<double> deltaMw(vector<TH1*> vdata, vector<TH1*> vtemp, vector<double> vbias, double mass_nominal, ValueType type){
  
  vector<double> dmW_val; 
  vector<double> dmW_err;
  
  string dataname = (vdata[0]->GetName()); 

  cout << " data name " << dataname << endl;
  if ( dataname.find("PDFset108")!= std::string::npos) { 
  cout<<" pdf "<<endl;
  }
  else{ 
    for (unsigned int k=1; k<vdata.size(); k++){

      TGraph graph(vtemp.size());
      TF1 fpol("fpol","(x-[0])*(x-[0])/[1]/[1] + [2]",80300,80500);


      for(unsigned int i=0; i<vtemp.size(); i++) {
	graph.SetPoint(i, 80400+vbias[i], vdata[k]->Chi2Test(vtemp[i], "CHI2WW"));
      }


      fpol.SetParameter(0,80400);
      fpol.SetParameter(1,10);
      fpol.SetParameter(2,1.);

      graph.Fit("fpol","rQ");
      graph.Fit("fpol","rQ");
      graph.Fit("fpol","rQ");


      dmW_val.push_back(fpol.GetParameter(0) - mass_nominal); // better m nominal                                                                                                                          
      dmW_err.push_back(fpol.GetParameter(1)); // ? // mw error not dmw                                                                                                                                    
    }
  }


  switch(type)
     {
     case kValue  : return dmW_val;   break;
     case kErr: return dmW_err; break;
     }


} 

double getError(vector<double> v, VariationType vtype, double scale){ 
  
  double Verrp = 0;
  double Verrm = 0; 

  for (unsigned int i=0; i<v.size(); i++){
    switch(vtype)
      {
      case kOffset : if(v[i]>0) Verrp += v[i]*v[i]/scale/scale; else Verrm += v[i]*v[i]/scale/scale;
      case kToys: Verrp += 0; 
      }
  } 
  return (sqrt(Verrp)+sqrt(Verrm))/2.;
}


double getCorrelation(vector<double> v1, vector<double> v2){
  // matrice de correlation pour le cas inclusif pour le moment 
  double cov = 0; 
  double corr = 0; 
  double sigma_1, sigma_2; 
  if (v1.size() != v2.size()) cout << " something wrong" << endl; //  

  for (unsigned int i=0; i<v1.size(); i++)
    { cov += v1[i]*v2[i]; // inclusive case
      sigma_1 += v1[i]*v1[i]; 
      sigma_2 += v2[i]*v2[i];
    }
  cout << " cov " << cov << " and sqrt(sigma_1) " << sqrt(sigma_1) << " and sqrt(sigma_2) " << sqrt(sigma_2) << endl;
  corr = cov / (sqrt(sigma_1)*sqrt(sigma_2));
  //  cout << " la correlation " << corr << endl; 
  return corr; 
}


TMatrixDSym getCovariance(vector<double> v1, vector<double> v2){ 
  TMatrixDSym cov(2);   
  if (v1.size() != v2.size()) cout << " something wrong" << endl;
  for (unsigned int i=0; i<v1.size(); i++)                                                                                                                                                                
    { cov(0,1) += v1[i]*v2[i]; // inclusive case   
      cov(1,0) += v1[i]*v2[i];
      cov(0,0)+= v1[i]*v1[i];
      cov(1,1)+= v2[i]*v2[i];
    }
  return cov;
}
/*
double getCorrelation(){

}

*/


int InputCombi(double mass_nom, double err_nom, vector<TH1*> vh, vector<double> sys_var, string inputname, string chargename, string channelname) {
  
  gSystem->Exec(Form("mkdir -p ./TevFiles_7TeV_smeared/%s", inputname.c_str()));
  
  cout << " inputname " << inputname << " charge name " << chargename << " channel  " << channelname << endl;
  TString charge_name, obs_name, channel_name, cat_name;  
  if (chargename.find("minus")!=std::string::npos) charge_name ="mi";
  else if (chargename.find("pl")!=std::string::npos) charge_name = "pl";
  if (chargename.find("Ptsmeared")!=std::string::npos) obs_name = "ptl3050";
  else if (chargename.find("mTSmeared")!=std::string::npos) obs_name= "mtw65100";
  if (chargename.find("eta1")!=std::string::npos) cat_name = "eta1";
  else if (chargename.find("eta2")!=std::string::npos) cat_name = "eta2";
  else if (chargename.find("eta3")!=std::string::npos) cat_name = "eta3"; 
  else if (chargename.find("eta4")!=std::string::npos) cat_name = "eta4"; 
  if (channelname == "muons") channel_name = "Wmunu";
  else if (channelname =="electrons") channel_name = "Wenu"; 

  ofstream ofs(("TevFiles_7TeV_smeared/"+inputname+"/"+channel_name+"_"+charge_name+"_"+cat_name+"_muA_"+obs_name+".txt"));

  cout << " writing to TevFiles_7TeV_smeared/"+inputname+"/"+channel_name+"_"+charge_name+"_"+cat_name+"_muA_"+obs_name+".txt" << endl;

  cout << " masse nominale " << mass_nom << " erreur nominale " << err_nom << endl;
  double scale68 =1.; 
  if (inputname.find("PDFset108")!= std::string::npos || inputname.find("PDFset110")!= std::string::npos || inputname.find("PDFset130")!= std::string::npos || inputname.find("PDFset105")!= std::string::npos || inputname.find("PDFset112")!= std::string::npos) scale68 =1.645;
  ofs << "Nominal" << " \t " << mass_nom << " \t " << err_nom << endl;
  for(unsigned int kid=0; kid<sys_var.size(); kid=kid+2) {                                                                                                                                                 
    cout << " sys var size  " << sys_var.size() << endl;
    string name_sys ; 
    if (inputname.find("PDFset108")!= std::string::npos) 
      name_sys  = (vh[kid])->GetName(); 
    else 
      name_sys  = (vh[kid+1])->GetName(); 
    cout << " name sys " << name_sys << endl;
    
    unsigned first_pos = name_sys.find(inputname);

    string sysname = name_sys.substr(first_pos); 
    cout << " substr sysname " << sysname << endl;
    ofs << sysname << " \t " << (sys_var[kid])/scale68 << " \t " << (sys_var[kid+1])/scale68 << endl;
  }
  
  ofs.close();
  
  return 0;
}

