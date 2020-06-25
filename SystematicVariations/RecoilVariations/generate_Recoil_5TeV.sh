#!/bin/bash
NominalPath="/eos/user/h/hatmani/likelihoodfits_wmass/"
HistoVersion="prepare_and_study_systematics/"
Channel="InputFiles/"
Variation="5TeV_Wminusenu_RecoilVar/"
NominalFile="mc16_5TeV.361103.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wminusenu.e4916_s3238_r10243_r10210_p3665"

varRESOLUTION_STAT0_DOWNbin="varRESOLUTION_STAT0_DOWNbin"
varRESOLUTION_STAT1_DOWNbin="varRESOLUTION_STAT1_DOWNbin"
varRESOLUTION_SYS_DOWNbin="varRESOLUTION_SYS_DOWNbin"
varRESOLUTION_EXTSYS_DOWNbin="varRESOLUTION_EXTSYS_DOWNbin"

varRESPONSE_STAT0_DOWNbin="varRESPONSE_STAT0_DOWNbin"
varRESPONSE_STAT1_DOWNbin="varRESPONSE_STAT1_DOWNbin"
varRESPONSE_SYS_DOWNbin="varRESPONSE_SYS_DOWNbin"
varRESPONSE_EXTSYS_DOWNbin="varRESPONSE_EXTSYS_DOWNbin"

varSET_SYSbin="varSET_SYSbin"

#********************************************************************************************************************************
#***********************************************    Wminus enu 5TeV    **********************************************************
#********************************************************************************************************************************

# var 1
for i in `seq 1 12`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESOLUTION_STAT0_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESOLUTION_STAT0.list
done

# var 2
for i in `seq 1 12`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESOLUTION_STAT1_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESOLUTION_STAT1.list
done

# var 3
for i in `seq 1 1`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESOLUTION_SYS_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESOLUTION_SYS.list
done

# var 4
for i in `seq 1 1`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESOLUTION_EXTSYS_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESOLUTION_EXTSYS.list
done

# var 5
for i in `seq 1 20`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESPONSE_STAT0_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESPONSE_STAT0.list
done

# var 6
for i in `seq 1 20`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESPONSE_STAT1_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESPONSE_STAT1.list
done

# var 7
for i in `seq 1 1`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESPONSE_SYS_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESPONSE_SYS.list
done

# var 8
for i in `seq 1 1`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varRESPONSE_EXTSYS_DOWNbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varRESPONSE_EXTSYS.list
done

# var 9
for i in `seq 1 1`;
do
echo "${NominalPath}${HistoVersion}${Channel}${Variation}${NominalFile}_${varSET_SYSbin}$i.root" >> Recoil_Variation_Wminusenu5.list #Recoil_Variation_Wminusenu5_varSET_SYS.list
done


