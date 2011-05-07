#!/bin/bash
# for Ubuntu Linux 9.04
# usage:
# sh make_jdic.sh 

OUTDIR=/work/nvda/miscdep/source/nvdajptext/dic/
OUTDIR2=/work/nvda/jp2011.1/source/nvdajptext/dic/

mkdir -p $OUTDIR
python eng_dic_maker.py # uses bep-eng.dic
python tankan_dic_maker.py # uses nvdajp_dic.py
python custom_dic_maker.py
python roma_dic_maker.py
mkdir -p _temp
cp nvdajp-eng-dic.csv nvdajp-tankan-dic.csv nvdajp-custom-dic.csv nvdajp-roma-dic.csv sjis-naist-jdic.csv _temp
cp char.def feature.def left-id.def matrix.def pos-id.def rewrite.def right-id.def _temp
cp unk.def.cp932 _temp/unk.def
cp dicrc _temp
cd _temp
/usr/lib/mecab/mecab-dict-index -d . -o $OUTDIR -f cp932 -c cp932
cd ..
cp dicrc $OUTDIR
echo "nvdajp-jtalk-dic" `date -u +%Y%m%d-%H%M%S` > $OUTDIR/DIC_VERSION
cp -av $OUTDIR/* $OUTDIR2
