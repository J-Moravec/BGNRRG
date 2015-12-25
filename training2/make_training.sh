#!/bin/bash
#
# author: Jiří Moravec
# contact: 323886@mail.muni.cz
# version: 0.1
# date: 2015 12 24
#
#
# Description:
#   This scripts trains tesseract on Sherwood fonts used in BG:EE
#   Various commans are part of tesseract package, which needs to be installed.
text2image --text=training_text.txt --outputbase=bgee2.sherwood.exp0 --font="Sherwood Thin" --fonts_dir=. --ysize=400 --xsize=800
tesseract bgee2.sherwood.exp0.tif bgee2.sherwood.exp0 box.train.stderr
tesseract bgee2.sherwood.exp1.tif bgee2.sherwood.exp1 box.train.stderr
unicharset_extractor bgee2.sherwood.exp0.box bgee2.sherwood.exp1.box
echo "sherwood 0 1 0 0 0" > sherwood.properties
#shapeclustering -F sherwood.properties -U unicharset bgee.sherwood.exp0.tr
mftraining -F sherwood.properties -U unicharset -O bgee2.unicharset bgee2.sherwood.exp0.tr bgee2.sherwood.exp1.tr
cntraining bgee2.sherwood.exp0.tr bgee2.sherwood.exp1.tr
cp inttemp bgee2.inttemp
cp pffmtable bgee2.pffmtable
cp normproto bgee2.normproto
cp shapetable bgee2.shapetable
combine_tessdata bgee2.
