import ROOT
import argparse
import sys

parser=argparse.ArgumentParser()
parser.add_argument("-f", "--certfile", default="", help="The path to a cert tree.")
parser.add_argument("-b", "--baseName", default="", help="The common string in the histograms.")
parser.add_argument("-r", "--bcidrange",default="700,1050", help="BCID range for plot.")

args=parser.parse_args()

tfile=ROOT.TFile.Open(args.certfile)

try:
    bcidrange=args.bcidrange.split(",")
    print bcidrange
    for iR in range(len(bcidrange)):
        bcidrange[iR]=float(bcidrange[iR])
except:
    print "failed to get range from:",args.bcidrange
    sys.exit(-1)

histNames=[]
histNames.append("Before_Corr_")
histNames.append("After_TypeI_Corr_")
#histNames.append("After_TypeI_TypeII_Corr_")
histNames.append("After_Corr_")

for iHist in range(len(histNames)):
    histNames[iHist]=histNames[iHist]+args.baseName
    print histNames[iHist]


hists=[]
for iHist in range(len(histNames)):
    hists.append(tfile.Get(histNames[iHist]))


colors = [418, 803, 632, 1]
styles = [21, 22, 23, 24]

leg=ROOT.TLegend(0.6,0.7,0.9,0.85)
leg.AddEntry(hists[0],"Before corrections","p")
leg.AddEntry(hists[1],"After type 1   - ~9%","p")
leg.AddEntry(hists[2],"After type 1+2 - ~12%","p")
leg.SetBorderSize(0)
leg.SetFillColor(ROOT.kWhite)
can=ROOT.TCanvas(args.baseName,"",700,1000)
for iHist in range(len(histNames)):
    hists[iHist].SetMarkerColor(colors[iHist])
    hists[iHist].SetMarkerStyle(styles[iHist])
    if iHist==0:
        hists[iHist].SetTitle(";Bunch Crossing;Instantaneous Luminosity (Hz/#mub)")
        hists[iHist].GetXaxis().SetRangeUser(bcidrange[0],bcidrange[1])
        hists[iHist].Draw("p");
        hists[iHist].SetMaximum(hists[iHist].GetMaximum()*1.3)
        hists[iHist].Draw("p");
    else :
        hists[iHist].Draw("psame");

leg.Draw("same");

text=ROOT.TLatex(0.72,0.88,"2016  (13TeV)")
text.SetNDC()
text.SetTextFont(62)
text.SetTextSize(0.05)
text2=ROOT.TLatex(0.15,0.88,"CMS #bf{#scale[0.75]{#it{Preliminary}}}")
text2.SetNDC()
text2.SetTextSize(0.05)
text2.SetTextFont(62)
text.Draw("same")
text2.Draw("same")


can.Update()
outNameBase="PCCcorrections_example_"+args.baseName
can.SaveAs(outNameBase+".png")
can.SaveAs(outNameBase+".C")

hists[0].GetYaxis().SetRangeUser(-0.01,0.3)
can.Update()
can.SaveAs(outNameBase+"_zoom.png")
can.SaveAs(outNameBase+"_zoom.C")
