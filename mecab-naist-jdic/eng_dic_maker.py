# eng_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2010-12-05 by Takuya Nishimoto
# bep-eng.dic is available at:
# http://cpansearch.perl.org/src/MASH/Lingua-JA-Yomi-0.01/lib/Lingua/JA/bep-eng.dic

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
	d = [
		['alt', 	u'オルト'],
		['acrobat', u'アクロバット'],
		['adobe', 	u'アドビー', "1/4", 1000],
		['about', 	u'アバウト'],
		['ass', 	u'アス', "1/2", 10000],
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
		
		['anpi', 		u'アンピ',			"1/3", 1000],
		['asian',		u'アジアン',		"1/4", 1000],
		['asahi', 		u'アサヒ',			"1/3", 1000],
		['edu',			u'エデュー',		"1/3", 1000],
		['gamba', 		u'ガンバ', 			"1/3", 1000],
		['genpatsu',	u'ゲンパツ',		"1/4", 1000],
		['hinan', 		u'ヒナン', 			"1/3", 1000],
		['horijun',		u'ホリジュン',		"1/4", 1000],
		['inosenaoki',	u'イノセナオキ',	"1/7", 1000],
		['kahoku', 		u'カホク', 			"1/3", 1000],
		['kurogen',		u'クロゲン',		"1/4", 1000],
		['medic', 		u'メディック',		"1/4", 1000],
		['miz',			u'ミズ',			"2/2", 1000],
		['minpo', 		u'ミンポー',		"1/4", 1000],
		['seikatsu',	u'セーカツ',		"1/4", 1000],
		['sagas',		u'サガス',			"1/3", 1000],
		['shimpo', 		u'シンポー', 		"1/4", 1000],
		['shimbun', 	u'シンブン',			"1/4", 1000],
		['teiden', 		u'テーデン',		"1/4", 1000],
		['tokuho',		u'トクホー',		"1/4", 1000],
		['takeyama', 	u'タケヤマ',		"1/4", 1000],
		['pref', 		u'プリフ',			"1/3", 1000],
		['wikipedia', 	u'ウイキペディーア',	"0/8", 1000],
		['tepco', 		u'テプコ',			"1/3", 1000],
		['akb', 		u'エーケービー',		"1/6", 1000],
		['npo', 		u'エヌピーオー',		"2/6", 1000],
		['takeshi',		u'タケシ',	"1/3", 1000],

		['nvda', 		u'エヌブイディーエー', 					"1/8", 1000],
		['jp', 			u'ジェーピー', 			"1/4", 1000],
		['co', 			u'シーオー', 			"1/4", 1000],
		['usb', 		u'ユーエスビー',		"1/6", 1000],
		['faq', 		u'エフエーキュー',		"1/6", 1000],
		['iaea', 		u'アイエーイーエー',		"7/8", 1000],
		['sjis', 		u'エスジス', 			"0/4", 1000],
		['jis', 		u'ジス', 			"1/2", 1000],
		['euc', 		u'イーユーシー', 	"1/6", 1000],
		['au', 			u'エーユー', 		"1/4", 600],
		['audio', 		u'オーディオ', 		"1/4", 610],
		['suite', 		u'スイート', 		"2/4", 1000],
		
		['opensource', 	u'オープンソース', None, 1000],
		['notepad', 	u'ノートパッド', None, 1000],
		['guidebook', 	u'ガイドブック', None, 1000],
		['blog', 		u'ブログ', None, 1000],
		['matlab', 		u'マトラブ', None, 1000],
		['keyboard', 	u'キーボード', None, 1000],
		['plugins', 	u'プラグインズ', None, 1000],
		['facebook', 	u'フェイスブック', None, 1000],
		['desktop', 	u'デスクトップ', None, 1000],
		['output', 		u'アウトプット', None, 1000],
		['nullsoft', 	u'ヌルソフト', None, 1000],
		['cygdrive', 	u'シグドライブ', None, 1000],
		['ustream', 	u'ユーストリーム', None, 1000],
		['ubuntu', 		u'ウブンツー', None, 1000],
		['ware', 		u'ウェアー', None, 1000],
		['id', 			u'アイディー', None, 1000],
		['it', 			u'アイティー', None, 1000],
		['time', 		u'タイム', None, 1000],
		['home', 		u'ホーム', None, 1000],

		['hokkaido', 	u'ホッカイドー', None, 1000],
		['yamagata', 	u'ヤマガタ', None, 1000],
		['akita', 		u'アキタ', None, 1000],
		['aomori', 		u'アオモリ', None, 1000],
		['iwate', 		u'イワテ', None, 1000],
		['tsukuba', 	u'ツクバ', None, 1000],
		['oshu', 		u'オーシュー', None, 1000],
		['hachinohe', 	u'ハチノヘ', None, 1000],
		['kesennuma', 	u'ケセンヌマ', None, 1000],
		['kantei', 		u'カンテー', None, 1000],
		['saigai', 		u'サイガイ', None, 1000],
		['tochigi', 	u'トチギ', None, 1000],
		['kashima', 	u'カシマ', None, 1000],
		['morioka', 	u'モリオカ', 		"2/4", 1000],
		['miyagi', 		u'ミヤギ',			"1/3", 1000],
		['fukushima', 	u'フクシマ', 		"2/4", 1000],
		['niigata', 	u'ニーガタ', 		"0/4", 1000],
		['yahoo', 		u'ヤフー',			"2/3", 1000],
		['japan', 		u'ジャパン',		"2/3", 1000],
		['asshuku',		u'アッシュク',		"0/4"],
		['mei',			u'メイ',			"1/2", 100],
	]
	k = {}
	for i in d:
		k[i[0]] = True
	for line in open(IN_FILE):
		if line[0] == '#': continue
		a1, a2 = line.rstrip().decode('UTF-8').split(' ')
		a1 = re.sub("'", "\\'", a1)
		a1 = a1.lower()
		if not k.has_key(a1):
			d.append([a1, a2])
			k[a1] = True
	d.sort()
	with open(OUT_FILE, "w") as file:
		for i in d:
			k = i[0]
			alpha_count = len(k)
			k1 = alpha2mb(k.lower())
			y = i[1]
			# default pros
			mora_count = len(y)
			pros = "1/%d" % mora_count
			# default cost
			cost = DEFAULT_COST
			if alpha_count <= 2: cost = cost * 5
			# override by entry
			if len(i) >= 3:
				if i[2] != None: pros = i[2]
			if len(i) >= 4: cost = i[3]
			# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
			s = u"%s,-1,-1,%d,名詞,一般,*,*,*,*,%s,%s,%s,%s,C0\n" % (k1,cost,k1,y,y,pros)
			file.write(s.encode('cp932'))

