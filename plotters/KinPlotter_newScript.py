import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import sys
import Plotting_Header
from Plotting_Header import *

def MakeKinPlots(F, N):
	print " -------------------- Making KinPlots for " + N
	print " -------------------- Creating Histograms"
	outfile = TFile("Hists_"+N+".root", "recreate")
	
	#uncut
	avg_mass = TH2F("avgMassvsEta1", "", 80, 0, 400, 20, -3, 3)
	avg_mass.GetXaxis().SetTitle("Average Soft Drop Mass")
	avg_mass.GetXaxis().SetTitleSize(0.045)
	avg_mass.GetYaxis().SetTitle("Events")
	avg_mass.GetYaxis().SetTitleSize(0.045)



	infile=ROOT.TFile(F)
	T = infile.Get("tree_nominal")
	nent = T.GetEntries()
	print " -------------------- Starting Event Loop: " + str(nent) + " entries"
	for i in range(nent):
		T.GetEntry(i)



	#Defining Variables
		ETA_0 = T.J1eta
                AVG_MASS = T.evt_aM

	#Filling Histograms
		avg_mass.Fill(AVG_MASS, AVG_MASS, ETA_0)



	print " "
	print " -------------------- Creating Plots"



	outfile.cd()
	outfile.Write()
	outfile.Close()

#choices = if 

from optparse import OptionParser


parser = OptionParser()

parser.add_option('-n', '--name', metavar='NAME', type='string', dest='n', help="The name of the output file, minus the .root.")
parser.add_option('-f', '--file', metavar='FILES', type='string', dest='files', help="Location of the ntuples to run over.")

(options, args) = parser.parse_args()

MakeKinPlots(options.files, options.n)	

