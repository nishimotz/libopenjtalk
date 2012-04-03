# roma_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2011-04-06 by Takuya Nishimoto

OUT_FILE = 'nvdajp-roma-dic.csv'
CODE = 'cp932'

import sys
import re

romadic = [
		# third item is number of morae
		['bba', 		u'ッバ', 			2],
		['bbi', 		u'ッビ', 			2],
		['bbu', 		u'ッブ', 			2],
		['bbe', 		u'ッベ', 			2],
		['bbo', 		u'ッボ', 			2],
		#
		['ccha', 		u'ッチャ', 			2],
		['cchi', 		u'ッチ', 			2],
		['cchu', 		u'ッチュ', 			2],
		['cche', 		u'ッチェ', 			2],
		['ccho', 		u'ッチョ', 			2],
		#
		['dda', 		u'ッダ', 			2],
		['ddi', 		u'ッジ', 			2],
		['ddu', 		u'ッヅ', 			2],
		['dde', 		u'ッデ', 			2],
		['ddo', 		u'ッド', 			2],
		#
		['ffa', 		u'ッファ', 			2],
		['ffi', 		u'ッフィ', 			2],
		['ffu', 		u'ッフ', 			2],
		['ffe', 		u'ッフェ', 			2],
		['ffo', 		u'ッフォ', 			2],
		#
		['gga', 		u'ッガ', 			2],
		['ggi', 		u'ッギ', 			2],
		['ggu', 		u'ッグ', 			2],
		['gge', 		u'ッゲ', 			2],
		['ggo', 		u'ッゴ', 			2],
		#
		['hha', 		u'ッハ', 			2],
		['hhi', 		u'ッヒ', 			2],
		['hhu', 		u'ッフ', 			2],
		['hhe', 		u'ッヘ', 			2],
		['hho', 		u'ッホ', 			2],
		#
		['jja', 		u'ッジャ', 			2],
		['jji', 		u'ッジ', 			2],
		['jju', 		u'ッジュ', 			2],
		['jje', 		u'ッジェ', 			2],
		['jjo', 		u'ッジョ', 			2],
		#
		['kka', 		u'ッカ', 			2],
		['kki', 		u'ッキ', 			2],
		['kku', 		u'ック', 			2],
		['kke', 		u'ッケ', 			2],
		['kko', 		u'ッコ', 			2],
		#
		['ppa', 		u'ッパ', 			2],
		['ppi', 		u'ッピ', 			2],
		['ppu', 		u'ップ', 			2],
		['ppe', 		u'ッペ', 			2],
		['ppo', 		u'ッポ', 			2],
		#
		['ssa', 		u'ッサ', 			2],
		['ssi', 		u'ッシ', 			2],
		['ssu', 		u'ッス', 			2],
		['sse', 		u'ッセ', 			2],
		['sso', 		u'ッソ', 			2],
		#
		['tta', 		u'ッタ', 			2],
		['tti', 		u'ッチ', 			2],
		['ttu', 		u'ッツ', 			2],
		['tte', 		u'ッテ', 			2],
		['tto', 		u'ット', 			2],
		#
		['zza', 		u'ッザ', 			2],
		['zzi', 		u'ッジ', 			2],
		['zzu', 		u'ッズ', 			2],
		['zze', 		u'ッゼ', 			2],
		['zzo', 		u'ッゾ', 			2],
		#
		['cha', 		u'チャ', 			1],
		['chu', 		u'チュ', 			1],
		['cho', 		u'チョ', 			1],
		#
		['tsu', 		u'ツ', 				1],
		#
		['ka', 			u'カ', 				1],
		['ki', 			u'キ', 				1],
		['ku', 			u'ク', 				1],
		['ke', 			u'ケ', 				1],
		['ko', 			u'コ', 				1],
		#
		['tya', 		u'チャ', 			1],
		['tyu', 		u'チュ', 			1],
		['tyo', 		u'チョ', 			1],
		#
		['jya', 		u'ジャ', 			1],
		['jyu', 		u'ジュ', 			1],
		['jyo', 		u'ジョ', 			1],
		#
		['kya', 		u'キャ', 			1],
		['kyu', 		u'キュ', 			1],
		['kyo', 		u'キョ', 			1],
		#
		['ga', 			u'ガ', 				1],
		['gi', 			u'ギ', 				1],
		['gu', 			u'グ', 				1],
		['ge', 			u'ゲ', 				1],
		['go', 			u'ゴ', 				1],
		#
		['gya', 		u'ギャ', 			1],
		['gyu', 		u'ギュ', 			1],
		['gyo', 		u'ギョ', 			1],
		#
		['sa', 			u'サ', 				1],
		['si', 			u'シ', 				1],
		['shi', 		u'シ', 				1],
		['su', 			u'ス', 				1],
		['se', 			u'セ', 				1],
		['so', 			u'ソ', 				1],
		#
		['sya', 		u'シャ', 			1],
		['syu', 		u'シュ', 			1],
		['syo', 		u'ショ', 			1],
		#
		['sha', 		u'シャ', 			1],
		['shu', 		u'シュ', 			1],
		['sho', 		u'ショ', 			1],
		#
		['za', 			u'ザ', 				1],
		['zi', 			u'ジ', 				1],
		['ji', 			u'ジ', 				1],
		['zu', 			u'ズ', 				1],
		['ze', 			u'ゼ', 				1],
		['zo', 			u'ゾ', 				1],
		#
		['ja', 			u'ジャ', 			1],
		['ju', 			u'ジュ', 			1],
		['jo', 			u'ジョ', 			1],
		#
		['ta', 			u'タ', 				1],
		['ti', 			u'チ', 				1],
		['chi', 		u'チ', 				1],
		['tu', 			u'ツ', 				1],
		['te', 			u'テ', 				1],
		['to', 			u'ト', 				1],
		#
		['da', 			u'ダ', 				1],
		['di', 			u'ヂ', 				1],
		['du', 			u'ヅ', 				1],
		['de', 			u'デ', 				1],
		['do', 			u'ド', 				1],
		#
		['na', 			u'ナ', 				1],
		['ni', 			u'ニ', 				1],
		['nu', 			u'ヌ', 				1],
		['ne', 			u'ネ', 				1],
		['no', 			u'ノ', 				1],
		#
		['nn', 			u'ン', 				1],
		#
		['nya', 		u'ニャ', 			1],
		['nyu', 		u'ニュ', 			1],
		['nyo', 		u'ニョ', 			1],
		#
		['ha', 			u'ハ', 				1],
		['hi', 			u'ヒ', 				1],
		['hu', 			u'フ', 				1],
		['he', 			u'ヘ', 				1],
		['ho', 			u'ホ', 				1],
		#
		['hya', 		u'ヒャ', 			1],
		['hyu', 		u'ヒュ', 			1],
		['hyo', 		u'ヒョ', 			1],
		#
		['fa', 			u'ファ', 			1],
		['fi', 			u'フィ', 			1],
		['fu', 			u'フ', 				1],
		['fe', 			u'フェ', 			1],
		['fo', 			u'フォ', 			1],
		#
		['ba', 			u'バ', 				1],
		['bi', 			u'ビ', 				1],
		['bu', 			u'ブ', 				1],
		['be', 			u'ベ', 				1],
		['bo', 			u'ボ', 				1],
		#
		['pa', 			u'パ', 				1],
		['pi', 			u'ピ', 				1],
		['pu', 			u'プ', 				1],
		['pe', 			u'ペ', 				1],
		['po', 			u'ポ', 				1],
		#
		['pya', 		u'ピャ', 			1],
		['pyu', 		u'ピュ', 			1],
		['pyo', 		u'ピョ', 			1],
		#
		['ma', 			u'マ',				1],
		['mi', 			u'ミ',				1],
		['mu', 			u'ム',				1],
		['me', 			u'メ',				1],
		['mo', 			u'モ',				1],
		#
		['mya', 		u'ミャ', 			1],
		['myu', 		u'ミュ', 			1],
		['myo', 		u'ミョ', 			1],
		#
		['rya', 		u'リャ', 			1],
		['ryu', 		u'リュ', 			1],
		['ryo', 		u'リョ', 			1],
		#
		['ya', 			u'ヤ',				1],
		['yu', 			u'ユ',				1],
		['yo', 			u'ヨ',				1],
		#
		['ra', 			u'ラ',				1],
		['ri', 			u'リ',				1],
		['ru', 			u'ル',				1],
		['re', 			u'レ',				1],
		['ro', 			u'ロ',				1],
		#
		['wa', 			u'ワ',				1],
		['wi', 			u'ウィ',			1],
		['wo', 			u'オ',				1],
		# 
		['a', 			u'ア', 				1],
		['i', 			u'イ', 				1],
		['u', 			u'ウ', 				1],
		['e', 			u'エ', 				1],
		['o', 			u'オ', 				1],
	]

