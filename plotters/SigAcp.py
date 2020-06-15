import ROOT
import math
import os
import numpy
from numpy import array
import array
import sys

RDF = ROOT.ROOT.RDataFrame
ROOT.ROOT.EnableImplicitMT()


def MakeNBinsFromMinToMax(N,Min,Max):
    BINS = []
    for i in range(N+1):
        BINS.append(Min+(i*(Max-Min)/N))
    return BINS

def accep(samp, tree, weight, cutsel, cutpsel, bins1, var1, var2, avals, Xvals, year):


    accPlot = ROOT.TH2F("acceptace", "", len(avals)-1, numpy.array(avals), len(Xvals)-1, numpy.array(Xvals))
    accPlot.SetStats(0)
    print numpy.array(avals)
    print numpy.array(Xvals)

    acclist = []

    for i in samp:

        F = ROOT.TChain(tree)
        F.Add(i[0])
        rdf = RDF(F)

        rdf_w = rdf.Define("total_weight", weight)
        hist = rdf_w.Filter(cutsel)
        plot = hist.Histo1D((var1, ";"+i[1]+";Events", len(bins1)-1, numpy.array(bins1)), var1, "total_weight")

        plotnew = plot.DrawCopy()
        
        histpresel = rdf_w.Filter(cutpsel)
        plotpresel = histpresel.Histo1D((var1, ";"+i[1]+";Events", len(bins1)-1, numpy.array(bins1)), var1, "total_weight")
        plotpresel.Scale(1/plot.Integral())
        
    
        acceptance = 100.*plot.GetEntries()/plotpresel.GetEntries()

        values = [i[1], acceptance]
        acclist.append(values)

    for i in acclist:
#        print i[0]
#        print i[1]
        if "a25" in i[0]:
            xbin = 1
        if "a30" in i[0]:
            xbin = 2 
        if "a50" in i[0]:
            xbin = 3
        if "a70" in i[0]:
            xbin = 4
        if "a80" in i[0]:
            xbin = 5
        if "a100" in i[0]:
            xbin = 6
        if "X1000" in i[0]:
            ybin = 1
        if "X1500" in i[0]:
            ybin = 2
        if "X2000" in i[0]:
            ybin = 3
        if "X2500" in i[0]:
            ybin = 4
        if "X3000" in i[0]:
            ybin = 5
       
        

        accPlot.SetEntries(len(samp))
        accPlot.SetBinContent(xbin, ybin, i[1])
    
        accPlot.GetXaxis().SetBinLabel(1, "25")
        accPlot.GetXaxis().SetBinLabel(2, "30")
        accPlot.GetXaxis().SetBinLabel(3, "50")
        accPlot.GetXaxis().SetBinLabel(4, "70")
        accPlot.GetXaxis().SetBinLabel(5, "80")
        accPlot.GetXaxis().SetBinLabel(6, "100")
        accPlot.GetYaxis().SetBinLabel(1, "1000")
        accPlot.GetYaxis().SetBinLabel(2, "1500")
        accPlot.GetYaxis().SetBinLabel(3, "2000")
        accPlot.GetYaxis().SetBinLabel(4, "2500")
        accPlot.GetYaxis().SetBinLabel(5, "3000")
        accPlot.GetXaxis().SetTitle("a Mass (GeV)")
        accPlot.GetYaxis().SetTitle("X Mass (GeV)")
        accPlot.GetZaxis().SetTitle("Acceptance (%)")
        accPlot.GetZaxis().SetTitleOffset(-0.2)

    C = ROOT.TCanvas("acc", "", 500, 500)
    C.cd()
    accPlot.Draw("colztext")
    C.Print(year+"acceptance.pdf")


