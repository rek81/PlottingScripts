import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import sys
from optparse import OptionParser
import glob

RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()


def FindAndSetMax(*args):
    maximum = 0.0
    for i in args:
        t = i.GetMaximum()
        if t > maximum:
            maximum = t
    for j in args:
        j.GetYaxis().SetRangeUser(0,maximum*1.375) # takes a set of histograms, sets their Range to show all of them

 

def Plotter(mcFile, dFile, trees, weight, cutsel, var):
    

    for i in mcFile:
        Fmc = RDF(trees, i)
    for i in dFile:
        Fd = RDF(trees, i)

    rdfd_w = Fd.Define("total_weightd", "1.")
    rdfmc_w = Fmc.Define("total_weightmc", weight)

    for v in var:
        
        histd = rdfd_w.Filter(cutsel)
        plotd = histd.Histo1D((v[0]+"d", ";"+v[2]+";Events", v[1][0], v[1][1], v[1][2]), v[0], "total_weightd")
        plotd.SetStats(0)
        plotd.GetXaxis().SetTitle(v[2])
        plotd.GetYaxis().SetTitleOffset(1.5)
        plotd.SetLineWidth(2)
        plotd.SetMarkerSize(2)
        dmax = plotd.GetMaximum()
#        dnew = plotd.DrawCopy()
        dnew = plotd.GetValue()
        dnew.GetYaxis().SetRangeUser(1, dmax)
        dnew2 = dnew.Clone("rat")   
#        print  dnew.Integral()
        
        
        histmc = rdfmc_w.Filter(cutsel)
        plotmc = histmc.Histo1D((v[0]+"mc", ";"+v[2]+";Events", v[1][0], v[1][1], v[1][2]), v[0], "total_weightmc")
        plotmc.SetStats(0)
        plotmc.GetXaxis().SetTitle(v[2])
        plotmc.GetYaxis().SetTitleOffset(1.5)
        plotmc.SetLineColor(kRed)
        plotmc.SetLineWidth(2)
        mcmax = plotmc.GetMaximum()
        mcnew = plotmc.GetValue()
        mcnew.GetYaxis().SetRangeUser(1, mcmax)
           

        dnew2.Divide(mcnew)
        dnew2.GetYaxis().SetTitle("DATA/MC")
        dnew2.GetXaxis().SetTitle(" ")
        dnew2.GetYaxis().SetLabelSize(0.1)
        dnew2.GetYaxis().SetLabelOffset(0.005)
        dnew2.GetYaxis().SetTitleSize(0.15)
        dnew2.GetYaxis().SetTitleOffset(0.2)
        

        FindAndSetMax(dnew, mcnew)

        L = TLegend(0.6, 0.6, 0.89, 0.89)
        L.SetFillColor(0)
        L.SetLineColor(0)
        L.AddEntry(mcnew, "2016 Background Monte Carlo", "l")
        L.AddEntry(dnew, "2016 JetHT Data", "p")

        flat = TLine(float(v[1][1]), 1. , float(v[1][2]), 1.)

        C = TCanvas(v[0], "", 500, 500)
        Plot = TPad("plot", " ", 0, 0.2, 1, 1)
        rat = TPad("rat", " ", 0, 0, 1.0, 0.2)
        Plot.Draw()
        rat.Draw()
        Plot.cd()
        Plot.SetLogy()
        mcnew.Draw("hist")
        dnew.Draw("esame")
        L.Draw("same")
        
        rat.cd()
        dnew2.Draw("e")
        flat.Draw()
        C.Print("PLOTS/"+v[0]+".root")
        C.Print("PLOTS/"+v[0]+".pdf")
        C.Delete()



dist = [["evt_HT", [260, 900, 3500], "HT"],["evt_Masym", [20, 0, 1], "Mass Asymmetry"], ["evt_Deta", [12, 0, 6], "#Delta#eta"],["J1pt", [300, 300, 3300], "Leading Jet p_{T}"], ["J1eta", [12, -3, 3], "Leading Jet #eta"],["J1SDM", [25, 0, 250], "Leading Jet Mass (GeV)"],["J1dbtag", [40, -1, 1], "Leading Jet Double b Tag (Hbb)"], ["J1DeeptagMD_Hbb", [20, 0, 1], "Leading Jet Double b Tag (Deep Decorrelated Hbb)"],["J2pt", [300, 300, 3300], "Subeading Jet p_{T}"], ["J2eta", [12, -3, 3], "Subleading Jet #eta"],["J2SDM", [25, 0, 250], "Subleading Jet Mass (GeV)"],["J2dbtag", [40, -1, 1], "Subleading Jet Double b Tag (Hbb)"], ["J2DeeptagMD_Hbb", [20, 0, 1], "Subleading Jet Double b Tag (Deep Decorrelated Hbb)"], ["PV", [12, 0, 60], "Primary Vertex"]]




#Cuts = " "
#Cuts = "evt_HT>900.&J1pt>300.&J2pt>300.&abs(J1eta)<2.4&abs(J2eta)<2.4"
Cuts = "evt_HT>900.&&J1pt>300.&&J2pt>300.&&abs(J1eta)<2.4&&abs(J2eta)<2.4"
Weight_MC = "35900.*weight_xsN*weight_trig*weight_PU"
Weight_DATA = "1.0"



qcdfiles = ["/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1000to1500exty16_1_June2_rerun3/QCDHT_1000to1500exty16_1_June2_rerun3.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1000to1500exty16_2_June2/QCDHT_1000to1500exty16_2_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1000to1500y16_June2/QCDHT_1000to1500y16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_100to200y16_1_June2/QCDHT_100to200y16_1_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_100to200y16_2_June2/QCDHT_100to200y16_2_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_100to200y16_2_June2/QCDHT_100to200y16_2_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1500to2000y16_June2/QCDHT_1500to2000y16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1500to2000exty16_June2_rerun3/QCDHT_1500to2000exty16_June2_rerun3.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_2000toInfexty16_June2/QCDHT_2000toInfexty16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_2000toInfy16_June2/QCDHT_2000toInfy16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_200to300exty16_1_June2/QCDHT_200to300exty16_1_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_200to300exty16_2_June2/QCDHT_200to300exty16_2_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_200to300y16_June2/QCDHT_200to300y16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_300to500exty16_June2/QCDHT_300to500exty16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_300to500y16_1_June2/QCDHT_300to500y16_1_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_300to500y16_2_June2/QCDHT_300to500y16_2_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_500to700exty16_June2/QCDHT_500to700exty16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_500to700y16_1_June2/QCDHT_500to700y16_1_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_500to700y16_2_June2/QCDHT_500to700y16_2_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_700to1000exty16_2_June2_rerun2/QCDHT_700to1000exty16_2_June2_rerun2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_700to1000y16_June2/QCDHT_700to1000y16_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/TTBAR_y16_June2/TTBAR_y16_June2.root"]
    
datafiles = ["/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016Bv1_June2/JetHT_2016Bv1_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016Bv2_June2/JetHT_2016Bv2_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016C_June2/JetHT_2016C_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016D_June2/JetHT_2016D_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016E_June2/JetHT_2016E_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016F_June2/JetHT_2016F_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016G_June2/JetHT_2016G_June2.root", "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016H_June2/JetHT_2016H_June2.root"]

Plotter(qcdfiles, datafiles, "tree_nominal", Weight_MC, Cuts, dist)
