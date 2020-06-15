#!/bin/bash

cluster=$1
process=$2

# CMSSW setup etc
export SCRAM_ARCH="slc7_amd64_gcc900"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh

cd /home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/PICOTREE_ADDED_DEEPBBTAGHbb/2016/DATA/
eval `scramv1 runtime -sh`

python RUN_picotree_data_$2.py >& /home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/PICOTREE_ADDED_DEEPBBTAGHbb/2016/DATA/condor_logfiles_forData/data_logfile_$1_$2.log
