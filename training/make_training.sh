

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
text2image --text=training_text.txt --outputbase=bgee.sherwood.exp0 --font="Sherwood Thin" --fonts_dir=. --ysize=400 --xsize=800
tesseract bgee.sherwood.exp0.tif bgee.sherwood.exp0 box.train.stderr
unicharset_extractor bgee.sherwood.exp0.box
echo "sherwood 0 1 0 0 0" > sherwood.properties
#shapeclustering -F sherwood.properties -U unicharset bgee.sherwood.exp0.tr
mftraining -F sherwood.properties -U unicharset -O bgee.unicharset bgee.sherwood.exp0.tr
cntraining bgee.sherwood.exp0.tr
cp inttemp bgee.inttemp
cp pffmtable bgee.pffmtable
cp normproto bgee.normproto
cp shapetable bgee.shapetable
combine_tessdata bgee.
