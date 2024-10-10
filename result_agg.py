import os
import re
import numpy as np
import warnings
from scipy import stats
import barplot
warnings.filterwarnings('ignore')
# parents = ["HT55rockimages", 'DA13rockinh18032022', 'Hutu80rockinh18032022', 'LS180rockimages']
# parents = ["Da1306042022cad", 'Da1318042022cad', 'Hutu8006042022cad', 'Hutu8018042022cad']
# parents = ["CMS3"]
# # typeofexps = ['RCM1','SW948', 'Lcolo']
# typeofexps = ['LS513']
#
# mother = 'invivo'
allpath = "outputs//benchmark//"
fils = [os.path.join(root, name)
             for root, dirs, files in os.walk(allpath)
             for name in files
             if name.endswith((".txt")) and "min" in name]

moddict = {}
modposdict = {}
alltags =[]
for i in range(len(fils)):
    outermost = fils[i].split("\\")[0]
    innerid = fils[i].split("\\")[1]
    tag = outermost + "\\" + innerid
    if tag not in alltags:
        alltags.append(tag)

for tag in alltags:
    moddict[tag] = 0
    modposdict[tag] = 0
    modlist = []
    for i in range(len(fils)):
        if tag in fils[i]:
            arr = np.loadtxt(fils[i])
            modlist.extend(arr.tolist())
            zerarr = np.asarray(modlist)-1
            posarr = zerarr[np.nonzero(zerarr)]
            print(np.mean(modlist), np.mean(posarr))
            moddict[tag] = np.mean(modlist)
            modposdict[tag] = np.mean(posarr)
import csv


