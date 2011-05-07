#!/bin/bash
# for Ubuntu Linux 9.04
# usage:
# sh make_jdic.sh 

SRCDIR=.
OUTDIR=/work/nvda/miscdep/source/nvdajptext/dic/
OUTDIR2=/work/nvda/jp2011.1/source/nvdajptext/dic/

mkdir -p $OUTDIR
python eng_dic_maker.py # uses bep-eng.dic
python tankan_dic_maker.py # uses nvdajp_dic.py
python custom_dic_maker.py
python roma_dic_maker.py
/usr/lib/mecab/mecab-dict-index -d $SRCDIR -o $OUTDIR -f cp932 -c cp932
cp $SRCDIR/dicrc $OUTDIR
echo "nvdajp-jtalk-dic" `date -u +%Y%m%d-%H%M%S` > $OUTDIR/DIC_VERSION
cp -av $OUTDIR/* $OUTDIR2
