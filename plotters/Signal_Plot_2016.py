import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import sys
from optparse import OptionParser

def FindAndSetMax(*args):
    maximum = 0.0
    for i in args:
        t = i.GetMaximum()
        if t > maximum:
            maximum = t
    for j in args:
        j.GetYaxis().SetRangeUser(0,maximum*1.375) # takes a set of histograms, sets their Range to show all of them

def quickplot(File, tree, plot, var, Cut, Weight):
    temp = plot.Clone("temp")
    chain = TChain(tree)
    chain.Add(File)
#    proof = ROOT.TProof.Open("lite://", "workers=2")
#    fast = ROOT.TProofChain(chain, True)
#    fast.Draw(var + ">>" + "temp", "(" + Weight + ")*(" + Cut + ")", "goff")
    chain.Draw(var + ">>" + "temp", "(" + Weight + ")*(" + Cut + ")", "goff")
    plot.Add(temp)

#dist = [["weight_xsN", 20, 0, 1], ["weight_PU", 50, 0, 5], ["weight_PU_up", 50, 0, 5], ["weight_PU_dn", 50, 0, 5], ["weight_trig", 50, 0, 5], ["evt_ttVeto", 50, 0, 5], ["evt_ttRW", 50, 0, 5], ["evt_XM", 300, 250, 3250], ["evt_HT", 300, 500, 3500], ["evt_hhM", 300, 500, 3500], ["evt_aM", 80, 0, 250], ["evt_Masym", 20, 0, 1], ["evt_Deta", 60, 0, 6], ["evt_Dphi", 60, 0, 6], ["evt_DR", 60, 0, 6], ["J1pt", 300, 500, 3500], ["J1eta", 60, -3, 3], ["J1phi", 60, -3, 3], ["J1SDM", 80, 0, 250], ["J1sbtag", 20, 0, 1], ["J1dbtag", 20, 0, 1], ["J1tau21", 20, 0, 1], ["J1tau32", 20, 0, 1], ["J2pt", 300, 500, 3500], ["J2eta", 60, -3, 3], ["J2phi", 60, -3, 3], ["J2SDM", 80, 0, 250], ["J2sbtag", 20, 0, 1], ["J2dbtag", 20, 0, 1], ["J2tau21", 20, 0, 1], ["J2tau32", 20, 0, 1]]

Cuts = " "
#Cuts = "evt_HT>900.&J1pt>300.&J2pt>300.&abs(J1eta)<2.4&abs(J2eta)<2.4"
Cuts = "evt_HT>1200.&J1pt>300.&J2pt>300.&abs(J1eta)<2.4&abs(J2eta)<2.4&evt_Deta<1.5&evt_Masym>0.0&evt_Masym<0.1&J1dbtag>0.8&J2dbtag>0.8"
Weight_MC = "35900.*weight_xsN*weight_PU"
Weight_MC_qcd = "35900.*weight_xsN*weight_PU"
Weight_DATA = "1.0"

dist = [["evt_aM", 30, 0, 150, "Average Jet Mass (GeV)"], ["evt_XM", 65, 250, 3250, "Dijet Mass (GeV)"]]
#dist = [["evt_aM", 30, 0, 150, "Average Jet Mass (GeV)"]]
#dist = [["evt_XM", 65, 250, 3250, "Dijet Mass (GeV)"]]
#dist = [["evt_Deta", 10, 0, 5, "HT"]]
#dist = [["evt_HT", 300, 500, 3500, "HT"]]
#dist = [["J1pt", 100, 500, 1500, "Leading Jet p_{T}"], ["J2pt", 100, 500, 1500, "Sub Leading Jet p_{T}"], ["J1eta", 12, -3, 3, "Leading Jet #eta"], ["J2eta", 12, -3, 3, "Sub Leading Jet #eta"], ["evt_Masym", 20, 0, 1, "Mass Asymmetry"], ["evt_Deta", 10, 0, 5, "#Delta#eta"], ["J1dbtag", 20, -1, 1, "Leading Jet Double b Tag"], ["J2dbtag", 20, -1, 1, "Sub Leading Jet Double b Tag"], ["J1SDM", 25, 0, 250, "Leading Jet Soft Drop Mass"], ["J2SDM", 25, 0, 250, "Sub Leading Jet Soft Drop Mass"], ["evt_HT", 300, 500, 3500, "HT"]]
#dist = [["J1dbtag", 20, -1., 1.], ["J2dbtag", 20, -1., 1.], ["J1SDM", 25, 0., 250.], ["J2SDM", 25, 0., 250.]]

