# jtalk.py 
# -*- coding: utf-8 -*-
# a speech engine for nvdajp
# based on Open-JTalk
# by Takuya Nishimoto
import os
from ctypes import *

DIC = r"C:\openjtalk\open_jtalk_dic_utf_8-1.00"
VOICE = r"C:\openjtalk\hts_voice_nitech_jp_atr503_m001-1.01"

c_double_p = POINTER(c_double)
c_double_p_p = POINTER(c_double_p) 
c_char_p_p = POINTER(c_char_p) 

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

# typedef struct _Mecab{
#    char **feature;
#    int size;
#    mecab_t *mecab;
# } Mecab;

FELEN   = 1000 # string len
FECOUNT = 100
FEATURE = c_char * FELEN
FEATURE_ptr = POINTER(FEATURE)
FEATURE_ptr_array = FEATURE_ptr * FECOUNT
FEATURE_ptr_array_ptr = POINTER(FEATURE_ptr_array)

mecab = None
libmc = None
mecab_feature = None
mecab_size = None

def Mecab_initialize():
	global libmc
	global mecab_feature, mecab_size
	libmc = cdll.LoadLibrary(r"C:\MeCab\bin\libmecab.dll")
	libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr
	mecab_size = 0
	mecab_feature = FEATURE_ptr_array()
	for i in xrange(0, FECOUNT):
		buf = create_string_buffer(FELEN)
		mecab_feature[i] = cast(byref(buf), FEATURE_ptr)

def Mecab_load():
	global mecab
	mecab = libmc.mecab_new2(r"mecab -d " + DIC)
	libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr

def Mecab_analysis(str):
	global mecab_size
	head = libmc.mecab_sparse_tonode(mecab, str)
	if head == None: return [None, None]
	mecab_size = 0

	# make array of features
	node = head
	i = 0
	while node:
		s = node[0].stat
		if s != MECAB_BOS_NODE and s != MECAB_EOS_NODE:
			c = node[0].length
			s = string_at(node[0].surface, c) + "," + string_at(node[0].feature)
			print s.decode('utf-8') # for debug
			buf = create_string_buffer(s)
# 			dst_ptr = mecab_feature[i]
# 			src_ptr = byref(buf)
# 			memmove(dst_ptr, src_ptr, len(s)+1)
			i += 1
		node = node[0].next
		mecab_size = i
		if i > FECOUNT: return [mecab_feature, mecab_size]

	# for debug
	print "size:", mecab_size
	for i in xrange(0, mecab_size):
		print string_at(mecab_feature[i])
	
	return [mecab_feature, mecab_size]

def Mecab_refresh():
	global mecab_size
	mecab_size = 0
	pass

def Mecab_clear():
	libmc.mecab_destroy(mecab)

############################################

# htsengineapi/include/HTS_engine.h

# size of structure:
# HTS_Global     56
# HTS_ModelSet   76
# HTS_Label      24
# HTS_SStreamSet 24
# HTS_PStreamSet 12
# HTS_GStreamSet 20

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

njd = NJD()
jpcommon = JPCommon()
engine = HTS_Engine()
libjt = None

def OpenJTalk_initialize():
	global libjt
	libjt = cdll.LoadLibrary("libopenjtalk.dll")

	libjt.NJD_initialize.argtypes = [NJD_ptr]
	libjt.NJD_initialize(njd)

	libjt.JPCommon_initialize.argtypes = [JPCommon_ptr]
	libjt.JPCommon_initialize(jpcommon)

	libjt.HTS_Engine_initialize.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_initialize(engine, 2);
	
	libjt.HTS_Engine_set_sampling_rate.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_sampling_rate(engine, 16000);
	
	libjt.HTS_Engine_set_fperiod.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_fperiod(engine, 80);

	libjt.HTS_Engine_set_alpha.argtypes = [HTS_Engine_ptr, c_double]
	libjt.HTS_Engine_set_alpha(engine, 0.42);

	libjt.HTS_Engine_set_gamma.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_gamma(engine, 0);
	
	libjt.HTS_Engine_set_log_gain.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_log_gain(engine, 0);
	
	libjt.HTS_Engine_set_beta.argtypes = [HTS_Engine_ptr, c_double]
	libjt.HTS_Engine_set_beta(engine, 0.0);
	
	libjt.HTS_Engine_set_audio_buff_size.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_audio_buff_size(engine, 1600);
	
	libjt.HTS_Engine_set_msd_threshold.argtypes = [HTS_Engine_ptr, c_int, c_double]
	libjt.HTS_Engine_set_msd_threshold(engine, 1, 0.5);
	
	libjt.HTS_Engine_set_gv_weight.argtypes = [HTS_Engine_ptr, c_int, c_double]
	libjt.HTS_Engine_set_gv_weight(engine, 0, 1.0);
	libjt.HTS_Engine_set_gv_weight(engine, 1, 0.7);

