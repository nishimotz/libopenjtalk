# dlmain.py 
# -*- coding: utf-8 -*-
# ./dlmain -ow out2.wav input.txt
import os
from ctypes import *

libmc = cdll.LoadLibrary(r"C:\MeCab\bin\libmecab.dll")
libjt = cdll.LoadLibrary("libopenjtalk.dll")
mcdic = r"C:\openjtalk\open_jtalk_dic_utf_8-1.00"

# http://mecab.sourceforge.net/libmecab.html
# c:/mecab/sdk/mecab.h
MECAB_NOR_NODE = 0
MECAB_UNK_NODE = 1
MECAB_BOS_NODE = 2
MECAB_EOS_NODE = 3
class mecab_token_t(Structure):
	pass
mecab_token_t_ptr = POINTER(mecab_token_t)

class mecab_path_t(Structure):
	pass
mecab_path_t_ptr = POINTER(mecab_path_t)

class mecab_node_t(Structure):
	pass
mecab_node_t_ptr = POINTER(mecab_node_t)
mecab_node_t_ptr_ptr = POINTER(mecab_node_t_ptr)
mecab_node_t._fields_ = [
		("prev", mecab_node_t_ptr),
		("next", mecab_node_t_ptr),
		("enext", mecab_node_t_ptr),
		("bnext", mecab_node_t_ptr),
		("rpath", mecab_path_t_ptr),
		("lpath", mecab_path_t_ptr),
		("begin_node_list", mecab_node_t_ptr_ptr),
		("end_node_list", mecab_node_t_ptr_ptr),
		("surface", c_char_p),
		("feature", c_char_p),
		("id", c_uint),
		("length", c_ushort),
		("rlength", c_ushort),
		("rcAttr", c_ushort),
		("lcAttr", c_ushort),
		("posid", c_ushort),
		("char_type", c_ubyte),
		("stat", c_ubyte),
		("isbest", c_ubyte),
		("sentence_length", c_uint),
		("alpha", c_float),
		("beta", c_float),
		("prob", c_float),
		("wcost", c_short),
		("cost", c_long),
		("token", mecab_token_t_ptr),
	]

#text = u'こんにちは。今日はいい天気です。'
text = u'今日は。'
text = text.encode('utf-8')

mecab = libmc.mecab_new2(r"mecab -d " + mcdic)
# s = libmc.mecab_sparse_tostr(mecab, text)
# ret = c_char_p(s).value
# print ret

libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr
n = libmc.mecab_sparse_tonode(mecab, text)
n = n[0].next
while n:
	print n[0].stat
	len = n[0].length
	print len
	print string_at(n[0].surface, len).decode('utf-8')
	print string_at(n[0].feature).decode('utf-8')
	n = n[0].next

libmc.mecab_destroy(mecab)

#s1 = create_string_buffer(text, 200)
#s2 = create_string_buffer('out2.wav', 20)
#e = libjt.libopen_jtalk_main(s1, s2)
#print e

