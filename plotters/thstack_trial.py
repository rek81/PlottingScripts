import ROOT
from ROOT import *
import os
import sys
import math
from array import array
import optparse 

hist = THStack("hs", "Stacked Preselection")
hist.GetXaxis().SetTitle("Backgrounds")
hist.GetYaxis().SetTitle("Events")

qcd = TH1F("QCD", "", 200, 450, 2000)
qcd.SetLineColor(4)
qcd.SetFillColor(4)

ttbar = TH1F("ttbar", "", 200, 450, 2000)
ttbar.SetLineColor(2)
ttbar.SetFillColor(2)

files = ["QCD.root", "ttbar.root"]

F2 = ROOT.TFile("QCD.root")
T2 = F2.Get("tree")
n2 = T2.GetEntries()
for i in range(n2):
    T2.GetEntry(i)
    ttbar.Fill(T2.pT_0)
ttbar.Scale(T2.weight*T2.puW)
hist.Add(ttbar)

F1 = ROOT.TFile("QCD.root")
T1 = F1.Get("tree")
n1 = T1.GetEntries()
for i in range(n1):
    T1.GetEntry(i)
    qcd.Fill(T1.pT_0)
qcd.Scale(T1.weight*T1.puW)
hist.Add(qcd)

C = TCanvas("c", "", 500, 500, 500, 500)
C.cd()
hist.Draw()
l = TLegend(0.6, 0.6, 0.89, 0.89)
l.SetLineColor(0)
l.SetFillColor(0)
l.AddEntry(qcd, "QCD", "f")
l.AddEntry(ttbar, "QCD but in red", "f")
l.Draw("same")
#l.AddEntry(ttbar, "t#bar{t}", "f")
C.Print("thstackTrial.root")
