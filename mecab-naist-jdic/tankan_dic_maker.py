# tankan_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2010-12-20 by Takuya Nishimoto

# IN_DIR : location of nvdajp_dic.py
# IN_DIR  = '/work/nvda/jp2011.1/source'
OUT_FILE = 'nvdajp-tankan-dic.csv'
CODE = 'cp932'

# import sys
# sys.path.append(IN_DIR)
import nvdajp_dic
import re

def contains_hankaku_katakana(k):
	# hankaku katakana check
	# http://programmer-toy-box.sblo.jp/article/24644519.html
	regexp = re.compile(r'(?:\xEF\xBD[\xA1-\xBF]|\xEF\xBE[\x80-\x9F])|[\x20-\x7E]')
	result = regexp.search(k.encode('utf-8'))
	if result != None: return True
	return False

def version1():
	with open(OUT_FILE, "w") as file:
		for k,v in nvdajp_dic.dic1.iteritems():
			# ＡＬＴ,1345,1345,6913,名詞,一般,*,*,*,*,ＡＬＴ,オルト,オルト,0/3,C1
			try:
				# hankaku katakana check
				# http://programmer-toy-box.sblo.jp/article/24644519.html
				#regexp = re.compile(r'(?:\xEF\xBD[\xA1-\xBF]|\xEF\xBE[\x80-\x9F])|[\x20-\x7E]')
				#result = regexp.search(k.encode('utf-8'))
				#if result != None : continue
				if contains_hankaku_katakana(k): continue
				dummy = k.encode(CODE)
				k1 = k
				y = v[4]
				mora_count = len(y)
				# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
				s = u"%s,-1,-1,15000,名詞,一般,*,*,*,*,%s,%s,%s,0/%d,C0\n" % (k1,k1,y,y,mora_count)
				file.write(s.encode(CODE))
			except Exception, e:
				print e

def version2():
	import csv
	jdic_tankan = {}
	reader = csv.reader(open('sjis-naist-jdic.csv', 'r'))
	for row in reader:
		hyousou = row[0].decode(CODE)
		if len(hyousou) == 1:
			jdic_tankan[hyousou] = row
	with open(OUT_FILE, "w") as file:
		for k,v in nvdajp_dic.dic1.iteritems():
			if contains_hankaku_katakana(k): continue
			if k in jdic_tankan:
				continue # print "%s in hyousou" % k.encode(CODE)
			try:
				dummy = k.encode(CODE)
			except Exception, e:
				print e
				continue
			k1 = k
			y = v[4]
			if u'コモジノ' in y:
				continue
			y = y.replace(' ', '')
			mora_count = len(y)
			# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
			s = u"%s,-1,-1,15000,記号,一般,*,*,*,*,%s,%s,%s,0/%d,C0\n" % (k1,k1,y,y,mora_count)
			file.write(s.encode(CODE))

def make_dic():
	version2()
	
if __name__ == '__main__':
	make_dic()