if __name__=="__main__":

    cuts17 = "evt_HT>1200. && J2pt>300. && evt_XM > 1000. && evt_Masym>0.0 && evt_Masym<0.25 && evt_Deta < 1.5 && J2dbtag > 0.8 && J1dbtag>0.8 && J2SDM > 12.5"
    cutspsel17 = "evt_HT>1200. && J2pt>300. && J1dbtag>0.8 && evt_XM > 1000."
    cuts16 = "evt_HT>900. && J2pt>300. && evt_XM > 900. && evt_Masym>0.0 && evt_Masym<0.25 && evt_Deta < 1.5 && J2dbtag > 0.8 && J1dbtag>0.8 && J2SDM > 12.5"
    cutspsel16 = "evt_HT>900. && J2pt>300. && J1dbtag>0.8 && evt_XM > 900."
    
    aMbins = MakeNBinsFromMinToMax(40 ,15., 215.)
    XMbins = MakeNBinsFromMinToMax(30 , 500., 3500.)

    XMasses = [1000., 1500., 2000., 2500., 3000., 3500.]
    aMasses = [10., 30., 50., 70., 90., 110., 130.]

    x1000a25 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1000A25y17_May25/X1000A25y17_May25.root", "X1000a25", ROOT.kRed]
    x1000a30 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1000A30y17_May25/X1000A30y17_May25.root", "X1000a30", ROOT.kRed]
    x1000a50 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1000A50y17_May25/X1000A50y17_May25.root", "X1000a50", ROOT.kRed]
    x1000a70 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1000A70y17_May25/X1000A70y17_May25.root", "X1000a70", ROOT.kRed]
    x1000a80 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1000A80y17_May25/X1000A80y17_May25.root", "X1000a80", ROOT.kRed]
    x1000a100 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1000A100y17_May25/X1000A100y17_May25.root", "X1000a100", ROOT.kRed]
    x1500a25 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1500A25y17_May25/X1500A25y17_May25.root", "X1500a25", ROOT.kRed]
    x1500a30 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1500A30y17_May25/X1500A30y17_May25.root", "X1500a30", ROOT.kRed]
    x1500a50 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1500A50y17_May25/X1500A50y17_May25.root", "X1500a50", ROOT.kRed]
    x1500a70 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1500A70y17_May25/X1500A70y17_May25.root", "X1500a70", ROOT.kRed]
    x1500a80 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1500A80y17_May25/X1500A80y17_May25.root", "X1500a80", ROOT.kRed]
    x1500a100 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X1500A100y17_May25/X1500A100y17_May25.root", "X1500a100", ROOT.kRed]
    x2000a25 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2000A25y17_May25/X2000A25y17_May25.root", "X2000a25", ROOT.kRed]
    x2000a30 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2000A30y17_May25/X2000A30y17_May25.root", "X2000a30", ROOT.kRed]
    x2000a50 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2000A50y17_May25/X2000A50y17_May25.root", "X2000a50", ROOT.kRed]
    x2000a70 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2000A70y17_May25/X2000A70y17_May25.root", "X2000a70", ROOT.kRed]
    x2000a80 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2000A80y17_May25/X2000A80y17_May25.root", "X2000a80", ROOT.kRed]
    x2000a100 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2000A100y17_May25/X2000A100y17_May25.root", "X2000a100", ROOT.kRed]
    x2500a25 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2500A25y17_May25/X2500A25y17_May25.root", "X2500a25", ROOT.kRed]
    x2500a30 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2500A30y17_May25/X2500A30y17_May25.root", "X2500a30", ROOT.kRed]
    x2500a50 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2500A50y17_May25/X2500A50y17_May25.root", "X2500a50", ROOT.kRed]
    x2500a70 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2500A70y17_May25/X2500A70y17_May25.root", "X2500a70", ROOT.kRed]
    x2500a80 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2500A80y17_May25/X2500A80y17_May25.root", "X2500a80", ROOT.kRed]
    x2500a100 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X2500A100y17_May25/X2500A100y17_May25.root", "X2500a100", ROOT.kRed]
    x3000a25 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X3000A25y17_May25/X3000A25y17_May25.root", "X3000a25", ROOT.kRed]
    x3000a30 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X3000A30y17_May25/X3000A30y17_May25.root", "X3000a30", ROOT.kRed]
    x3000a50 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X3000A50y17_May25/X3000A50y17_May25.root", "X3000a50", ROOT.kRed]
    x3000a70 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X3000A70y17_May25/X3000A70y17_May25.root", "X3000a70", ROOT.kRed]
    x3000a80 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X3000A80y17_May25/X3000A80y17_May25.root", "X3000a80", ROOT.kRed]
    x3000a100 = ["/cms/xaastorage/PicoTrees/2017/April2020v6/X3000A100y17_May25/X3000A100y17_May25.root", "X3000a100", ROOT.kRed]

    x1000a25y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1000A25y18_May25/X1000A25y18_May25.root", "X1000a25", ROOT.kRed]
    x1000a30y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1000A30y18_May25/X1000A30y18_May25.root", "X1000a30", ROOT.kRed]
    x1000a50y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1000A50y18_May25/X1000A50y18_May25.root", "X1000a50", ROOT.kRed]
    x1000a70y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1000A70y18_May25/X1000A70y18_May25.root", "X1000a70", ROOT.kRed]
    x1000a80y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1000A80y18_May25/X1000A80y18_May25.root", "X1000a80", ROOT.kRed]
    x1000a100y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1000A100y18_May25/X1000A100y18_May25.root", "X1000a100", ROOT.kRed]

    x1500a25y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1500A25y18_May25/X1500A25y18_May25.root", "X1500a25", ROOT.kRed]
    x1500a30y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1500A30y18_May25/X1500A30y18_May25.root", "X1500a30", ROOT.kRed]
    x1500a50y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1500A50y18_May25/X1500A50y18_May25.root", "X1500a50", ROOT.kRed]
    x1500a70y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1500A70y18_May25/X1500A70y18_May25.root", "X1500a70", ROOT.kRed]
    x1500a80y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1500A80y18_May25/X1500A80y18_May25.root", "X1500a80", ROOT.kRed]
    x1500a100y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X1500A100y18_May25/X1500A100y18_May25.root", "X1500a100", ROOT.kRed]

    x2000a25y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2000A25y18_May25/X2000A25y18_May25.root", "X2000a25", ROOT.kRed]
    x2000a30y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2000A30y18_May25/X2000A30y18_May25.root", "X2000a30", ROOT.kRed]
    x2000a50y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2000A50y18_May25/X2000A50y18_May25.root", "X2000a50", ROOT.kRed]
    x2000a70y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2000A70y18_May25/X2000A70y18_May25.root", "X2000a70", ROOT.kRed]
    x2000a80y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2000A80y18_May25/X2000A80y18_May25.root", "X2000a80", ROOT.kRed]
    x2000a100y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2000A100y18_May25/X2000A100y18_May25.root", "X2000a100", ROOT.kRed]

    x2500a25y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2500A25y18_May25/X2500A25y18_May25.root", "X2500a25", ROOT.kRed]
    x2500a30y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2500A30y18_May25/X2500A30y18_May25.root", "X2500a30", ROOT.kRed]
    x2500a50y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2500A50y18_May25/X2500A50y18_May25.root", "X2500a50", ROOT.kRed]
    x2500a70y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2500A70y18_May25/X2500A70y18_May25.root", "X2500a70", ROOT.kRed]
    x2500a80y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2500A80y18_May25/X2500A80y18_May25.root", "X2500a80", ROOT.kRed]
    x2500a100y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X2500A100y18_May25/X2500A100y18_May25.root", "X2500a100", ROOT.kRed]


    x3000a25y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X3000A25y18_May25/X3000A25y18_May25.root", "X3000a25", ROOT.kRed]
    x3000a30y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X3000A30y18_May25/X3000A30y18_May25.root", "X3000a30", ROOT.kRed]
    x3000a50y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X3000A50y18_May25/X3000A50y18_May25.root", "X3000a50", ROOT.kRed]
    x3000a70y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X3000A70y18_May25/X3000A70y18_May25.root", "X3000a70", ROOT.kRed]
    x3000a80y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X3000A80y18_May25/X3000A80y18_May25.root", "X3000a80", ROOT.kRed]
    x3000a100y18 = ["/cms/xaastorage/PicoTrees/2018/April2020v6/X3000A100y18_May25/X3000A100y18_May25.root", "X3000a100", ROOT.kRed]

    x1000a25y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A25y16_June2/X1000A25y16_June2.root", "X1000a25", ROOT.kRed]
    x1000a30y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A30y16_June2/X1000A30y16_June2.root", "X1000a30", ROOT.kRed]
    x1000a50y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A50y16_June2/X1000A50y16_June2.root", "X1000a50", ROOT.kRed]
    x1000a70y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A70y16_June2/X1000A70y16_June2.root", "X1000a70", ROOT.kRed]
    x1000a80y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A80y16_June2/X1000A80y16_June2.root", "X1000a80", ROOT.kRed]
    x1000a100y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1000A100y16_June2/X1000A100y16_June2.root", "X1000a100", ROOT.kRed]

    x1500a25y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A25y16_June2/X1500A25y16_June2.root", "X1500a25", ROOT.kRed]
    x1500a30y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A30y16_June2/X1500A30y16_June2.root", "X1500a30", ROOT.kRed]
    x1500a50y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A50y16_June2/X1500A50y16_June2.root", "X1500a50", ROOT.kRed]
    x1500a70y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A70y16_June2/X1500A70y16_June2.root", "X1500a70", ROOT.kRed]
    x1500a80y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A80y16_June2/X1500A80y16_June2.root", "X1500a80", ROOT.kRed]
    x1500a100y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X1500A100y16_June2/X1500A100y16_June2.root", "X1500a100", ROOT.kRed]

    x2000a25y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A25y16_June2/X2000A25y16_June2.root", "X2000a25", ROOT.kRed]
    x2000a30y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A30y16_June2/X2000A30y16_June2.root", "X2000a30", ROOT.kRed]
    x2000a50y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A50y16_June2/X2000A50y16_June2.root", "X2000a50", ROOT.kRed]
    x2000a70y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A70y16_June2/X2000A70y16_June2.root", "X2000a70", ROOT.kRed]
    x2000a80y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A80y16_June2/X2000A80y16_June2.root", "X2000a80", ROOT.kRed]
    x2000a100y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2000A100y16_June2/X2000A100y16_June2.root", "X2000a100", ROOT.kRed]

    x2500a25y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A25y16_June2/X2500A25y16_June2.root", "X2500a25", ROOT.kRed]
    x2500a30y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A30y16_June2/X2500A30y16_June2.root", "X2500a30", ROOT.kRed]
    x2500a50y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A50y16_June2/X2500A50y16_June2.root", "X2500a50", ROOT.kRed]
    x2500a70y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A70y16_June2/X2500A70y16_June2.root", "X2500a70", ROOT.kRed]
    x2500a80y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X2500A80y16_June2/X2500A80y16_June2.root", "X2500a80", ROOT.kRed]

    x3000a30y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A30y16_June2/X3000A30y16_June2.root", "X3000a30", ROOT.kRed]
    x3000a50y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A50y16_June2/X3000A50y16_June2.root", "X3000a50", ROOT.kRed]
    x3000a70y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A70y16_June2/X3000A70y16_June2.root", "X3000a70", ROOT.kRed]
    x3000a80y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A80y16_June2/X3000A80y16_June2.root", "X3000a80", ROOT.kRed]
    x3000a100y16 = ["/cms/xaastorage/PicoTrees/2016/April2020v6/X3000A100y16_June2/X3000A100y16_June2.root", "X3000a100", ROOT.kRed]

    flist = [x1000a25, x1000a30, x1000a50, x1000a70, x1000a80, x1000a100, x1500a25, x1500a30, x1500a50, x1500a70, x1500a80, x1500a100, x2000a25, x2000a30, x2000a50, x2000a70, x2000a80, x2000a100, x2500a25, x2500a30, x2500a50, x2500a70, x2500a80, x2500a100, x3000a25, x3000a30, x3000a50, x3000a70, x3000a80, x3000a100]

    flist18 = [x1000a25y18, x1000a30y18, x1000a50y18, x1000a70y18, x1000a80y18, x1000a100y18, x1500a25y18, x1500a30y18, x1500a50y18, x1500a70y18, x1500a80y18, x1500a100y18, x2000a25y18, x2000a30y18, x2000a50y18, x2000a70y18, x2000a80y18, x2000a100y18, x2500a25y18, x2500a30y18, x2500a50y18, x2500a70y18, x2500a80y18, x2500a100y18, x3000a25y18, x3000a30y18, x3000a50y18, x3000a70y18, x3000a80y18, x3000a100y18]

    flist16 = [x1000a25y16, x1000a30y16, x1000a50y16, x1000a70y16, x1000a80y16, x1000a100y16, x1500a25y16, x1500a30y16, x1500a50y16, x1500a70y16, x1500a80y16, x1500a100y16, x2000a25y16, x2000a30y16, x2000a50y16, x2000a70y16, x2000a80y16, x2000a100y16, x2500a25y16, x2500a30y16, x2500a50y16, x2500a70y16, x2500a80y16, x3000a30y16, x3000a50y16, x3000a70y16, x3000a80y16, x3000a100y16]
    
#    accep(flist, "tree_nominal", "weight_xsN*weight_PU", cuts17, cutspsel17, aMbins, "evt_aM", "evt_XM", aMasses, XMasses, "2017")    
    accep(flist16, "tree_nominal", "weight_xsN*weight_PU", cuts16, cutspsel16, aMbins, "evt_aM", "evt_XM", aMasses, XMasses, "2016")    
#    accep(flist18, "tree_nominal", "weight_xsN*weight_PU", cuts17, cutspsel17, aMbins, "evt_aM", "evt_XM", aMasses, XMasses, "2018")    
