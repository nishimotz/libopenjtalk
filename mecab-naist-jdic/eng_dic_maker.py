# eng_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2010-12-05 by Takuya Nishimoto

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
	for line in open('bep-eng.dic'):
		if line[0] == '#': continue
		a1, a2 = line.rstrip().decode('UTF-8').split(' ')
		a1 = re.sub("'", "\\'", a1)
		a1 = a1.lower()
		if not k.has_key(a1):
			d.append([a1, a2])
			k[a1] = True
	d2 = [
		['alt', u'オルト'],
		['acrobat', u'アクロバット'],
		['adobe', u'アドビ'],
		['about', u'アバウト'],
		['blank', u'ブランク'],
		['biz', u'ビズ'],
		['bazaar', u'バザール'],
		['cam', u'キャム'],
		['ctrl', u'コントロール'],
		['console', u'コンソール'],
		['caps', u'キャプス'],
		['cygwin', u'シグウィン'],
		['delete', u'デリート'],
		['del', u'デリート'],
		['explorer', u'エクスプローラ'],
		['esc', u'エスケープ'],
		['enter', u'エンター'],
		['firefox', u'ファイアフォックス'],
		['for', u'フォー'],
		['google', u'グーグル'],
		['home', u'ホーム'],
		['hub', u'ハブ'],
		['internet', u'インターネット'],
		['insert', u'インサート'],
		['java', u'ジャバ'],
		['konica', u'コニカ'],
		['micro', u'マイクロ'],
		['mozilla', u'モジラ'],
		['open', u'オープン'],
		['office', u'オフィス'],
		['python', u'パイソン'],
		['pro', u'プロ'],
		['shift', u'シフト'],
		['skype', u'スカイプ'],
		['soft', u'ソフト'],
		['systems', u'システムズ'],
		['think', u'シンク'],
		['talk', u'トーク'],
		['tab', u'タブ'],
		['update', u'アップデート'],
		['version', u'バージョン'],
		['vantage', u'バンテージ'],
		['wave', u'ウェーブ'],
		['welcome to', u'ウェルカムトゥー'],
		['welcome', u'ウェルカム'],
		['windows', u'ウィンドウズ'],
	]
	for i in d2:
		if not k.has_key(i[0]):
			d.append([i[0], i[1]])
			k[i[0]] = True
	d.sort()
	with open(r"_nvdajp-eng-dic.csv", "w") as file:
		for i in d:
			# ＡＬＴ,1345,1345,6913,名詞,一般,*,*,*,*,ＡＬＴ,オルト,オルト,0/3,C1
			k1 = alpha2mb(i[0].upper())
			k2 = alpha2mb(i[0].capitalize())
			k3 = alpha2mb(i[0].lower())
			y = i[1]
                        mora_count = len(y)
			s = u"%s,1345,1345,6913,名詞,一般,*,*,*,*,%s,%s,%s,0/%d,C1\n" % (k1,k1,y,y,mora_count)
			file.write(s.encode('euc_jp'))
			s = u"%s,1345,1345,6913,名詞,一般,*,*,*,*,%s,%s,%s,0/%d,C1\n" % (k2,k2,y,y,mora_count)
			file.write(s.encode('euc_jp'))
			s = u"%s,1345,1345,6913,名詞,一般,*,*,*,*,%s,%s,%s,0/%d,C1\n" % (k3,k3,y,y,mora_count)
			file.write(s.encode('euc_jp'))

