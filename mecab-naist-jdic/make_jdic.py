# coding: utf-8
# make_jdic.py for nvdajp
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010-2011 Takuya Nishimoto (nishimotz.com)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import shutil
import subprocess
import datetime
import errno

import eng_dic_maker
import tankan_dic_maker
import custom_dic_maker
import roma_dic_maker

THISDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.normpath(THISDIR + "\\dic\\") # "c:/work/nvda/miscdep/source/nvdajptext/dic/"
TEMPDIR = os.path.normpath(THISDIR + "\\_temp\\") # '_temp'
ENGDIC = os.path.normpath(THISDIR + "..\\..\\..\\bep-eng.dic")
MECAB_DICT_INDEX = os.path.normpath(THISDIR + '..\\..\\mecab\\src\\mecab-dict-index.exe')
#print MECAB_DICT_INDEX
CODE = 'cp932'

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST:
			pass
		else: raise exc

mkdir_p(OUTDIR)
mkdir_p(TEMPDIR)

eng_dic_maker.make_dic(ENGDIC)
tankan_dic_maker.make_dic()
custom_dic_maker.make_dic()
roma_dic_maker.make_dic()

def convert_file(src_file, src_enc, dest_file, dest_enc):
	with open(src_file) as sf:
		with open(dest_file, "w") as df:
			while 1:
				s = sf.readline()
				if not s:
					break
				df.write(s.decode(src_enc).encode(dest_enc))

files = ['sjis-naist-jdic.csv','dicrc',
		 'nvdajp-eng-dic.csv','nvdajp-tankan-dic.csv',
		 'nvdajp-custom-dic.csv','nvdajp-roma-dic.csv',
		 ]

euc_files = ['char.def','feature.def','left-id.def','matrix.def',
	'pos-id.def','rewrite.def','right-id.def', 'unk.def']

for f in files:
	shutil.copy(f, TEMPDIR)

for f in euc_files:							 
	print "converting %s" % f
	convert_file(f, 'euc-jp', TEMPDIR+os.sep+f, CODE)

subprocess.check_call([MECAB_DICT_INDEX, '-d','.', '-o',OUTDIR, '-f',CODE, '-c',CODE], cwd=TEMPDIR)

shutil.copy('dicrc', OUTDIR)
with open(OUTDIR + os.sep + "DIC_VERSION", "wb") as f:
	f.write("nvdajp-jtalk-dic " 
		+ datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S') + os.linesep) 

# end of file
