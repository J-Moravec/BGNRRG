# BGNRRG
**Baldur's Gate: Enhanced Edition Non Random Roll Generator** is tool that helps you maximize your totall roll without having to manually click on anything.

**BGNRRG** use utilize tesseract-ocr for computer vision to recognize rolled number. For this reason, you need to have tesseract installed (and its python wrapper pytesseract). Furthermore, BGNRRG use some cross-platform libraries: pyscreenshot for taking screenshots and pymouse for clicking and mouse positioning. These should work on any platform, but this script was not extensively tested anywhere else but Linux.

First, copy bgee.traineddata and bgee2.traineddata to your tessdata folder:
* Linux: ```/usr/share/tesseract-ocr/tessdata``` or ```/usr/share/tessdata``` 
* Windows: ```C:\Program Files\Tesseract OCR\tessdata```
* Mac: Tesseract page is unclear on this. If some Mac user knows, please contact me.

Then you need to initialize positions for buttons and area of totall roll. Run Baldur's Gate: Enhanced edition, go to character creation, abilities, then run terminal and write:
```
python BGNRRG.py -i
```
and follow instruction.

Now, you can type (while still on Abilities screen of Character Creation):
```
pyton BGNRRG.py
```
and enjoy your highest roll. You can further specify delay, language (by default, bgee2 is used), number of rolls (by default 100 rolls) and verbose output. Simply write ```python BGNRRG.py -h``` and read help.

Be carefull with number of rolls and delay. Programs can't be currently stopped while rolling, so you may want to go with lower number of rolls (100 or at max 1000) and repeat, BGNRRG takes current roll as starting value and at the and, recall the highest one, so it can be repeated with ease. For the delay, you need to find something that works for you and your computer. With too small delay, results starts to be nondeterministics. Probably some clicks are not performed so returned roll is different than maximal roll. Default value 0.1 should work, on my computer, 0.05 works as well but 0.01 does not.

If you want to know more about training, read [training](training.md) document in this folder. If you want to know more about how this was done, read [making_of](making_of.md) document in this folder.