FNLEN = 1000
FILENAME = c_char * FNLEN
FILENAME_ptr = POINTER(FILENAME)
FILENAME_ptr_ptr = POINTER(FILENAME_ptr)
FILENAME_ptr_x3 = FILENAME_ptr * 3
FILENAME_ptr_x3_ptr = POINTER(FILENAME_ptr_x3)

def OpenJTalk_load():
	libjt.HTS_Engine_load_duration_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr_ptr, FILENAME_ptr_ptr, c_int]
	
	fn_ms_dur_buf = create_string_buffer(VOICE + "/dur.pdf", FNLEN)
	fn_ms_dur_buf_ptr = cast(byref(fn_ms_dur_buf), FILENAME_ptr)
	fn_ms_dur = cast(byref(fn_ms_dur_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_dur_buf = create_string_buffer(VOICE + "/tree-dur.inf", FNLEN)
	fn_ts_dur_buf_ptr = cast(byref(fn_ts_dur_buf), FILENAME_ptr)
	fn_ts_dur = cast(byref(fn_ts_dur_buf_ptr), FILENAME_ptr_ptr)
	libjt.HTS_Engine_load_duration_from_fn(engine, fn_ms_dur, fn_ts_dur, 1)
	
	libjt.HTS_Engine_load_parameter_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr_ptr, FILENAME_ptr_ptr,
		FILENAME_ptr_x3_ptr, c_int, c_int, c_int, c_int]
	
	fn_ms_mcp_buf = create_string_buffer(VOICE + "/mgc.pdf", FNLEN)
	fn_ms_mcp_buf_ptr = cast(byref(fn_ms_mcp_buf), FILENAME_ptr)
	fn_ms_mcp = cast(byref(fn_ms_mcp_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_mcp_buf = create_string_buffer(VOICE + "/tree-mgc.inf", FNLEN)
	fn_ts_mcp_buf_ptr = cast(byref(fn_ts_mcp_buf), FILENAME_ptr)
	fn_ts_mcp = cast(byref(fn_ts_mcp_buf_ptr), FILENAME_ptr_ptr)
	fn_ws_mcp_buf_1 = create_string_buffer(VOICE + "/mgc.win1", FNLEN)
	fn_ws_mcp_buf_2 = create_string_buffer(VOICE + "/mgc.win2", FNLEN)
	fn_ws_mcp_buf_3 = create_string_buffer(VOICE + "/mgc.win3", FNLEN)
	fn_ws_mcp_buf_ptr_x3 = FILENAME_ptr_x3(
		cast(byref(fn_ws_mcp_buf_1), FILENAME_ptr),
		cast(byref(fn_ws_mcp_buf_2), FILENAME_ptr),
		cast(byref(fn_ws_mcp_buf_3), FILENAME_ptr))
	fn_ws_mcp = cast(byref(fn_ws_mcp_buf_ptr_x3), FILENAME_ptr_x3_ptr)
	libjt.HTS_Engine_load_parameter_from_fn(
		engine, fn_ms_mcp, fn_ts_mcp, fn_ws_mcp, 
		0, 0, 3, 1)
	
	fn_ms_lf0_buf = create_string_buffer(VOICE + "/lf0.pdf", FNLEN)
	fn_ms_lf0_buf_ptr = cast(byref(fn_ms_lf0_buf), FILENAME_ptr)
	fn_ms_lf0 = cast(byref(fn_ms_lf0_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_lf0_buf = create_string_buffer(VOICE + "/tree-lf0.inf", FNLEN)
	fn_ts_lf0_buf_ptr = cast(byref(fn_ts_lf0_buf), FILENAME_ptr)
	fn_ts_lf0 = cast(byref(fn_ts_lf0_buf_ptr), FILENAME_ptr_ptr)
	fn_ws_lf0_buf_1 = create_string_buffer(VOICE + "/lf0.win1", FNLEN)
	fn_ws_lf0_buf_2 = create_string_buffer(VOICE + "/lf0.win2", FNLEN)
	fn_ws_lf0_buf_3 = create_string_buffer(VOICE + "/lf0.win3", FNLEN)
	fn_ws_lf0_buf_ptr_x3 = FILENAME_ptr_x3(
		cast(byref(fn_ws_lf0_buf_1), FILENAME_ptr),
		cast(byref(fn_ws_lf0_buf_2), FILENAME_ptr),
		cast(byref(fn_ws_lf0_buf_3), FILENAME_ptr))
	fn_ws_lf0 = cast(byref(fn_ws_lf0_buf_ptr_x3), FILENAME_ptr_x3_ptr)
	libjt.HTS_Engine_load_parameter_from_fn(
		engine, fn_ms_lf0, fn_ts_lf0, fn_ws_lf0, 
		1, 1, 3, 1)
	
	libjt.HTS_Engine_load_gv_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr_ptr, FILENAME_ptr_ptr, 
		c_int, c_int]

	fn_ms_gvm_buf = create_string_buffer(VOICE + "/gv-mgc.pdf", FNLEN)
	fn_ms_gvm_buf_ptr = cast(byref(fn_ms_gvm_buf), FILENAME_ptr)
	fn_ms_gvm = cast(byref(fn_ms_gvm_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_gvm_buf = create_string_buffer(VOICE + "/tree-gv-mgc.inf", FNLEN)
	fn_ts_gvm_buf_ptr = cast(byref(fn_ts_gvm_buf), FILENAME_ptr)
	fn_ts_gvm = cast(byref(fn_ts_gvm_buf_ptr), FILENAME_ptr_ptr)
	libjt.HTS_Engine_load_gv_from_fn(
		engine, fn_ms_gvm, fn_ts_gvm, 0, 1)

	fn_ms_gvl_buf = create_string_buffer(VOICE + "/gv-lf0.pdf", FNLEN)
	fn_ms_gvl_buf_ptr = cast(byref(fn_ms_gvl_buf), FILENAME_ptr)
	fn_ms_gvl = cast(byref(fn_ms_gvl_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_gvl_buf = create_string_buffer(VOICE + "/tree-gv-lf0.inf", FNLEN)
	fn_ts_gvl_buf_ptr = cast(byref(fn_ts_gvl_buf), FILENAME_ptr)
	fn_ts_gvl = cast(byref(fn_ts_gvl_buf_ptr), FILENAME_ptr_ptr)
	libjt.HTS_Engine_load_gv_from_fn(
		engine, fn_ms_gvl, fn_ts_gvl, 1, 1)

	libjt.HTS_Engine_load_gv_switch_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr]

	fn_gv_switch_buf = create_string_buffer(VOICE + "/gv-switch.inf", FNLEN)
	fn_gv_switch = cast(byref(fn_gv_switch_buf), FILENAME_ptr)
	libjt.HTS_Engine_load_gv_switch_from_fn(
		engine, fn_gv_switch)

def OpenJTalk_text2mecab(buff, txt):
	libjt.text2mecab(buff, txt)

def OpenJTalk_synthesis(feature, size):
	if feature == None or size == None: return
	print "starting OpenJTalk_synthesis, size:", size
	libjt.mecab2njd.argtypes = [NJD_ptr, FEATURE_ptr_array_ptr, c_int]
	libjt.mecab2njd(njd, feature, size)
	print "done"

def OpenJTalk_clear():
	pass

############################################

def main():
	#global mecab
	#text = u'こんにちは。今日はいい天気です。'
	text = u'今日ABC'
	text = text.encode('utf-8')

	# Notice: Mecab is separated from OpenJTalk
	Mecab_initialize()
	Mecab_load()
	
	OpenJTalk_initialize()
	OpenJTalk_load()

	buff = create_string_buffer(len(text) * 2 + 1)
	OpenJTalk_text2mecab(buff, text)
	print buff.value.decode('utf-8')

	[feature, size] = Mecab_analysis(buff.value)
	OpenJTalk_synthesis(feature, size)

	OpenJTalk_clear()
	Mecab_clear()

if __name__ == "__main__":
	main()
