# custom_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2011-01-19 by Takuya Nishimoto

OUT_FILE = 'nvdajp-custom-dic.csv'

import sys
import re

jdic = [
		# first item should use zenkaku charactors
		[u'読み込み中',	u'ヨミコミチュー',		"2/6"],
		[u'一行', 		u'イチギョー',			"2/4"],
		[u'１行', 		u'イチギョー',			"2/4"],
		[u'２行', 		u'ニギョー',			"1/3"],
		[u'３行', 		u'サンギョー',			"1/4"],
		[u'空行', 		u'クーギョー',			"0/4"],
		[u'行末', 		u'ギョーマツ',			"0/4"],
		[u'複数行', 	u'フクスーギョー'		"3/6"],

		[u'孫正義', 	u'ソンマサヨシ', 		"4/6"],
		[u'池田信夫',	u'イケダノブオ',		"0/6"],
		[u'方々',		u'カタガタ',			"2/4"],
		[u'当分の間',	u'トーブンノアイダ',	"0/8"],
		[u'中通り',		u'ナカドーリ',			"3/5"],
		[u'中',			u'チュー',				"1/2", 5000],
		[u'中の人',		u'ナカノヒト',			"1/5"],
		[u'中程度',		u'チューテード',		"3/5"],
		[u'各基',		u'カクキ',				"1/3"],
		[u'高',			u'コー',				"1/2", 5000],
		[u'県立高',		u'ケンリツコー',		"0/6"],
		[u'業務',		u'ギョーム',			"1/3"],
		[u'値',			u'アタイ',				"0/3"],
		[u'２４時間', 	u'ニジューヨジカン'		"1/7"],
		[u'明朝',		u'ミンチョー',			"1/4"],
		[u'障がい',		u'ショーガイ',			"0/4"],
		[u'蓮舫', 		u'レンホー',			"1/4"],
		[u'既読', 		u'キドク',				"0/3"],
		[u'新家', 		u'シンケ',				"1/3"],
		[u'大嘘', 		u'オーウソ',			"0/4"],
		[u'１人', 		u'ヒトリ',				"2/3"],
		[u'一人ひとり', 		u'ヒトリヒトリ',				"0/6"],
		[u'日中', 		u'ニッチュー',			"3/4"],
		[u'次',			u'ツギ',				"2/2", 5000],
		[u'他人事',		u'タニンゴト',			"0/5"],
		[u'セブン―イレブン', 	u'セブンイレブン',				"5/7"],
		[u'東国原',		u'ヒガシコクバル',		"5/7"],
		[u'中越',		u'チューエツ',			"1/4"],
		[u'発災',		u'ハッサイ',			"0/4"],
		[u'その上',		u'ソノウエ',			"0/4"],
		[u'時期',		u'ジキ',				"1/2"],
	]

