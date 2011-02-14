# custom_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2011-01-19 by Takuya Nishimoto

IN_DIR  = '/home/nishi/code/launchpad/with_jtalk/source/'
OUT_FILE = 'nvdajp-custom-dic.csv'

import sys
sys.path.append(IN_DIR)
import nvdajp_dic
import re

if __name__ == '__main__':
	with open(OUT_FILE, "w") as file:
		for k,v in nvdajp_dic.dic1.iteritems():
			# ＡＬＴ,1345,1345,6913,名詞,一般,*,*,*,*,ＡＬＴ,オルト,オルト,0/3,C1
                        try:
                                regexp = re.compile(r'(?:\xEF\xBD[\xA1-\xBF]|\xEF\xBE[\x80-\x9F])|[\x20-\x7E]')
                                result = regexp.search(k.encode('utf-8'))
                                if result != None : continue
                                dummy = k.encode('euc-jp')
                                dummy = k.encode('shift_jis')
                                k1 = k
                                y = v[4]
                                mora_count = len(y)
                                s = u"%s,1345,1345,6913,名詞,一般,*,*,*,*,%s,%s,%s,0/%d,C0\n" % (k1,k1,y,y,mora_count)
                                file.write(s.encode('euc_jp'))
                        except:
                                pass
