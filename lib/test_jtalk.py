# test_jtalk.py 
# -*- coding: utf-8 -*-

from ctypes import *
from jtalk import *

CODE = 'shift_jis'
FELEN   = 1000 # string len
FECOUNT = 100
FEATURE = c_char * FELEN
FEATURE_ptr = POINTER(FEATURE)
FEATURE_ptr_array = FEATURE_ptr * FECOUNT

libjt = cdll.LoadLibrary(JT_DLL)
mecab_feature = FEATURE_ptr_array()

for i in xrange(0, FECOUNT):
	buf = libjt.jt_malloc(FELEN)
	mecab_feature[i] = cast(buf, FEATURE_ptr)

_feature = [
u'ある,連体詞,*,*,*,*,*,ある,アル,アル,1/2,*',
u'社長,名詞,一般,*,*,*,*,社長,シャチョウ,シャチョー,0/3,C2',
u'は,助詞,係助詞,*,*,*,*,は,ハ,ワ,0/1,名詞%F1/動詞%F2@0/形容詞%F2@0',
u'若い,形容詞,自立,*,*,形容詞・アウオ段,基本形,若い,ワカイ,ワカイ,2/3,C1',
u'間,名詞,一般,*,*,*,*,間,アイダ,アイダ,0/1,C2',
u'は,助詞,係助詞,*,*,*,*,は,ハ,ワ,0/1,名詞%F1/動詞%F2@0/形容詞%F2@0',
u'おおいに,副詞,一般,*,*,*,*,おおいに,オオイニ,オーイニ,1/4,*',
u'遊べ,動詞,自立,*,*,五段・バ行,命令ｅ,遊ぶ,アソベ,アソベ,0/3,C2',
u'と,助詞,格助詞,引用,*,*,*,と,ト,ト,0/1,形容詞%F1/動詞%F1',
u'いう,動詞,自立,*,*,五段・ワ行促音便,基本形,いう,イウ,イウ,0/2,C1',
u'。,記号,句点,*,*,*,*,。,。,。,*/*,*',]
size = 0
for f in _feature:
	s = f.encode(CODE)
	dst_ptr = mecab_feature[size]
	buf = create_string_buffer(s)
	src_ptr = byref(buf)
	memmove(dst_ptr, src_ptr, len(s)+1)
	size += 1

msg = [mecab_feature, size]

def main():
	initialize()
	print "speaking"
	#speak(u'こんにちは。')
	for i in xrange(0,5):
		r = 100 - i * 25
		print r
		setRate(r)
		#speak(u'ユーモアとは、高慢このうえない解毒剤だ。'); time.sleep(5)
		#speak(u'ある社長は若い間はおおいに遊べという。'); time.sleep(10)
		speak(msg, isFeatures=True);time.sleep(5)
# 		speak(u'老人は、漁夫として、すばらしい人間だと思う。'); time.sleep(3)
# 		speak(u'初めて、沈黙を破って、キリストがささやいた。'); time.sleep(3)
	# 私が一番古い友達というので碑文に一筆すすめられた。
# 	setRate(100)
# 	speak(u'私が一番古い友達というので碑文に一筆すすめられた。')
# 	time.sleep(3)
# 	speak(u'私が一番古い友達というので')
# 	speak(u'碑文')
# 	speak(u'に一筆すすめられた。')
# 	time.sleep(3)
# 	speak(u'私が一番古い友達というので碑文')
# 	speak(u'に一筆すすめられた。')
# 	time.sleep(3)
# 	speak(u'私が一番古い友達というので')
# 	speak(u'碑文に一筆すすめられた。')
# 	time.sleep(3)
# 	setRate(80)
# 	speak(u'私が一番古い友達というので')
# 	setRate(20)
# 	speak(u'碑文')
# 	setRate(80)
# 	speak(u'に一筆すすめられた。')
# 	time.sleep(3)
# 	setRate(60)
# 	speak(u'私が一番古い友達というので')
# 	setRate(0)
# 	speak(u'碑文')
# 	setRate(60)
# 	speak(u'に一筆すすめられた。')
# 	time.sleep(3)
	#print "sleep"
	#time.sleep(1.5)
	#print "stopping"
	#stop()
	#time.sleep(2)
	#print "sleep"
	#speak(u'今日はいい天気です。')
	#time.sleep(1.2)
	#print "stopping"
	#stop()
	time.sleep(10)
	#print "terminating"
	terminate()
	print "end"

if __name__ == "__main__":
	main()
