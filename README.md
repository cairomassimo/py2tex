To see how an example works open Test folder and run ./test.sh

Note: mainOIIPC.tex uses the translation of keywords name in italian for the template of OII pseudocode

To convert Python code to Latex pseudocode:
(1) Write a python file input.py
(2) Run python py2latexpc.py input.py 1>output.txt
(3) Run latexmk main.tex -pdf
(4) Admire result ;-)

In folder LatexExtension you may find a couple of files that allow you to trasform into pdfs many txt files. To try it do the following run ./myScript.sh Source
