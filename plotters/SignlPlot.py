import ROOT
import math
import os
import numpy
from numpy import array
import array
import sys

RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()

def FindAndSetMax(*args):
    if len(args) == 1: args = args[0]
    maximum = 0.0
    for i in args:
        i.SetStats(0)
        t = i.GetMaximum()
        if t > maximum:
            maximum = t

def MakeNBinsFromMinToMax(N,Min,Max):
    BINS = []
    for i in range(N+1):
        BINS.append(Min+(i*(Max-Min)/N))
    return BINS

def Plotter(File, trees, cols, weight, cutsel, bins, var, name, atitle, branch):


    if var is "evt_aM" and ("TTBAR" in name):
        L = ROOT.TLegend(0.2, 0.6, 0.4, 0.89)
    elif var is "evt_XM" and ("X3000" in name):
        L = ROOT.TLegend(0.2, 0.6, 0.4, 0.89)
    else:
        L = ROOT.TLegend(0.7, 0.7, 0.89, 0.89)
    L.SetLineColor(0)
    L.SetFillColor(0)

    Fnom = RDF(trees[0], File)

    rdfnom_w = Fnom.Define("total_weight", weight)
    rdfup_w = Fnom.Define("total_weight_up", weight + "*weight_BBMT_up")
    rdfdn_w = Fnom.Define("total_weight_dn", weight + "*weight_BBMT_dn")

    histnom = rdfnom_w.Filter(cutsel)
    plotnom = histnom.Histo1D((var+"nom", ";"+name+"nom"+";Events", len(bins)-1, numpy.array(bins)), var, "total_weight")
    #        plot.Scale(1/plot.Integral())
    plotnom.SetStats(0)
    plotnom.GetXaxis().SetTitle(name+" "+atitle)
    plotnom.GetYaxis().SetTitleOffset(1.5)
    plotnom.SetLineColor(cols[0])
    plotnom.SetLineWidth(2)
    nomnew = plotnom.DrawCopy()
    nomnew2 = nomnew.Clone("nominal")
    nomnewratu = nomnew.Clone("nomrat")
    nomnewratd = nomnew.Clone("nomrat")

    L.AddEntry(nomnew2, "nominal", "l")
    L.AddEntry(upnew2, branch+" Up", "l")
    L.AddEntry(dnnew2, branch+" Down", "l")

    u = ROOT.TCanvas(name+"_"+var, "", 400, 400)

    u.cd()
    
    nomnew2.Draw("hist")
    upnew2.Draw("histsame")
    dnnew2.Draw("histsame")
    L.Draw("same")
    p22.cd()
    nomnewratu.GetXaxis().SetTitleSize(0.1925)
    nomnewratu.GetXaxis().SetLabelSize(0.16)
    nomnewratu.GetXaxis().SetTitleOffset(0.84)
    nomnewratu.GetYaxis().SetTitleSize(0.1)
    nomnewratu.GetYaxis().SetLabelSize(0.12)
    nomnewratu.GetYaxis().SetTitleOffset(0.5)
    nomnewratu.Draw("hist")
    nomnewratd.GetXaxis().SetTitleSize(0.1925)
    nomnewratd.GetXaxis().SetLabelSize(0.16)
    nomnewratd.GetXaxis().SetTitleOffset(0.84) 
    nomnewratd.GetYaxis().SetTitleSize(0.1)
    nomnewratd.GetYaxis().SetLabelSize(0.12)
    nomnewratd.GetYaxis().SetTitleOffset(0.5)
    nomnewratd.Draw("histsame")
    line.Draw("same")

#    print "down entries = " + str(dnnew2.GetEntries())
#    print "up entries = " + str(upnew2.GetEntries())
#    print "nom entries = " + str(nomnew2.GetEntries())
    

    u.Print(branch+"/"+var+"_"+name+"_"+branch+".pdf")

    print "done with " + name

