#!/bin/bash

dir=$1
for wholename in $dir/*.txt;
do
  filename=${wholename##*/}
  rootname="${filename%.*}"
  echo $wholename
  echo $filename
  echo $rootname
  cp main.tex tmp.tex
  sed -i -- "s#bau#$wholename#g" tmp.tex
  cat -n tmp.tex | sed '36p'
  lualatex tmp.tex -pdf 
  mv tmp.pdf $rootname.pdf
done
#rm tmp.fls
rm tmp.log
rm tmp.aux
#rm tmp.fdb_latexmk

