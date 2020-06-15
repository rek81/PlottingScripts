import ROOT
import os
from ROOT import *
import sys
import math
from array import array
import functools
import scipy
import random
import string

colors = []
Ncol = 6
for i in range(Ncol):
    ci = 2214 + i
    Co = (float(i)/float(Ncol))
#    print Co
    color = TColor(ci, 1.0-Co, 0.0, 0.0+Co)
    colors.append([ci, color])
files = ["QCD.root", "ttbar.root"]
names = ["qcd", "ttbar"]
legnames = ["qcd", "t#bar{t}"]

'''class distribution:
    def __init__(self, name, treename, weight,  printname, isData):
        self.name = name
        self.treename = treename
        self.weight = weight
        self.col = col
        self.printname = printname
        self.MC = not isData'''

class variable:
    def __init__(self, tree, var, weight, bins, name):
        self.name = name 
        self.tree = tree
        self.var = var
        self.weight = weight
        self.bins = bins
        self.nbins = len(bins)-1
        

def plotFormat(H, *args):
    H.SetStats(0)
    if args[0] == 'thickline':
        H.SetLineColor(args[1])
        H.SetLineWidth(2)
    if args[0] == 'thinline':
        H.SetLineColor(args[1])
        H.SetLineWidth(1)
    if args[0] == 'fill':
        H.SetLineColor(args[1])
        H.SetFillColor(args[1])
        H.SetFillStyle(args[2])

def AddCMSLumi(pad, fb, extra):
    cmsText = "CMS";
    cmsTextFont = 61
    extraText = extra
    extraTextFont = 52
    lumiTextSize = 0.4
    lumiTextOffset = 0.15
    cmsTextSize = 0.5
    cmsTextOffset = 0.15

    H = pad.GetWh()
    W = pad.GetWw()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    e = 0.025
    pad.cd()

    lumiText = str(fb)+" fb^{-1} (13 TeV)"

    extraTextSize = 0.76*cmsTextSize
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSide(lumiTextSide*t)
    latext.DrawLatex(1-r, 1-t+lumiTextOffset*t. lumiText)
    pad.cd()

    latex.SetTextFont(cmsTextFont)
    latex.SetTextSize(cmsTextSide*t)
    latex.SetTextAlign(11)
    latex.DrawLatex(l, 1-t+cmsTextOffset*t, cmsText)
    latex.SetTextFont(extraTextFont)
    latex.SetTextAlign(11)
    latex.SetTextSize(extraTextSize*t)
    latex.DrawLatex(l+0.11, 1-t+cmsTextOffset*t, extraText)
    pad.Update()

class plotter(variable):
    def __init__(self, VAR, cuts, lumi, extra):
        variable.VAR = VAR
        self.cuts = cuts
        self.lumi = lumi
        self.extra = extra

        for q in variable.VAR:
            final_plot = THStack("hs" , "Preselection Plot")
            for u in names:
                names[u] = TH1F(names[u], "", q.nbins, scipy.array(q.nbins))
                for j in files:
                    print "for files"
                    chn = TChain(q.treename)
                    chn.Add(j)
                    chn.Draw(q.var+">>"+names[u], "("+q.weight+"*"+lumi+")*("+cuts+")", "goff")
                    for b in colors:
                        hist.SetFillColor(colors[b][0])
                final_plot.Add(names[u])
                C = TCanvas("C", "", 500, 500)
                C.cd()
                final_plot.Draw()
                AddCMSLumi(gPad, self.lumi, self.extra)
                print "Drawing " + "stacked_preselection/"+q.var+"_"+".root"
                C.Print("stacked_preselection/"+q.var+"_"+".root")
                C.Print("stacked_preselection/"+q.var+"_"+".png")
                leg = TLegend(0.53, 0.63, 0.89, 0.89)
                leg.SetLineColor(0)
                leg.SetFillColor(0)
                for c in legnames:
                    leg.AddEntry(names[u], legnames[c], "f")
                    leg.Draw("same")
        print "stacked plot drawn"

if __name__ == '__main__':

    pTbins = []
    for i in range(55):
        pTbins.append(450. + i*10)

    cut = "SD_0>10.&SD_1>10.&&weight<15.&Tau32_0>0.57&Tau32_1>0.57&Tau21_0>0.55&Tau21_1>0.55"
    pT0 = variable("tree", "pT_0", "weight*puW", pTbins, "Leading Jet p_{T}")

    plot = plotter(pT0, cut, 35.8, "test")