for d in dist:

    hist1 = TH1F(d[0]+"_1", "", d[1], d[2], d[3]) # QCD
    hist1.GetXaxis().SetTitle(d[4])
    hist1.GetYaxis().SetTitle("Events")
    hist1.SetStats(0)
    hist1.SetLineColor(kRed+3)
#    hist1.SetLineWidth(2)

    hist2 = TH1F(d[0]+"_2", "", d[1], d[2], d[3]) # DATA
    hist2.GetXaxis().SetTitle(d[4])
    hist2.GetYaxis().SetTitle("Events")
    hist2.SetStats(0)
    hist2.SetLineColor(kBlue+3)
#    hist2.SetLineWidth(2)

    hist3 = TH1F(d[0]+"_3", "", d[1], d[2], d[3]) # ttbar
    hist3.GetXaxis().SetTitle(d[4])
    hist3.GetYaxis().SetTitle("Events")
    hist3.SetStats(0)
    hist3.SetLineColor(kGreen+3)
#    hist3.SetLineWidth(2)


    hist4 = TH1F(d[0]+"_4", "", d[1], d[2], d[3]) # Drell Yan
    hist4.GetXaxis().SetTitle(d[4])
    hist4.GetYaxis().SetTitle("Events")
    hist4.SetStats(0)
    hist4.SetLineColor(kCyan+3)
#    hist4.SetLineWidth(2)


    hist5 = TH1F(d[0]+"_5", "", d[1], d[2], d[3]) # Single Top
    hist5.GetXaxis().SetTitle(d[4])
    hist5.GetYaxis().SetTitle("Events")
    hist5.SetStats(0)
    hist5.SetLineColor(kYellow+3)
#    hist5.SetLineWidth(2)


    hist6 = TH1F(d[0]+"_6", "", d[1], d[2], d[3]) # Single Antitop 
    hist6.GetXaxis().SetTitle(d[4])
    hist6.GetYaxis().SetTitle("Events")
    hist6.SetStats(0)
    hist6.SetLineColor(kMagenta+3)
#    hist6.SetLineWidth(2)


    hist7 = TH1F(d[0]+"_7", "", d[1], d[2], d[3]) # Single Top TChannel 
    hist7.GetXaxis().SetTitle(d[4])
    hist7.GetYaxis().SetTitle("Events")
    hist7.SetStats(0)
    hist7.SetLineColor(kRed+1)
#    hist7.SetLineWidth(2)


    hist8 = TH1F(d[0]+"_8", "", d[1], d[2], d[3]) # Single Antitop TChannel
    hist8.GetXaxis().SetTitle(d[4])
    hist8.GetYaxis().SetTitle("Events")
    hist8.SetStats(0)
    hist8.SetLineColor(kBlue+1)
#    hist8.SetLineWidth(2)
    

    hist9 = TH1F(d[0]+"_9", "", d[1], d[2], d[3]) # W+Jets starting at HT180evt_HT_pTbin.png
    hist9.GetXaxis().SetTitle(d[4])
    hist9.GetYaxis().SetTitle("Events")
    hist9.SetStats(0)
    hist9.SetLineColor(kGreen+1)
