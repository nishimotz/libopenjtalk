#!/bin/bash
# for Ubuntu Linux 9.04
SRCDIR=/work/github/libopenjtalk/mecab-naist-jdic
OUTDIR=/work/jtalk/_dic
cp /usr/share/mecab/dic/ipadic/dicrc .
/usr/lib/mecab/mecab-dict-index -d $SRCDIR -o $OUTDIR -f EUC-JP -c Shift_JIS
cp $SRCDIR/dicrc $OUTDIR

