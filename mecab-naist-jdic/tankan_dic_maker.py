# tankan_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2010-12-20 by Takuya Nishimoto

# IN_DIR : location of nvdajp_dic.py
# IN_DIR  = '/home/nishi/code/launchpad/with_jtalk/source/'
IN_DIR  = '/work/nvda/releases_2011.1/source'
OUT_FILE = 'nvdajp-tankan-dic.csv'

import sys
sys.path.append(IN_DIR)
import nvdajp_dic
import re

if __name__ == '__main__':
	with open(OUT_FILE, "w") as file:
		for k,v in nvdajp_dic.dic1.iteritems():
			# ＡＬＴ,1345,1345,6913,名詞,一般,*,*,*,*,ＡＬＴ,オルト,オルト,0/3,C1
			try:
				# http://programmer-toy-box.sblo.jp/article/24644519.html
				regexp = re.compile(r'(?:\xEF\xBD[\xA1-\xBF]|\xEF\xBE[\x80-\x9F])|[\x20-\x7E]')
				result = regexp.search(k.encode('utf-8'))
				if result != None : continue
				dummy = k.encode('cp932')
				k1 = k
				y = v[4]
				mora_count = len(y)
				# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
				s = u"%s,-1,-1,15000,名詞,一般,*,*,*,*,%s,%s,%s,0/%d,C0\n" % (k1,k1,y,y,mora_count)
				file.write(s.encode('cp932'))
			except Exception, e:
				print e