#    hist9.SetLineWidth(2)
###############################################################33    

    hist10 = TH1F(d[0]+"_10", "", d[1], d[2], d[3]) # ZZ to 4q
    hist10.GetXaxis().SetTitle(d[4])
    hist10.GetYaxis().SetTitle("Events")
    hist10.SetStats(0)
    hist10.SetLineColor(kCyan+1)

    hist11 = TH1F(d[0]+"_11", "", d[1], d[2], d[3]) # ZZ to 4q
    hist11.GetXaxis().SetTitle(d[4])
    hist11.GetYaxis().SetTitle("Events")
    hist11.SetStats(0)
    hist11.SetLineColor(kYellow+1)


    hist12 = TH1F(d[0]+"_12", "", d[1], d[2], d[3]) # ZZ to 4q
    hist12.GetXaxis().SetTitle(d[4])
    hist12.GetYaxis().SetTitle("Events")
    hist12.SetStats(0)
    hist12.SetLineColor(kMagenta+1)

    hist13 = TH1F(d[0]+"_13", "", d[1], d[2], d[3]) # ZZ to 4q
    hist13.GetXaxis().SetTitle(d[4])
    hist13.GetYaxis().SetTitle("Events")
    hist13.SetStats(0)
    hist13.SetLineColor(kRed)

    hist14 = TH1F(d[0]+"_14", "", d[1], d[2], d[3]) # ZZ to 4q
    hist14.GetXaxis().SetTitle(d[4])
    hist14.GetYaxis().SetTitle("Events")
    hist14.SetStats(0)
    hist14.SetLineColor(kBlue)

    hist15 = TH1F(d[0]+"_15", "", d[1], d[2], d[3]) # ZZ to 4q
    hist15.GetXaxis().SetTitle(d[4])
    hist15.GetYaxis().SetTitle("Events")
    hist15.SetStats(0)
    hist15.SetLineColor(kGreen)

    hist16 = TH1F(d[0]+"_16", "", d[1], d[2], d[3]) # ZZ to 4q
    hist16.GetXaxis().SetTitle(d[4])
    hist16.GetYaxis().SetTitle("Events")
    hist16.SetStats(0)
    hist16.SetLineColor(kCyan)

    hist17 = TH1F(d[0]+"_17", "", d[1], d[2], d[3]) # ZZ to 4q
    hist17.GetXaxis().SetTitle(d[4])
    hist17.GetYaxis().SetTitle("Events")
    hist17.SetStats(0)
    hist17.SetLineColor(kYellow)

    hist18 = TH1F(d[0]+"_18", "", d[1], d[2], d[3]) # ZZ to 4q
    hist18.GetXaxis().SetTitle(d[4])
    hist18.GetYaxis().SetTitle("Events")
    hist18.SetStats(0)
    hist18.SetLineColor(kMagenta)

    hist19 = TH1F(d[0]+"_19", "", d[1], d[2], d[3]) # ZZ to 4q
    hist19.GetXaxis().SetTitle(d[4])
    hist19.GetYaxis().SetTitle("Events")
    hist19.SetStats(0)
    hist19.SetLineColor(kRed-7)

    hist20 = TH1F(d[0]+"_20", "", d[1], d[2], d[3]) # ZZ to 4q
    hist20.GetXaxis().SetTitle(d[4])
    hist20.GetYaxis().SetTitle("Events")
    hist20.SetStats(0)
    hist20.SetLineColor(kBlue-7)

    hist21 = TH1F(d[0]+"_21", "", d[1], d[2], d[3]) # ZZ to 4q
    hist21.GetXaxis().SetTitle(d[4])
    hist21.GetYaxis().SetTitle("Events")
    hist21.SetStats(0)
    hist21.SetLineColor(kGreen-7)

    hist22 = TH1F(d[0]+"_22", "", d[1], d[2], d[3]) # ZZ to 4q
    hist22.GetXaxis().SetTitle(d[4])
    hist22.GetYaxis().SetTitle("Events")
    hist22.SetStats(0)
    hist22.SetLineColor(kCyan-7)

    hist23 = TH1F(d[0]+"_23", "", d[1], d[2], d[3]) # ZZ to 4q
    hist23.GetXaxis().SetTitle(d[4])
    hist23.GetYaxis().SetTitle("Events")
    hist23.SetStats(0)
    hist23.SetLineColor(kYellow-7)

    hist24 = TH1F(d[0]+"_24", "", d[1], d[2], d[3]) # ZZ to 4q
    hist24.GetXaxis().SetTitle(d[4])
    hist24.GetYaxis().SetTitle("Events")
    hist24.SetStats(0)
    hist24.SetLineColor(kMagenta-7)

    hist25 = TH1F(d[0]+"_25", "", d[1], d[2], d[3]) # ZZ to 4q
    hist25.GetXaxis().SetTitle(d[4])
    hist25.GetYaxis().SetTitle("Events")
    hist25.SetStats(0)
    hist25.SetLineColor(kRed-9)

    hist26 = TH1F(d[0]+"_26", "", d[1], d[2], d[3]) # ZZ to 4q
    hist26.GetXaxis().SetTitle(d[4])
    hist26.GetYaxis().SetTitle("Events")
    hist26.SetStats(0)
    hist26.SetLineColor(kBlue-9)

    hist27 = TH1F(d[0]+"_27", "", d[1], d[2], d[3]) # ZZ to 4q
    hist27.GetXaxis().SetTitle(d[4])
    hist27.GetYaxis().SetTitle("Events")
    hist27.SetStats(0)
    hist27.SetLineColor(kGreen-9)

    hist28 = TH1F(d[0]+"_28", "", d[1], d[2], d[3]) # ZZ to 4q
    hist28.GetXaxis().SetTitle(d[4])
    hist28.GetYaxis().SetTitle("Events")
    hist28.SetStats(0)
    hist28.SetLineColor(kCyan-9)

    hist29 = TH1F(d[0]+"_29", "", d[1], d[2], d[3]) # ZZ to 4q
    hist29.GetXaxis().SetTitle(d[4])
    hist29.GetYaxis().SetTitle("Events")
    hist29.SetStats(0)
    hist29.SetLineColor(kYellow-9)

    hist30 = TH1F(d[0]+"_30", "", d[1], d[2], d[3]) # ZZ to 4q
    hist30.GetXaxis().SetTitle(d[4])
    hist30.GetYaxis().SetTitle("Events")
    hist30.SetStats(0)
    hist30.SetLineColor(kMagenta-9)


    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A25y16_May25/X1000A25y16_May25.root", "tree_nominal", hist1, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A30y16_May25/X1000A30y16_May25.root", "tree_nominal", hist2, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A50y16_May25/X1000A50y16_May25.root", "tree_nominal", hist3, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A70y16_May25/X1000A70y16_May25.root", "tree_nominal", hist4, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A80y16_May25/X1000A80y16_May25.root", "tree_nominal", hist5, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A100y16_May25/X1000A100y16_May25.root", "tree_nominal", hist6, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A25y16_May25/X1500A25y16_May25.root", "tree_nominal", hist7, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A30y16_May25/X1500A30y16_May25.root", "tree_nominal", hist8, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A50y16_May25/X1500A50y16_May25.root", "tree_nominal", hist9, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A70y16_May25/X1500A70y16_May25.root", "tree_nominal", hist10, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A80y16_May25/X1500A80y16_May25.root", "tree_nominal", hist11, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A100y16_May25/X1500A100y16_May25.root", "tree_nominal", hist12, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A25y16_May25/X2000A25y16_May25.root", "tree_nominal", hist13, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A30y16_May25/X2000A30y16_May25.root", "tree_nominal", hist14, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A50y16_May25/X2000A50y16_May25.root", "tree_nominal", hist15, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A70y16_May25/X2000A70y16_May25.root", "tree_nominal", hist16, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A80y16_May25/X2000A80y16_May25.root", "tree_nominal", hist17, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A100y16_May25/X2000A100y16_May25.root", "tree_nominal", hist18, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A25y16_May25/X2500A25y16_May25.root", "tree_nominal", hist19, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A30y16_May25/X2500A30y16_May25.root", "tree_nominal", hist20, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A50y16_May25/X2500A50y16_May25.root", "tree_nominal", hist21, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A70y16_May25/X2500A70y16_May25.root", "tree_nominal", hist22, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A80y16_May25/X2500A80y16_May25.root", "tree_nominal", hist23, d[0], Cuts, Weight_MC) 
