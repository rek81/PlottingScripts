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


def makeplot(files, tree, var, weight, cuts, isdata):

    listofplots = []
    for i in files:
        Fd = RDF(tree, i)

    rdfd_w = Fd.Define("total_weightd", weight)

    for v in var:
        
        histd = rdfd_w.Filter(cuts)
        if isdata:
            plotd = histd.Histo1D((v[0]+"d", ";"+v[2]+";Events", v[1][0], v[1][1], v[1][2]), v[0], "total_weightd")
        else:
            plotd = histd.Histo1D((v[0]+"mc", ";"+v[2]+";Events", v[1][0], v[1][1], v[1][2]), v[0], "total_weightd")

        plotd.SetStats(0)
        plotd.GetXaxis().SetTitle(v[2])
        plotd.GetYaxis().SetTitleOffset(1.5)
        plotd.SetLineWidth(2)
        plotd.SetMarkerSize(2)
        plotd.SetMinimum(1)
        
        dnew = plotd.GetValue()
        dnew.SetMinimum(1)
        if isdata:
            clone = dnew.Clone("histd")
        else:
            clone = dnew.Clone("histmc")

        name = v[0]
        plots = (clone, name, var)
        listofplots.append(plots)
        
    return listofplots
 

def Plotter(mchist, dhist):

    
    for d in dhist:
        for mc in mchist:
#            if d[2][0] == mc[2][0]:
#                print d[2][0] 
#                print mc[2][0]
                dnew2 = d[0].Clone("rat")
                dnew2.Divide(mc[0])
                dnew2.GetYaxis().SetTitle("DATA/MC")
                dnew2.GetXaxis().SetTitle(" ")
                dnew2.GetYaxis().SetLabelSize(0.1)
                dnew2.GetYaxis().SetLabelOffset(0.005)
                dnew2.GetYaxis().SetTitleSize(0.15)
                dnew2.GetYaxis().SetTitleOffset(0.2)
                
                
                FindAndSetMax(d[0], mc[0])
                
                L = TLegend(0.6, 0.6, 0.89, 0.89)
                L.SetFillColor(0)
                L.SetLineColor(0)
                L.AddEntry(mc[0], "2016 Background Monte Carlo", "l")
                L.AddEntry(d[0], "2016 JetHT Data", "p")
                
                
                flat = TLine(float(d[2][0][1][2]), 1. , float(d[2][0][1][2]), 1.)
                
                C = TCanvas(d[1], "", 500, 500)
                #        C.SetLogy()
                Plot = TPad("plot", " ", 0, 0.2, 1, 1)
                rat = TPad("rat", " ", 0, 0, 1.0, 0.2)
                Plot.Draw()
                rat.Draw()
                Plot.cd()
                mc[0].Draw("hist")
                d[0].Draw("esame") 
                #        Plot.SetLogy()
                L.Draw("same")
                
                rat.cd()
                dnew2.Draw("e")
                #       flat.Draw()
                C.Print("PLOTS/TEST"+d[1]+".root")
                C.Print("PLOTS/TEST"+d[1]+".pdf")
                #    C.Delete()
        
                #    return C
        
if __name__ == "__main__":
        
    dist = [["evt_HT", [260, 900, 3500], "HT"]]
#    dist = [["evt_HT", [260, 900, 3500], "HT"],["evt_Masym", [20, 0, 1], "Mass Asymmetry"], ["evt_Deta", [12, 0, 6], "#Delta#eta"],["J1pt", [300, 300, 3300], "Leading Jet p_{T}"], ["J1eta", [12, -3, 3], "Leading Jet #eta"],["J1SDM", [25, 0, 250], "Leading Jet Mass (GeV)"],["J1dbtag", [40, -1, 1], "Leading Jet Double b Tag (Hbb)"], ["J1DeeptagMD_Hbb", [20, 0, 1], "Leading Jet Double b Tag (Deep Decorrelated Hbb)"],["J2pt", [300, 300, 3300], "Subeading Jet p_{T}"], ["J2eta", [12, -3, 3], "Subleading Jet #eta"],["J2SDM", [25, 0, 250], "Subleading Jet Mass (GeV)"],["J2dbtag", [40, -1, 1], "Subleading Jet Double b Tag (Hbb)"], ["J2DeeptagMD_Hbb", [20, 0, 1], "Subleading Jet Double b Tag (Deep Decorrelated Hbb)"]]#, ["PV", [12, 0, 60], "Primary Vertex"]]




    Cuts = "evt_HT>900.&&J1pt>300.&&J2pt>300.&&abs(J1eta)<2.4&&abs(J2eta)<2.4"
