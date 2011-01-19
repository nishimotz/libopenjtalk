#!/bin/bash
# for Ubuntu Linux 9.04

# usage:
# python eng_dic_maker.py
# python tankan_dic_maker.py
# sh make_jdic.sh 

SRCDIR=.
OUTDIR=/home/nishi/code/jtalk/dic

mkdir -p $OUTDIR
/usr/lib/mecab/mecab-dict-index -d $SRCDIR -o $OUTDIR -f EUC-JP -c Shift_JIS
cp $SRCDIR/dicrc $OUTDIR