#    quickplot("/cms/xaastorage/PicoTrees/2017/April2020v6/X2500A100y17_May25/X2500A100y17_May25.root", "tree_nominal", hist24, d[0], Cuts, Weight_MC) 
#    quickplot("/cms/xaastorage/PicoTrees/2017/April2020v6/X3000A25y17_May25/X3000A25y17_May25.root", "tree_nominal", hist25, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A30y16_May25/X3000A30y16_May25.root", "tree_nominal", hist26, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A50y16_May25/X3000A50y16_May25.root", "tree_nominal", hist27, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A70y16_May25/X3000A70y16_May25.root", "tree_nominal", hist28, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A80y16_May25/X3000A80y16_May25.root", "tree_nominal", hist29, d[0], Cuts, Weight_MC) 
    quickplot("/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A100y16_May25/X3000A100y16_May25.root", "tree_nominal", hist30, d[0], Cuts, Weight_MC) 

    hist1.Scale(1./hist1.Integral())
    hist2.Scale(1./hist2.Integral())
    hist3.Scale(1./hist3.Integral())
    hist4.Scale(1./hist4.Integral())
    hist5.Scale(1./hist5.Integral())
    hist6.Scale(1./hist6.Integral())
    hist7.Scale(1./hist7.Integral())
    hist8.Scale(1./hist8.Integral())
    hist9.Scale(1./hist9.Integral())
    hist10.Scale(1./hist10.Integral())
    hist11.Scale(1./hist11.Integral())
    hist12.Scale(1./hist12.Integral())
    hist13.Scale(1./hist13.Integral())
    hist14.Scale(1./hist14.Integral())
    hist15.Scale(1./hist15.Integral())
    hist16.Scale(1./hist16.Integral())
    hist17.Scale(1./hist17.Integral())
    hist18.Scale(1./hist18.Integral())
    hist19.Scale(1./hist19.Integral())
    hist20.Scale(1./hist20.Integral())
    hist21.Scale(1./hist21.Integral())
    hist22.Scale(1./hist22.Integral())
    hist23.Scale(1./hist23.Integral())