#    Weight_MC = "35900.*weight_xsN*weight_trig*weight_PU"
    Weight_MC = "0.9*3590000*weight_xsN*weight_trig*weight_PU"
    Weight_DATA = "1.0"
    
    
    v100to1001 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_100to200y16_1_June2/QCDHT_100to200y16_1_June2.root"
    v100to1002 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_100to200y16_2_June2/QCDHT_100to200y16_2_June2.root"
    v200to300 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_200to300y16_June2/QCDHT_200to300y16_June2.root"    
    v200to300ext1 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_200to300exty16_1_June2/QCDHT_200to300exty16_1_June2.root"
    v200to300ext2 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_200to300exty16_2_June2/QCDHT_200to300exty16_2_June2.root"
    v300to5001 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_300to500y16_1_June2/QCDHT_300to500y16_1_June2.root"
    v300to5002 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_300to500y16_2_June2/QCDHT_300to500y16_2_June2.root"
    v300to500ext = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_300to500exty16_June2/QCDHT_300to500exty16_June2.root"
    v500to7001 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_500to700y16_1_June2/QCDHT_500to700y16_1_June2.root"
    v500to7002 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_500to700y16_2_June2/QCDHT_500to700y16_2_June2.root"
    v500to700ext = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_500to700exty16_June2/QCDHT_500to700exty16_June2.root"
    v700to1000 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_700to1000y16_June2/QCDHT_700to1000y16_June2.root"
    v700to1000ext1 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_700to1000exty16_1_June2/QCDHT_700to1000exty16_1_June2.root"
    v700to1000ext2 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_700to1000exty16_2_June2_rerun2/QCDHT_700to1000exty16_2_June2_rerun2.root"
    v1000to1500 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1000to1500y16_June2/QCDHT_1000to1500y16_June2.root"
    v1000to1500ext1 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1000to1500exty16_1_June2_rerun3/QCDHT_1000to1500exty16_1_June2_rerun3.root"
    v1000to1500ext2 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1000to1500exty16_2_June2/QCDHT_1000to1500exty16_2_June2.root"
    v1500to2000 = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1500to2000y16_June2/QCDHT_1500to2000y16_June2.root"
    v1500to2000ext = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_1500to2000exty16_June2_rerun3/QCDHT_1500to2000exty16_June2_rerun3.root"
    v2000toInf = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_2000toInfy16_June2/QCDHT_2000toInfy16_June2.root"
    v2000toInfext = "/cms/xaastorage/PicoTrees/2016/April2020v6/QCDHT_2000toInfexty16_June2/QCDHT_2000toInfexty16_June2.root"


    Bv1 = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016Bv1_June2/JetHT_2016Bv1_June2.root"
    Bv2 = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016Bv2_June2/JetHT_2016Bv2_June2.root"
    C = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016C_June2/JetHT_2016C_June2.root"
    D = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016D_June2/JetHT_2016D_June2.root"
    E = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016E_June2/JetHT_2016E_June2.root"
    F = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016F_June2/JetHT_2016F_June2.root"
    G = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016G_June2/JetHT_2016G_June2.root"
    H = "/cms/xaastorage/PicoTrees/2016/April2020v6/JetHT_2016H_June2/JetHT_2016H_June2.root"

    TT = "/cms/xaastorage/PicoTrees/2016/April2020v6/TTBAR_y16_June2/TTBAR_y16_June2.root"



    qcdfiles = [v100to1001, v100to1002, v200to300, v200to300ext1, v200to300ext2, v300to5001, v300to5002, v300to500ext, v500to7001, v500to7002, v500to700ext, v700to1000, v700to1000ext1, v700to1000ext2, v1000to1500, v1000to1500ext1, v1000to1500ext2, v1500to2000, v1500to2000ext, v2000toInf, v2000toInfext, TT]
    
    datafiles = [Bv1, Bv2, C, D, E, F, G, H]

    mc = makeplot(qcdfiles,"tree_nominal", dist, Weight_MC, Cuts, False)
    dat = makeplot(datafiles,"tree_nominal", dist, "1.0", Cuts, True)

    Plotter(mc, dat)
