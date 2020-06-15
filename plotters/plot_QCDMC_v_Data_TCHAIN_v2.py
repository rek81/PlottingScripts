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
    for i in File:
        chain.Add(i)
#    proof = ROOT.TProof.Open("lite://", "workers=2")
#    fast = ROOT.TProofChain(chain, True)
#    fast.Draw(var + ">>" + "temp", "(" + Weight + ")*(" + Cut + ")", "goff")
    chain.Draw(var + ">>" + "temp", "(" + Weight + ")*(" + Cut + ")", "goff")
    plot.Add(temp)

#dist = [["evt_HT", 200, 900, 2900, "HT"],["evt_Masym", 20, 0, 1, "Mass Asymmetry"], ["evt_Deta", 12, 0, 6, "#Delta#eta"],["J1pt", 300, 300, 3300, "Leading Jet p_{T}"], ["J1eta", 12, -3, 3, "Leading Jet #eta"],["J1SDM", 25, 0, 250, "Leading Jet Mass (GeV)"],["J1dbtag", 40, -1, 1, "Leading Jet Double b Tag (Hbb)"], ["J1DeeptagMD_Hbb", 20, 0, 1, "Leading Jet Double b Tag (Deep Decorrelated Hbb)"],["J2pt", 300, 300, 3300, "Subeading Jet p_{T}"], ["J2eta", 12, -3, 3, "Subleading Jet #eta"],["J2SDM", 25, 0, 250, "Subleading Jet Mass (GeV)"],["J2dbtag", 40, -1, 1, "Subleading Jet Double b Tag (Hbb)"], ["J2DeeptagMD_Hbb", 20, 0, 1, "Subleading Jet Double b Tag (Deep Decorrelated Hbb)"], ["PV", 12, 0, 60, "Primary Vertex"]]

dist = [["evt_HT", 300, 500, 3500, "HT"]]

#dist = [["evt_Deta", 12, 0, 6, "#Delta#eta"], ["J1eta", 12, -3, 3, "Leading Jet #eta"], ["J2eta", 12, -3, 3, "Subleading Jet #eta"]]


Cuts = " "
#Cuts = "evt_HT>900.&J1pt>300.&J2pt>300.&abs(J1eta)<2.4&abs(J2eta)<2.4"
Cuts = "evt_HT>900.&J1pt>300.&J2pt>300.&abs(J1eta)<2.4&abs(J2eta)<2.4"
Weight_MC = "35900.*weight_xsN"
Weight_MC_qcd = "0.9*35900.*weight_xsN"
Weight_DATA = "1.0"

#dist = [["J1dbtag", 20, -1, 1, "Leading Jet Double b Tag"], ["J2dbtag", 20, -1, 1, "Sub Leading Jet Double b Tag"]]
#dist = [["evt_Deta", 10, 0, 5, "HT"]]
#dist = [["evt_HT", 300, 500, 3500, "HT"]]
#dist = [["J1pt", 100, 500, 1500, "Leading Jet p_{T}"], ["J2pt", 100, 500, 1500, "Sub Leading Jet p_{T}"], ["J1eta", 12, -3, 3, "Leading Jet #eta"], ["J2eta", 12, -3, 3, "Sub Leading Jet #eta"], ["evt_Masym", 20, 0, 1, "Mass Asymmetry"], ["evt_Deta", 10, 0, 5, "#Delta#eta"], ["J1dbtag", 20, -1, 1, "Leading Jet Double b Tag"], ["J2dbtag", 20, -1, 1, "Sub Leading Jet Double b Tag"], ["J1SDM", 25, 0, 250, "Leading Jet Soft Drop Mass"], ["J2SDM", 25, 0, 250, "Sub Leading Jet Soft Drop Mass"], ["evt_HT", 300, 500, 3500, "HT"]]
#dist = [["J1dbtag", 20, -1., 1.], ["J2dbtag", 20, -1., 1.], ["J1SDM", 25, 0., 250.], ["J2SDM", 25, 0., 250.]]

for d in dist:

    hist1 = TH1F(d[0]+"_1", "", d[1], d[2], d[3]) # QCD
    hist1.GetXaxis().SetTitle(d[4])
    hist1.GetYaxis().SetTitle("Events")
    hist1.SetStats(0)
    hist1.SetLineColor(kRed)
    hist1.SetLineWidth(2)

    hist2 = TH1F(d[0]+"_2", "", d[1], d[2], d[3]) # DATA
    hist2.GetXaxis().SetTitle(d[4])
    hist2.GetYaxis().SetTitle("Events")
    hist2.GetYaxis().SetTitleOffset(1.5)
    hist2.SetStats(0)
    hist2.SetMarkerStyle(20)
    hist2.SetMarkerColor(1)

    hist3 = TH1F(d[0]+"_3", "", d[1], d[2], d[3]) # ttbar
    hist3.GetXaxis().SetTitle(d[4])
    hist3.GetYaxis().SetTitleOffset(1.5)
    hist3.GetYaxis().SetTitle("Events")
    hist3.SetStats(0)

