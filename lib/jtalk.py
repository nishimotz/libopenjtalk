# jtalk.py 
# -*- coding: utf-8 -*-
# a speech engine for nvdajp
# based on Open-JTalk
# by Takuya Nishimoto
import os
from ctypes import *

mcdic = r"C:\openjtalk\open_jtalk_dic_utf_8-1.00"
voice = r"C:\openjtalk\hts_voice_nitech_jp_atr503_m001-1.01"

##############################################

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

############################################

# htsengineapi/include/HTS_engine.h

# size of structure:
# HTS_Global     56
# HTS_ModelSet   76
# HTS_Label      24
# HTS_SStreamSet 24
# HTS_PStreamSet 12
# HTS_GStreamSet 20

c_double_p = POINTER(c_double)
c_double_p_p = POINTER(c_double_p) 

class HTS_ModelSet(Structure):
	_fields_ = [
		("_dummy", c_byte * 56),
	]

class HTS_Label(Structure):
	_fields_ = [
		("_dummy", c_byte * 76),
	]

class HTS_SStreamSet(Structure):
	_fields_ = [
		("_dummy", c_byte * 24),
	]

class HTS_PStreamSet(Structure):
	_fields_ = [
		("_dummy", c_byte * 12),
	]

class HTS_GStreamSet(Structure):
	_fields_ = [
		("_dummy", c_byte * 20),
	]

class HTS_Global(Structure):
	_fields_ = [
		("state", c_int), 		# /* Gamma=-1/stage : if stage=0 then Gamma=0 */
		("use_log_gain", c_int), 	# HTS_Boolean (TRUE=1) /* log gain flag (for LSP) */
		("sampling_rate", c_int), 	# /* sampling rate */
		("fperiod", c_int),		# /* frame period */
		("alpha", c_double),		# /* all-pass constant */
		("beta", c_double),		# /* postfiltering coefficient */
		("audio_buff_size", c_int),	# /* audio buffer size (for audio device) */
		("msd_threshold", c_double_p),	# /* MSD thresholds */
		("duration_iw", c_double_p),	# /* weights for duration interpolation */
		("parameter_iw", c_double_p_p),	# /* weights for parameter interpolation */
		("gv_iw", c_double_p_p),	# /* weights for GV interpolation */
		("gv_weight", c_double_p),	# /* GV weights */
	]
HTS_Global_ptr = POINTER(HTS_Global)

class HTS_Engine(Structure):
	_fields_ = [
		("global", HTS_Global),
		("ms", HTS_ModelSet),
		("label", HTS_Label),
		("sss", HTS_SStreamSet),
		("pss", HTS_PStreamSet),
		("gss", HTS_GStreamSet),
	]
HTS_Engine_ptr = POINTER(HTS_Engine)

############################################

class NJD(Structure):
	_fields_ = [
		("_dummy", c_byte * 8),
	]
NJD_ptr = POINTER(NJD)

class JPCommon(Structure):
	_fields_ = [
		("_dummy", c_byte * 12),
	]
JPCommon_ptr = POINTER(JPCommon)

############################################

mecab = None
libmc = None

def Mecab_initialize():
	global mecab, libmc
	libmc = cdll.LoadLibrary(r"C:\MeCab\bin\libmecab.dll")
	mecab = libmc.mecab_new2(r"mecab -d " + mcdic)
	# s = libmc.mecab_sparse_tostr(mecab, text)
	# ret = c_char_p(s).value
	# print ret
	libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr

############################################

njd = NJD()
jpcommon = JPCommon()
engine = HTS_Engine()
libjt = None

def OpenJTalk_initialize():
	global libjt
	libjt = cdll.LoadLibrary("libopenjtalk.dll")

	libjt.NJD_initialize.argtypes = [NJD_ptr]
	e = libjt.NJD_initialize(njd)

	libjt.JPCommon_initialize.argtypes = [JPCommon_ptr]
	e = libjt.JPCommon_initialize(jpcommon)

	libjt.HTS_Engine_initialize.argtypes = [HTS_Engine_ptr, c_int]
	e = libjt.HTS_Engine_initialize(engine, 2);
	
	libjt.HTS_Engine_set_sampling_rate.argtypes = [HTS_Engine_ptr, c_int]
	e = libjt.HTS_Engine_set_sampling_rate(engine, 16000);
	
	libjt.HTS_Engine_set_fperiod.argtypes = [HTS_Engine_ptr, c_int]
	e = libjt.HTS_Engine_set_fperiod(engine, 80);

	libjt.HTS_Engine_set_alpha.argtypes = [HTS_Engine_ptr, c_double]
	e = libjt.HTS_Engine_set_alpha(engine, 0.42);

	libjt.HTS_Engine_set_gamma.argtypes = [HTS_Engine_ptr, c_int]
	e = libjt.HTS_Engine_set_gamma(engine, 0);
	
	libjt.HTS_Engine_set_log_gain.argtypes = [HTS_Engine_ptr, c_int]
	e = libjt.HTS_Engine_set_log_gain(engine, 0);
	
	libjt.HTS_Engine_set_beta.argtypes = [HTS_Engine_ptr, c_double]
	e = libjt.HTS_Engine_set_beta(engine, 0.0);
	
	libjt.HTS_Engine_set_audio_buff_size.argtypes = [HTS_Engine_ptr, c_int]
	e = libjt.HTS_Engine_set_audio_buff_size(engine, 1600);
	
	libjt.HTS_Engine_set_msd_threshold.argtypes = [HTS_Engine_ptr, c_int, c_double]
	e = libjt.HTS_Engine_set_msd_threshold(engine, 1, 0.5);
	
	libjt.HTS_Engine_set_gv_weight.argtypes = [HTS_Engine_ptr, c_int, c_double]
	e = libjt.HTS_Engine_set_gv_weight(engine, 0, 1.0);
	e = libjt.HTS_Engine_set_gv_weight(engine, 1, 0.7);

############################################

def main():
	#global mecab
	#text = u'こんにちは。今日はいい天気です。'
	text = u'今日は。'
	text = text.encode('utf-8')
	Mecab_initialize()
	OpenJTalk_initialize()

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

if __name__ == "__main__":
	main()
