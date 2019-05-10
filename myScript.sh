#!/bin/bash

dir="python"
#$1
out="output.txt"
for wholename in $dir/*.py;
do
	python py2tex.py $wholename 1>$out
  filename=${wholename##*/}
  rootname="${filename%.*}"
  #echo $wholename
  #echo $filename
  #echo $rootname
  cp $out "txt/$rootname.txt"
  #cp main.tex tmp.tex
  #sed -i -- "s#bau#$wholename#g" tmp.tex
  #cat -n tmp.tex | sed '36p'
  (pdflatex main.tex -pdf) 
  #>/dev/null
  mv main.pdf "latex/$rootname.pdf"
done
#rm tmp.fls
rm main.log
rm main.aux
#rm tmp.fdb_latexmk
rm output.txt