#    hist9 = TH1F(d[0]+"_9", "", d[1], d[2], d[3]) # W+Jets starting at HT180evt_HT_pTbin.png
#    hist9.GetXaxis().SetTitle(d[4])
#    hist9.GetYaxis().SetTitle("Events")
#    hist9.SetStats(0)

#    hist10 = TH1F(d[0]+"_10", "", d[1], d[2], d[3]) # ZZ to 4q
#    hist10.GetXaxis().SetTitle(d[4])
#    hist10.GetYaxis().SetTitle("Events")
#    hist10.SetStats(0)

#    quickplot("", "tree_nominal", hist1, d[0], Cuts, Weight_MC_qcd) # for pT binned QCD
    quickplot(["/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT100to200.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT200to300.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT200to300_ext.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT300to500.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT300to500_ext.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT500to700.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT500to700_ext.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT700to1000.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT700to1000_ext.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT1000to1500.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT1000to1500_ext.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT1500to2000.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT1500to2000_ext.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT2000toInf.root", "/cms/xaastorage/PicoTrees/JAN6_2020/2016/QCD_HT/HT2000toInf_ext.root"], "tree_nominal", hist1, d[0], Cuts, Weight_MC_qcd) # for HT binned QCD
    quickplot(["/cms/xaastorage/PicoTrees/JAN6_2020/2016/DATA/2016_DATA.root"], "tree_nominal", hist2, d[0], Cuts, Weight_DATA)
    quickplot(["/cms/xaastorage/PicoTrees/JAN6_2020/2016/TTBAR/ttbar.root"], "tree_nominal", hist3, d[0], Cuts, Weight_MC)
##    quickplot("/home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/Picotrees_2017/June2019/WJetstoQQ/2017_WJets.root", "tree_nominal", hist9, d[0], Cuts, Weight_MC)
##    quickplot("/home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/Picotrees_2017/June2019/ZJetstoQQ/2017_ZJets.root", "tree_nominal", hist10, d[0], Cuts, Weight_MC)


    hist1.Add(hist3)
#    hist1.Add(hist9)
#    hist1.Add(hist10)

#    hist1.GetYaxis().SetRangeUser(0., hist1.GetMaximum())
#    hist2.GetYaxis().SetRangeUser(0., hist2.GetMaximum())
    # Making Ratio Plot: Data/(Sum of Backgrounds)
    ratio = hist2.Clone("ratio")
    ratio.Divide(hist1)
    ratio.GetYaxis().SetTitle("DATA/MC")
    ratio.GetXaxis().SetTitle(" ")
    ratio.GetYaxis().SetLabelSize(0.1)
    ratio.GetYaxis().SetLabelOffset(0.005)
    ratio.GetYaxis().SetTitleSize(0.15)
    ratio.GetYaxis().SetTitleOffset(0.2)
    
#    ratio.GetYaxis().SetRangeUser(0.75, 1.05)
#    ratio.GetYaxis().SetTextSize(0.1)

    FindAndSetMax(hist1, hist2, hist3)

    L = TLegend(0.6, 0.6, 0.89, 0.89)
    L.SetFillColor(0)
    L.SetLineColor(0)
    L.AddEntry(hist1, "2016 Background Monte Carlo", "l")
    L.AddEntry(hist2, "2016 JetHT Data", "P")
           
    flat = TLine(float(d[2]), 1., float(d[3]), 1.)
    
    C = TCanvas(d[0], "", 500, 500)
    C.cd()
    Plot = TPad("plot", "The pad 80% of the height",0,0.15,1,1)
    rat = TPad("rat", "The pad 20% of the height",0,0,1.0,0.15)
    Plot.Draw()
    rat.Draw()
    Plot.cd()
#    Plot.SetLogy()
    hist1.Draw("hist")
    hist2.Draw("esame")
    L.Draw("same")
    rat.cd()
    ratio.Draw("e")
    flat.Draw()
    C.Print("PLOTS/HTQCD/" + d[0]+".root")
    C.Print("PLOTS/HTQCD/" + d[0]+".pdf")

#parser = OptionParser()
#parser.add_option('-n', '--name', metavar='NAME', type='string', dest='n', help="The name of the output file, minus the .root.")
#(options, args) = parser.parse_args()
#Plots(options.n)