def alpha2mb(s):
        # 'abc' -> 'ａｂｃ'
        import string
        from_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        to_table = u'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
        result = ''
        for ch in s:
                pos = string.find(from_table, ch)
                if pos >= 0:
                        result += to_table[pos]
        return result


def make_dic():
	with open(OUT_FILE, "w") as file:
		## romadic
		cost = 500.0
		step = 0.5
		for i in romadic:
			try:
				k = i[0]
				for p in [('a', u'ア'), ('i', u'イ'), ('u', u'ウ'), ('e', u'エ'), ('o', u'オ')]:
					k1 = k1 = alpha2mb(k.lower() + p[0])
					y = i[1] + p[1] + u'ー'
					pros = "%d/%d" % (0, i[2] + 2)
					# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
					s = u"%s,-1,-1,%.1f,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
					file.write(s.encode(CODE))
				cost += step
				for p in [('a', u'ア'), ('i', u'イ'), ('u', u'ウ'), ('e', u'エ'), ('o', u'オ')]:
					k1 = k1 = alpha2mb(p[0] + k.lower())
					y = p[1] + i[1] + u'ー'
					pros = "%d/%d" % (0, i[2] + 2)
					# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
					s = u"%s,-1,-1,%.1f,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
					file.write(s.encode(CODE))
				cost += step
			except Exception, e:
				print e
		for i in romadic:
			try:
				k = i[0]
				if k != 'nn':
					k1 = k1 = alpha2mb(k.lower() + 'x')
					y = i[1] + u'ックスー'
					pros = "%d/%d" % (0, i[2] + 4)
					# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
					s = u"%s,-1,-1,%.1f,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
					file.write(s.encode(CODE))
					cost += step
			except Exception, e:
				print e
		for i in romadic:
			try:
				k = i[0]
				if k != 'nn':
					k1 = k1 = alpha2mb(k.lower() + 'n')
					y = i[1] + u'ンー'
					pros = "%d/%d" % (0, i[2] + 2)
					# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
					s = u"%s,-1,-1,%.1f,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
					file.write(s.encode(CODE))
					cost += step
			except Exception, e:
				print e
		for i in romadic:
			try:
				k = i[0]
				if len(k) != 1:
					k1 = k1 = alpha2mb(k.lower())
					y = i[1] + u'ー'
					pros = "%d/%d" % (0, i[2] + 1)
					# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
					s = u"%s,-1,-1,%.1f,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
					file.write(s.encode(CODE))
					cost += step
			except Exception, e:
				print e

if __name__ == '__main__':
	make_dic()
