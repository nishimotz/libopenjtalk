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
		[u'複数行', 	u'フクスーギョー',		"3/6"],
		[u'行操作',		u'ギョーソーサ',		"1/5"],
		[u'空要素',		u'カラヨーソ',			"3/5"],
		[u'ニコ生',		u'ニコナマ',			"0/4"],
		[u'スリーマイル島原発',	u'スリーマイルトーゲンパツ'],

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
		[u'一人ひとり', u'ヒトリヒトリ',		"0/6"],
		[u'日中', 		u'ニッチュー',			"3/4"],
		[u'次',			u'ツギ',				"2/2", 5000],
		[u'他人事',		u'タニンゴト',			"0/5"],
		[u'セブン―イレブン', 	u'セブンイレブン',				"5/7"],
		[u'東国原',		u'ヒガシコクバル',		"5/7"],
		[u'中越',		u'チューエツ',			"1/4"],
		[u'発災',		u'ハッサイ',			"0/4"],
		[u'その上',		u'ソノウエ',			"0/4"],
		[u'時期',		u'ジキ',				"1/2"],
		[u'扱い',		u'アツカイ',			"0/4"],
		[u'停波',		u'テーハ',				"0/3"],
		[u'建屋',		u'タテヤ',				"2/3"],
		[u'なう',		u'ナウ',				"1/2"],
		[u'被り',		u'カブリ',				"0/3"],
		[u'寺田寅彦',	u'テラダトラヒコ',		"0/7"],
		[u'橋下知事',	u'ハシモトチジ',		"0/6"],
		[u'フレッツ光',	u'フレッツヒカリ',		"2/7"],
		[u'選択行',		u'センタクギョー',		"0/6"],
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
