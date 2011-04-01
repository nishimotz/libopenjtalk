# eng_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2010-12-05 by Takuya Nishimoto

IN_FILE  = '/work/nvda/bep-eng.dic'
OUT_FILE = 'nvdajp-eng-dic.csv'
DEFAULT_COST = 1600

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
	import re
	d = []
	k = {}
	for line in open(IN_FILE):
		if line[0] == '#': continue
		a1, a2 = line.rstrip().decode('UTF-8').split(' ')
		a1 = re.sub("'", "\\'", a1)
		a1 = a1.lower()
		if not k.has_key(a1):
			d.append([a1, a2])
			k[a1] = True
	d2 = [
		['alt', 	u'オルト'],
		['acrobat', u'アクロバット'],
		['adobe', 	u'アドビー', "1/4", 1000],
		['about', 	u'アバウト'],
		['au', 		u'エーユー'],
		['blank', 	u'ブランク'],
		['biz', 	u'ビズ'],
		['bazaar', 	u'バザール'],
		['cam', 	u'キャム'],
		['ctrl', 	u'コントロール'],
		['console', u'コンソール'],
		['caps', 	u'キャプス'],
		['cygwin', 	u'シグウィン'],
		['delete', 	u'デリート'],
		['del', 	u'デリート'],
		['explorer', u'エクスプローラ'],
		['esc', 	u'エスケープ'],
		['enter', 	u'エンター'],
		['firefox', u'ファイアフォックス'],
		['for', 	u'フォー'],
		['google', 	u'グーグル'],
		['home', 	u'ホーム'],
		['hub', 	u'ハブ'],
		['href',	u'エイチレフ'],
		['internet', u'インターネット'],
		['insert', 	u'インサート'],
		['java', 	u'ジャバ'],
		['jaxa',    u'ジャクサ'],
		['konica', 	u'コニカ'],
		['micro', 	u'マイクロ'],
		['mozilla', u'モジラ'],
		['open', 	u'オープン'],
		['office', 	u'オフィス'],
		['python', 	u'パイソン'],
		['pro', 	u'プロ'],
		['radio', 	u'ラジオ', "1/3", 800],
		['shift', 	u'シフト'],
		['skype', 	u'スカイプ', "2/4"],
		['soft', 	u'ソフト'],
		['systems', u'システムズ'],
		['think', 	u'シンク'],
		['talk', 	u'トーク'],
		['tab', 	u'タブ'],
		['update', 	u'アップデート'],
		['version', u'バージョン'],
		['vantage', u'バンテージ'],
		['wave', 	u'ウェーブ'],
		['welcome', u'ウェルカム'],
		['windows', u'ウィンドウズ'],
	]
	#for i in d2:
	#	if not k.has_key(i[0]):
	#		d.append([i[0], i[1]])
	#		k[i[0]] = True
	for i in d2:
		d.append(i)
	d.sort()
	with open(OUT_FILE, "w") as file:
		for i in d:
			k = i[0]
			alpha_count = len(k)
			k1 = alpha2mb(k.lower())
			y = i[1]
			mora_count = len(y)
			pros = "1/%d" % mora_count
			cost = DEFAULT_COST
			if alpha_count <= 2: cost = cost * 5
			if len(i) >= 3: pros = i[2]
			if len(i) >= 4: cost = i[3]
			# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
			s = u"%s,-1,-1,%d,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
			file.write(s.encode('cp932'))