#    if hist24.Integral()>0:
#        hist24.Scale(1./hist24.Integral())
#    if hist25.Integral()>0:
#        hist25.Scale(1./hist25.Integral())
    if hist26.Integral()>0:
        hist26.Scale(1./hist26.Integral())
    if hist27.Integral()>0:
        hist27.Scale(1./hist27.Integral())
    if hist28.Integral()>0:
        hist28.Scale(1./hist28.Integral())
    if hist29.Integral()>0:
        hist29.Scale(1./hist29.Integral())
    if hist30.Integral()>0:
        hist30.Scale(1./hist30.Integral())
    
    FindAndSetMax(hist1, hist2, hist3, hist3, hist4, hist5, hist6, hist7, hist8, hist9, hist10, hist11, hist12, hist13, hist14, hist15, hist16, hist17, hist18, hist19, hist20, hist21, hist22, hist23, hist24, hist25, hist26, hist27, hist28, hist29, hist30)
#    FindAndSetMax(hist5, hist6, hist7, hist8, hist9, hist10)

    L = TLegend(0.45, 0.45, 0.89, 0.89)
    L.SetFillColor(0)
    L.SetLineColor(0)
    L.SetNColumns(2)
    L.AddEntry(hist1, "X_{1000} #rightarrow a_{25}a_{25}", "l")
    L.AddEntry(hist2, "X_{1000} #rightarrow a_{30}a_{30}", "l")
    L.AddEntry(hist3, "X_{1000} #rightarrow a_{50}a_{50}", "l")
    L.AddEntry(hist4, "X_{1000} #rightarrow a_{70}a_{70}", "l")
    L.AddEntry(hist5, "X_{1000} #rightarrow a_{80}a_{80}", "l")
    L.AddEntry(hist6, "X_{1000} #rightarrow a_{100}a_{100}", "l")
    L.AddEntry(hist7, "X_{1500} #rightarrow a_{25}a_{25}", "l")
    L.AddEntry(hist8, "X_{1500} #rightarrow a_{30}a_{30}", "l")
    L.AddEntry(hist9, "X_{1500} #rightarrow a_{50}a_{50}", "l")
    L.AddEntry(hist10, "X_{1500} #rightarrow a_{70}a_{70}", "l")
    L.AddEntry(hist11, "X_{1500} #rightarrow a_{80}a_{80}", "l")
    L.AddEntry(hist12, "X_{1500} #rightarrow a_{100}a_{100}", "l")
    L.AddEntry(hist13, "X_{2000} #rightarrow a_{25}a_{25}", "l")
    L.AddEntry(hist14, "X_{2000} #rightarrow a_{30}a_{30}", "l")
    L.AddEntry(hist15, "X_{2000} #rightarrow a_{50}a_{50}", "l")
    L.AddEntry(hist16, "X_{2000} #rightarrow a_{70}a_{70}", "l")
    L.AddEntry(hist17, "X_{2000} #rightarrow a_{80}a_{80}", "l")
    L.AddEntry(hist18, "X_{2000} #rightarrow a_{100}a_{100}", "l")
    L.AddEntry(hist19, "X_{2500} #rightarrow a_{25}a_{25}", "l")
    L.AddEntry(hist20, "X_{2500} #rightarrow a_{30}a_{30}", "l")
    L.AddEntry(hist21, "X_{2500} #rightarrow a_{50}a_{50}", "l")
    L.AddEntry(hist22, "X_{2500} #rightarrow a_{70}a_{70}", "l")
    L.AddEntry(hist23, "X_{2500} #rightarrow a_{80}a_{80}", "l")