if __name__=="__main__":


    cuts16 = "evt_HT>900. && J2pt>300 && evt_Masym<0.1 && evt_Deta < 1.5 && J2dbtag > 0.8 && J1dbtag>0.8 && J2SDM > 12.5"
    cuts17 = "evt_HT>1200. && J2pt>300 && evt_Masym<0.1 && evt_Deta < 1.5 && J2dbtag > 0.8 && J1dbtag>0.8 && J2SDM > 12.5"
    
    aMbins = MakeNBinsFromMinToMax(40 ,15., 215.)
    XMbins = MakeNBinsFromMinToMax(30 , 500., 3500.)
    ttbaraMbins = MakeNBinsFromMinToMax(20, 15., 215.)
    ttbarXMbins = MakeNBinsFromMinToMax(20, 500., 3500.)


    tree_list = ["tree_nominal"]
    color_list = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]

    XM = ["1000", "1500", "2000", "2500", "3000"]
    aM = ["25", "30", "50", "70", "80", "100"]

    for X in XM:
        for a in aM:
#            if X is "2500" and a is "100": continue
#            elif X is "3000" and a is "25": continue
#            else:
            samp18 = "/cms/xaastorage/PicoTrees/2018/April2020v6/X"+X+"A"+a+"y18_May25/X"+X+"A"+a+"y18_May25.root"
            nm18 = "X"+X+"a"+a+"y18"
#            samp17 = "/cms/xaastorage/PicoTrees/2017/April2020v6/X"+X+"A"+a+"y17_May25/X"+X+"A"+a+"y17_May25.root"
#            nm17 = "X"+X+"a"+a+"y17"
#                samp16 = "/cms/xaastorage/PicoTrees/2016/April2020v6/X"+X+"A"+a+"y16_May25/X"+X+"A"+a+"y16_May25.root"
#                nm16 = "X"+X+"a"+a+"y16"

#            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, aMbins, "evt_aM", nm18, "Average Jet Mass (GeV)", "PDF")
#            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, XMbins, "evt_XM", nm18, "X Mass (GeV)", "PDF")
#            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_trig", cuts17, aMbins, "evt_aM", nm18, "Average Jet Mass (GeV)", "MCvsData")
#            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_trig", cuts17, XMbins, "evt_XM", nm18, "X Mass (GeV)", "MCvsData")
#            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_PU", cuts17, aMbins, "evt_aM", nm18, "Average Jet Mass (GeV)", "PU")
#            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_PU", cuts17, XMbins, "evt_XM", nm18, "X Mass (GeV)", "PU")
            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, aMbins, "evt_aM", nm18, "Average Jet Mass (GeV)", "bb")
            Plotter(samp18, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, XMbins, "evt_XM", nm18, "X Mass (GeV)", "bb")

##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, aMbins, "evt_aM", nm17, "Average Jet Mass (GeV)", "PDF")
##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, XMbins, "evt_XM", nm17, "X Mass (GeV)", "PDF")
##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_trig", cuts17, aMbins, "evt_aM", nm17, "Average Jet Mass (GeV)", "MCvsData")
##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_trig", cuts17, XMbins, "evt_XM", nm17, "X Mass (GeV)", "MCvsData")
##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_PU", cuts17, aMbins, "evt_aM", nm17, "Average Jet Mass (GeV)", "PU")
##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_PU", cuts17, XMbins, "evt_XM", nm17, "X Mass (GeV)", "PU")
##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, aMbins, "evt_aM", nm17, "Average Jet Mass (GeV)", "bb")
##            Plotter(samp17, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts17, XMbins, "evt_XM", nm17, "X Mass (GeV)", "bb")

##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts16, aMbins, "evt_aM", nm16, "Average Jet Mass (GeV)", "PDF")
##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts16, XMbins, "evt_XM", nm16, "X Mass (GeV)", "PDF")
##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_trig", cuts16, aMbins, "evt_aM", nm16, "Average Jet Mass (GeV)", "MCvsData")
##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_trig", cuts16, XMbins, "evt_XM", nm16, "X Mass (GeV)", "MCvsData")
##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_PU", cuts16, aMbins, "evt_aM", nm16, "Average Jet Mass (GeV)", "PU")
##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT*weight_PU", cuts16, XMbins, "evt_XM", nm16, "X Mass (GeV)", "PU")
##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts16, aMbins, "evt_aM", nm16, "Average Jet Mass (GeV)", "bb")
##            Plotter(samp16, tree_list, color_list, "weight_PU*weight_xsN*weight_BBMT", cuts16, XMbins, "evt_XM", nm16, "X Mass (GeV)", "bb")
