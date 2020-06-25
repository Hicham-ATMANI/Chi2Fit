#!/bin/bash
NominalPath="/eos/user/h/hatmani/likelihoodfits_wmass/"
HistoVersion="prepare_and_study_systematics/"
Channel="InputFiles/"
Variation="5TeV_Wminusenu_ElCalibVar/"
NominalFile="mc16_5TeV.361103.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wminusenu.e4916_s3238_r10243_r10210_p3665"
varC="varcDownbin"
varAlpha="varscaleDownbin"

#********************************************************************************************************************************
#***********************************************    Wminus enu 5TeV    **********************************************************
#********************************************************************************************************************************

# Nominal
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}.root" >> Calib_Nominal_Wminusenu5.list

# Variation of the Constant "C"
for i in `seq 1 24`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varC}$i.root" >> Calib_Variation_Wminusenu5_C.list
done

# Variation of the Scale "Alpha" 
for i in `seq 1 24`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varAlpha}$i.root" >> Calib_Variation_Wminusenu5_Alpha.list
done