#    L.AddEntry(hist24, "X_{2500} #rightarrow a_{100}a_{100}", "l")
#    L.AddEntry(hist25, "X_{3000} #rightarrow a_{25}a_{25}", "l")
    L.AddEntry(hist26, "X_{3000} #rightarrow a_{30}a_{30}", "l")
    L.AddEntry(hist27, "X_{3000} #rightarrow a_{50}a_{50}", "l")
    L.AddEntry(hist28, "X_{3000} #rightarrow a_{70}a_{70}", "l")
    L.AddEntry(hist29, "X_{3000} #rightarrow a_{80}a_{80}", "l")
    L.AddEntry(hist30, "X_{3000} #rightarrow a_{100}a_{100}", "l")

    hist1.GetYaxis().SetTitleOffset(1.5)

    C = TCanvas(d[0], "", 500, 500)
    C.cd()
    hist1.Draw("hist")
    hist2.Draw("histsame")
    hist3.Draw("histsame")
    hist4.Draw("histsame")
    hist5.Draw("histsame")
    hist6.Draw("histsame")
    hist7.Draw("histsame")
    hist8.Draw("histsame")
    hist9.Draw("histsame")
    hist10.Draw("histsame")
    hist11.Draw("histsame")
    hist12.Draw("histsame")
    hist13.Draw("histsame")
    hist14.Draw("histsame")
    hist15.Draw("histsame")
    hist16.Draw("histsame")
    hist17.Draw("histsame")
    hist18.Draw("histsame")
    hist19.Draw("histsame")
    hist20.Draw("histsame")
    hist21.Draw("histsame")
    hist22.Draw("histsame")
    hist23.Draw("histsame")
#    hist24.Draw("histsame")
#    hist25.Draw("histsame")
    hist26.Draw("histsame")
    hist27.Draw("histsame")
    hist28.Draw("histsame")
    hist29.Draw("histsame")
    hist30.Draw("histsame")
    L.Draw("same")
    C.Print("PLOTS/2016_Normalized_Signal_" + d[0]+".pdf")


#parser = OptionParser()
#parser.add_option('-n', '--name', metavar='NAME', type='string', dest='n', help="The name of the output file, minus the .root.")
#(options, args) = parser.parse_args()
#Plots(options.n)

