# dlmain.py 
# -*- coding: utf-8 -*-
# ./dlmain -ow out2.wav input.txt
from ctypes import *
h = cdll.LoadLibrary("libopenjtalk.dll")
text = u'こんにちは。今日はいい天気です。'
text = text.encode('utf-8')
s1 = create_string_buffer(text, 200)
s2 = create_string_buffer('out2.wav', 20)
e = h.libopen_jtalk_main(s1, s2)
print e
# print c_char_p(h.method).value

lib = cdll.LoadLibrary("C:\\MeCab\\bin\\libmecab.dll")
tagger = lib.mecab_new2("mecab " + "-Oyomi")
s = lib.mecab_sparse_tostr(tagger, text)
ret = c_char_p(s).value
lib.mecab_destroy(tagger)
print ret