with open('outputs/moddictbenchmark.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, moddict.keys())
    w.writeheader()
    w.writerow(moddict)
with open('outputs/modposdictbenchmark.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, moddict.keys())
    w.writeheader()
    w.writerow(modposdict)
# for parentdirectory in parents:
#     print(parentdirectory)
#     # parentdirectory = "HT55rockimages"
#     param = list()
#     l32 = []
#     allaparam = {}
#     allapos = {}
#     alla0tempo = {}
#     alla1tempo = {}
#     allaexp = {}
#     for indexcount in range(len(typeofexps)):
#         allaparam[typeofexps[indexcount]] = []
#         allapos[typeofexps[indexcount]] = []
#         alla0tempo[typeofexps[indexcount]] = []
#         alla1tempo[typeofexps[indexcount]] = []
#         allaexp[typeofexps[indexcount]] = []
#     aparam = list()
#     bparam = list()
#     cparam = list()
#     dparam = list()
#     eparam = list()
#     fparam = list()
#     gparam = list()
#     hparam = list()
#     apos = list()
#     bpos = list()
#     cpos = list()
#     dpos = list()
#     epos = list()
#     fpos = list()
#     gpos = list()
#     hpos = list()
#     a0tempo = list()
#     b0tempo = list()
#     c0tempo = list()
#     d0tempo = list()
#     e0tempo = list()
#     f0tempo = list()
#     g0tempo = list()
#     h0tempo = list()
#     a1tempo = list()
#     b1tempo = list()
#     c1tempo = list()
#     d1tempo = list()
#     e1tempo = list()
#     f1tempo = list()
#     g1tempo = list()
#     h1tempo = list()
#     aexp = "unknown"
#     bexp = "unknown"
#     cexp = "unknown"
#     dexp = "unknown"
#     eexp = "unknown"
#     fexp = "unknown"
#     gexp = "unknown"
#     hexp = "unknown"
#     fileprefs = "../../DispersionQuant2/outputs/"
#     #concentrations = ['control', '0.9375', '1.875', '3.75', '7.5', '15', '30', '60']
#
#     for root, dirs, files in os.walk(fileprefs + parentdirectory):
#         path = root.split(os.sep)
#         # print((len(path) - 1) * '---', os.path.basename(root))
#         for filer in files:
#             paramfilen = "gomparams.dat"
#             if paramfilen in filer:
#                 nameoffolder = ''
#                 for i in range(0, len(path) - 1):
#                     nameoffolder += path[i] + os.sep
#                 filesin = os.listdir(nameoffolder)
#                 firstif = 0
#                 for filerin in filesin:
#                     # print (filerin)
#                     if ".tif" in filerin and firstif ==0:
#                         firstif = 1
#                         for indexcount in range(len(typeofexps)):
#                             typeofexp = typeofexps[indexcount]
#                             match = re.search(typeofexp, filerin)
#                             if match != None:
#                                 aval, bval, cval, r2val, chnval = np.loadtxt(root + os.sep + paramfilen, delimiter=' ',
#                                                                              unpack=True)
#                                 param.append(aval)
#                                 allaparam[typeofexp].append(aval)
#                                 allapos[typeofexp].append(int(re.findall('[0-9]+', filerin)[-1]))
#                                 alla0tempo[typeofexp].append(aval[0])
#                                 alla1tempo[typeofexp].append(aval[1])
#                                 allaexp[typeofexp] = typeofexps[indexcount]
#
#                         # match = re.search(typeofexps[0], filerin)
#                         # if match!=None:
#                         #
#                         #     aval, bval, cval, r2val, chnval = np.loadtxt(root + os.sep + paramfilen, delimiter=' ',
#                         #                                                  unpack=True)
#                         #     param.append(aval)
#                         #     aparam.append(aval)
#                         #     apos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #     a0tempo.append(aval[0])
#                         #     a1tempo.append(aval[1])
#                         #     aexp = typeofexps[0]
#                         #     # print("A", path[-3], filerin, match.group(1), aval)
#                         #     break
#                         # else:
#                         #     match1 = re.search(typeofexps[1], filerin)
#                         #     match2 = re.search(typeofexps[2], filerin)
#                         #     if match1 != None or  match2 != None:
#                         #
#                         #         aval, bval, cval, r2val, chnval = np.loadtxt(root + os.sep + paramfilen, delimiter=' ',
#                         #                                                      unpack=True)
#                         #         param.append(aval)
#                         #         bparam.append(aval)
#                         #         bpos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #         b0tempo.append(aval[0])
#                         #         b1tempo.append(aval[1])
#                         #         bexp = typeofexps[1]
#                         #         # print("B", path[-3], filerin, match.group(1), aval)
#                         #         break
#                         #     else:
#                         #         match = re.search(typeofexps[3], filerin)
#                         #         if match!=None:
#                         #             # print("C", filerin, match.group(1), root)
#                         #             aval, bval, cval, r2val, chnval = np.loadtxt(root + os.sep + paramfilen,
#                         #                                                          delimiter=' ',
#                         #                                                          unpack=True)
#                         #             param.append(aval)
#                         #             cparam.append(aval)
#                         #             cpos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #             c0tempo.append(aval[0])
#                         #             c1tempo.append(aval[1])
#                         #             cexp = typeofexps[3]
#                         #             # print("C", path[-3], filerin, match.group(1), aval)
#                         #             break
#                         #         else:
#                         #             match = re.search('D(\d+)', filerin)
#                         #             if path[-3] == '3.75':
#                         #
#                         #                 aval, bval, cval, r2val, chnval = np.loadtxt(root + os.sep + paramfilen,
#                         #                                                              delimiter=' ',
#                         #                                                              unpack=True)
#                         #                 param.append(aval)
#                         #                 dparam.append(aval)
#                         #                 dpos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #                 d0tempo.append(aval[0])
#                         #                 d1tempo.append(aval[1])
#                         #                 dexp = path[-3]
#                         #                 # print("D", path[-3], filerin, match.group(1), aval)
#                         #                 break
#                         #             else:
#                         #                 match = re.search('E(\d+)', filerin)
#                         #                 if path[-3] == '7.5':
#                         #                     aval, bval, cval, r2val, chnval = np.loadtxt(root + os.sep + paramfilen,
#                         #                                                                  delimiter=' ',
#                         #                                                                  unpack=True)
#                         #                     param.append(aval)
#                         #                     eparam.append(aval)
#                         #                     epos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #                     e0tempo.append(aval[0])
#                         #                     e1tempo.append(aval[1])
#                         #                     eexp = path[-3]
#                         #                     # print("E", path[-3], filerin, match.group(1), aval)
#                         #                     break
#                         #                 else:
#                         #                     match = re.search('F(\d+)', filerin)
#                         #                     if path[-3] == '15':
#                         #                         aval, bval, cval, r2val, chnval = np.loadtxt(root + os.sep + paramfilen,
#                         #                                                                      delimiter=' ',
#                         #                                                                      unpack=True)
#                         #                         param.append(aval)
#                         #                         fparam.append(aval)
#                         #                         fpos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #                         f0tempo.append(aval[0])
#                         #                         f1tempo.append(aval[1])
#                         #                         fexp = path[-3]
#                         #                         # print("F", path[-3], filerin, match.group(1), aval)
#                         #                         break
#                         #                     else:
#                         #                         match = re.search('G(\d+)', filerin)
#                         #                         if path[-3] == '30':
#                         #                             aval, bval, cval, r2val, chnval = np.loadtxt(
#                         #                                 root + os.sep + paramfilen,
#                         #                                 delimiter=' ',
#                         #                                 unpack=True)
#                         #                             param.append(aval)
#                         #                             gparam.append(aval)
#                         #                             gpos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #                             g0tempo.append(aval[0])
#                         #                             g1tempo.append(aval[1])
#                         #                             gexp = path[-3]
#                         #                             # print("G", path[-3], filerin, match.group(1), aval)
#                         #                             break
#                         #                         else:
#                         #                             match = re.search('H(\d+)', filerin)
#                         #                             if path[-3] == '60':
#                         #                                 aval, bval, cval, r2val, chnval = np.loadtxt(
#                         #                                     root + os.sep + paramfilen,
#                         #                                     delimiter=' ',
#                         #                                     unpack=True)
#                         #                                 param.append(aval)
#                         #                                 hparam.append(aval)
#                         #                                 hpos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #                                 h0tempo.append(aval[0])
#                         #                                 h1tempo.append(aval[1])
#                         #                                 hexp = path[-3]
#                         #                                 # print("H", path[-3], filerin, match.group(1), aval)
#                         #                                 break
#                         #                             else:
#                         #                                 if path[-3] == 'ecadherin':
#                         #                                     aval, bval, cval, r2val, chnval = np.loadtxt(
#                         #                                         root + os.sep + paramfilen,
#                         #                                         delimiter=' ',
#                         #                                         unpack=True)
#                         #                                     param.append(aval)
#                         #                                     hparam.append(aval)
#                         #                                     hpos.append(int(re.findall('[0-9]+', filerin)[-1]))
#                         #                                     h0tempo.append(aval[0])
#                         #                                     h1tempo.append(aval[1])
#                         #                                     hexp = path[-3]
#                         #                                     # print("H", path[-3], filerin, match.group(1), aval)
#                         #                                     break
#
#     for indexcount in range(len(typeofexps)):
#         typeofexp = typeofexps[indexcount]
#         a0tempo = np.asarray(allaparam[typeofexp])[np.where(np.argsort(allaparam[typeofexp])==0)]
#         a1tempo = np.asarray(allaparam[typeofexp])[np.where(np.argsort(allaparam[typeofexp])==1)]
#         outwrite = open(fileprefs + parentdirectory + os.sep + typeofexp + ".out", "w")
#         np.savetxt(outwrite, a0tempo)
#         np.savetxt(outwrite, a1tempo)
#         outwrite.close()
#         zscores = stats.zscore(a0tempo, axis=None)
#         zscoremean = np.mean(a0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#         print(typeofexp, np.mean(a0tempo), zscoremean, np.mean(a1tempo), (np.mean(a0tempo) + np.mean(
#             a1tempo)) / 2, np.mean(np.hstack((a0tempo,
#                                               a1tempo))))
#     # a = np.asarray(aparam)
#     # b = np.asarray(bparam)
#     # c = np.asarray(cparam)
#     # d = np.asarray(dparam)
#     # e = np.asarray(eparam)
#     # f = np.asarray(fparam)
#     # g = np.asarray(gparam)
#     # h = np.asarray(hparam)
#     # params = np.asarray(param)
#     # print(aexp, bexp, cexp, dexp, eexp, fexp, gexp, hexp)
#     # # print c,d
#     # # print(np.mean(params[:, 0]), np.mean(params[:, 1]), np.mean(params[:, 2]), np.mean(params[:, 0:2]))
#     # if len(a) != 0:
#     #     kss = np.argsort(apos)
#     #     apos = np.asarray(apos)[kss]
#     #     a0tempo = np.asarray(a0tempo)[kss]
#     #     a1tempo = np.asarray(a1tempo)[kss]
#     #     aropo = fileprefs + parentdirectory + os.sep + aexp + ".out"
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + aexp + ".out", "w")
#     #     # np.savetxt(outwrite, apos, delimiter=' ')
#     #     np.savetxt(outwrite, a0tempo)
#     #     np.savetxt(outwrite, a1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(a0tempo, axis=None)
#     #     zscoremean = np.mean(a0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("A", aexp, apos, np.mean(a0tempo), zscoremean, np.mean(a1tempo), (np.mean(a0tempo) + np.mean(
#     #         a1tempo)) / 2, np.mean(np.hstack((a0tempo,
#     #                                           a1tempo))))  # , np.mean(a[:, 0]), np.mean(a[:, 1]), np.mean(a[:, 2]), np.mean(a[:, 0:2]), np.median(a[:, 0:2]))
#     # if len(b) != 0:
#     #     kss = np.argsort(bpos)
#     #     bpos = np.asarray(bpos)[kss]
#     #     b0tempo = np.asarray(b0tempo)[kss]
#     #     b1tempo = np.asarray(b1tempo)[kss]
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + bexp + ".out", "w")
#     #     # np.savetxt(outwrite, bpos)
#     #     np.savetxt(outwrite, b0tempo)
#     #     np.savetxt(outwrite, b1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(b0tempo, axis=None)
#     #     zscoremean = np.mean(b0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("B", bexp, bpos, np.mean(b0tempo), zscoremean, np.mean(b1tempo), (np.mean(b0tempo) + np.mean(
#     #         b1tempo)) / 2, np.mean(np.hstack((b0tempo,
#     #                                           b1tempo))))  # , np.mean(b[:, 0]), np.mean(b[:, 1]), np.mean(b[:, 2]), np.mean(b[:, 0:2]), np.median(b[:, 0:2]))
#     # if len(c) != 0:
#     #     kss = np.argsort(cpos)
#     #     cpos = np.asarray(cpos)[kss]
#     #     c0tempo = np.asarray(c0tempo)[kss]
#     #     c1tempo = np.asarray(c1tempo)[kss]
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + cexp + ".out", "w")
#     #     # np.savetxt(outwrite, cpos)
#     #     np.savetxt(outwrite, c0tempo)
#     #     np.savetxt(outwrite, c1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(c0tempo, axis=None)
#     #     zscoremean = np.mean(c0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("C", cexp, cpos, np.mean(c0tempo), zscoremean, np.mean(c1tempo), (np.mean(c0tempo) + np.mean(
#     #         c1tempo)) / 2, np.mean(np.hstack((c0tempo,
#     #                                           c1tempo))))  # , np.mean(c[:, 0]), np.mean(c[:, 1]), np.mean(c[:, 2]), np.mean(c[:, 0:2]), np.median(c[:, 0:2]))
#     # if len(d) != 0:
#     #     kss = np.argsort(dpos)
#     #     dpos = np.asarray(dpos)[kss]
#     #     d0tempo = np.asarray(d0tempo)[kss]
#     #     d1tempo = np.asarray(d1tempo)[kss]
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + dexp + ".out", "w")
#     #     # np.savetxt(outwrite, len(dpos))
#     #     np.savetxt(outwrite, d0tempo)
#     #     np.savetxt(outwrite, d1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(d0tempo, axis=None)
#     #     zscoremean = np.mean(d0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("D", dexp, dpos, np.mean(d0tempo), zscoremean, np.mean(d1tempo), (np.mean(d0tempo) + np.mean(
#     #         d1tempo)) / 2, np.mean(np.hstack((d0tempo,
#     #                                           d1tempo))))  # , np.mean(d[:, 0]), np.mean(d[:, 1]), np.mean(d[:, 2]), np.mean(d[:, 0:2]), np.median(d[:, 0:2]))
#     # if len(e) != 0:
#     #     kss = np.argsort(epos)
#     #     epos = np.asarray(epos)[kss]
#     #     e0tempo = np.asarray(e0tempo)[kss]
#     #     e1tempo = np.asarray(e1tempo)[kss]
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + eexp + ".out", "w")
#     #     # np.savetxt(outwrite, epos, delimiter=' ')
#     #     np.savetxt(outwrite, e0tempo)
#     #     np.savetxt(outwrite, e1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(e0tempo, axis=None)
#     #     zscoremean = np.mean(e0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("E", eexp, epos, np.mean(e0tempo), zscoremean, np.mean(e1tempo), (np.mean(e0tempo) + np.mean(
#     #         e1tempo)) / 2, np.mean(np.hstack((e0tempo,
#     #                                           e1tempo))))  # , np.mean(e[:, 0]), np.mean(e[:, 1]), np.mean(e[:, 2]), np.mean(e[:, 0:2]), np.median(e[:, 0:2]))
#     # if len(f) != 0:
#     #     kss = np.argsort(fpos)
#     #     fpos = np.asarray(fpos)[kss]
#     #     f0tempo = np.asarray(f0tempo)[kss]
#     #     f1tempo = np.asarray(f1tempo)[kss]
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + fexp + ".out", "w")
#     #     # np.savetxt(outwrite, fpos)
#     #     np.savetxt(outwrite, f0tempo)
#     #     np.savetxt(outwrite, f1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(f0tempo, axis=None)
#     #     zscoremean = np.mean(f0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("F", fexp, fpos, np.mean(f0tempo), zscoremean, np.mean(f1tempo), (np.mean(f0tempo) + np.mean(
#     #         f1tempo)) / 2, np.mean(np.hstack((f0tempo,
#     #                                           f1tempo))))  # , np.mean(f[:, 0]), np.mean(f[:, 1]), np.mean(f[:, 2]), np.mean(f[:, 0:2]), np.median(f[:, 0:2]))
#     # if len(g) != 0:
#     #     kss = np.argsort(gpos)
#     #     gpos = np.asarray(gpos)[kss]
#     #     g0tempo = np.asarray(g0tempo)[kss]
#     #     g1tempo = np.asarray(g1tempo)[kss]
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + gexp + ".out", "w")
#     #     # np.savetxt(outwrite, gpos)
#     #     np.savetxt(outwrite, g0tempo)
#     #     np.savetxt(outwrite, g1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(g0tempo, axis=None)
#     #     zscoremean = np.mean(g0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("G", gexp, gpos, np.mean(g0tempo), zscoremean, np.mean(g1tempo), (np.mean(g0tempo) + np.mean(
#     #         g1tempo)) / 2, np.mean(np.hstack((g0tempo,
#     #                                           g1tempo))))  # , np.mean(g[:, 0]), np.mean(g[:, 1]), np.mean(g[:, 2]), np.mean(g[:, 0:2]), np.median(g[:, 0:2]))
#     # if len(h) != 0:
#     #     kss = np.argsort(hpos)
#     #     hpos = np.asarray(hpos)[kss]
#     #     h0tempo = np.asarray(h0tempo)[kss]
#     #     h1tempo = np.asarray(h1tempo)[kss]
#     #     outwrite = open(fileprefs + parentdirectory + os.sep + hexp + ".out", "w")
#     #     # np.savetxt(outwrite, hpos)
#     #     np.savetxt(outwrite, h0tempo)
#     #     np.savetxt(outwrite, h1tempo)
#     #     outwrite.close()
#     #     zscores = stats.zscore(h0tempo, axis=None)
#     #     zscoremean0 = np.mean(h0tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     zscores = stats.zscore(h1tempo, axis=None)
#     #     zscoremean1 = np.mean(h1tempo[np.where(((zscores > -1) & (zscores < 1)))])
#     #     print("H", hexp, hpos, np.mean(h0tempo), zscoremean0, np.mean(h1tempo), zscoremean1,
#     #           (np.mean(h0tempo) + np.mean(
#     #               h1tempo)) / 2, np.mean(np.hstack((h0tempo,
#     #                                                 h1tempo))))  # , np.mean(h[:, 0]), np.mean(h[:, 1]), np.mean(h[:, 2]), np.mean(h[:, 0:2]), np.median(h[:, 0:2]))
#     # # x = [x[0] for x in os.walk()]
#     # a = 1
#