edic = [
		# first field should use single-byte charactors
		['anpi', 		u'アンピ',			"1/3"],
		['asian',		u'アジアン',		"1/4"],
		['asahi', 		u'アサヒ'			"1/3"],
		['edu',			u'エデュー',		"1/3"],
		['gamba', 		u'ガンバ', 			"1/3"],
		['genpatsu',	u'ゲンパツ',		"1/4"],
		['hinan', 		u'ヒナン', 			"1/3"],
		['horijun',		u'ホリジュン',		"1/4"],
		['inosenaoki'	u'イノセナオキ',	"1/7"],
		['kahoku', 		u'カホク', 			"1/3"],
		['kurogen',		u'クロゲン',		"1/4"],
		['medic', 		u'メディック',		"1/4"],
		['miz',			u'ミズ',			"2/2"],
		['minpo', 		u'ミンポー',		"1/4"],
		['seikatsu',	u'セーカツ',		"1/4"],
		['sagas',		u'サガス',			"1/3"],
		['shimpo', 		u'シンポー', 		"1/4"],
		['shimbun', 	u'シンブン'			"1/4"],
		['teiden', 		u'テーデン',		"1/4"],
		['tokuho',		u'トクホー',		"1/4"],
		['takeyama', 	u'タケヤマ',		"1/4"],
		['pref', 		u'プリフ',			"1/3"],
		['wikipedia', 	u'ウイキペディーア',	"0/8"],
		['tepco', 		u'テプコ',			"1/3"],
		['akb', 		u'エーケービー',		"1/6"],
		['npo', 		u'エヌピーオー',		"2/6"],

		['opensource', 	u'オープンソース'],
		['notepad', 	u'ノートパッド'],
		['guidebook', 	u'ガイドブック'],
		['blog', 		u'ブログ'],
		['matlab', 		u'マトラブ'],
		['keyboard', 	u'キーボード'],
		['plugins', 	u'プラグインズ'],
		['facebook', 	u'フェイスブック'],
		['desktop', 	u'デスクトップ'],
		['output', 		u'アウトプット'],
		['nullsoft', 	u'ヌルソフト'],
		['cygdrive', 	u'シグドライブ'],
		['ustream', 	u'ユーストリーム'],
		['ubuntu', 		u'ウブンツー'],
		['ware', 		u'ウェアー'],
		['id', 			u'アイディー'],
		['it', 			u'アイティー'],
		['time', 		u'タイム'],
		['home', 		u'ホーム'],
		['nvda', 		u'エヌブイディーエー', 					"1/8"],
		['jp', 			u'ジェーピー', 			"1/4"],
		['co', 			u'シーオー', 			"1/4"],
		['usb', 		u'ユーエスビー',		"1/6"],
		['faq', 		u'エフエーキュー',		"1/6"],
		['iaea', 		u'アイエーイーエー',		"7/8"],
		
		['morioka', 	u'モリオカ', 		"2/4"],
		['miyagi', 		u'ミヤギ',			"1/3"],
		['fukushima', 	u'フクシマ', 		"2/4"],
		['niigata', 	u'ニーガタ', 		"0/4"],
		['hokkaido', 	u'ホッカイドー'],
		['yamagata', 	u'ヤマガタ'],
		['akita', 		u'アキタ'],
		['aomori', 		u'アオモリ'],
		['iwate', 		u'イワテ'],
		['tsukuba', 	u'ツクバ'],
		['oshu', 		u'オーシュー'],
		['hachinohe', 	u'ハチノヘ'],
		['kesennuma', 	u'ケセンヌマ'],
		['kantei', 		u'カンテー'],
		['saigai', 		u'サイガイ'],
		['tochigi', 	u'トチギ'],
		['kashima', 	u'カシマ'],
		['yahoo', 		u'ヤフー',			"2/3"],
		['japan', 		u'ジャパン',		"2/3"],
	]

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


if __name__ == '__main__':
	with open(OUT_FILE, "w") as file:
		## edic
		for i in edic:
			try:
				k = i[0]
				k1 = alpha2mb(k.lower())
				y = i[1]
				mora_count = len(y)
				pros = "0/%d" % mora_count
				cost = 1000 # eng_dic_maker cost=1800
				if len(i) >= 3: pros = i[2]
				if len(i) >= 4: cost = i[3]
				# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
				s = u"%s,-1,-1,%d,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
				file.write(s.encode('cp932'))
			except Exception, e:
				print e
		## jdic
		for i in jdic:
			try:
				k = i[0]
				k1 = k
				y = i[1]
				mora_count = len(y)
				pros = "0/%d" % mora_count
				cost = 1000
				if len(i) >= 3: pros = i[2]
				if len(i) >= 4: cost = i[3]
				# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
				s = u"%s,-1,-1,%d,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
				file.write(s.encode('cp932'))
			except Exception, e:
				print e
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
					file.write(s.encode('cp932'))
				cost += step
				for p in [('a', u'ア'), ('i', u'イ'), ('u', u'ウ'), ('e', u'エ'), ('o', u'オ')]:
					k1 = k1 = alpha2mb(p[0] + k.lower())
					y = p[1] + i[1] + u'ー'
					pros = "%d/%d" % (0, i[2] + 2)
					# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
					s = u"%s,-1,-1,%.1f,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
					file.write(s.encode('cp932'))
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
					file.write(s.encode('cp932'))
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
					file.write(s.encode('cp932'))
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
					file.write(s.encode('cp932'))
					cost += step
			except Exception, e:
				print e
