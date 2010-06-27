/* ----------------------------------------------------------------- */
/*           The HMM-Based Speech Synthesis System (HTS)             */
/*           Open JTalk developed by HTS Working Group               */
/*           http://open-jtalk.sourceforge.net/                      */
/* ----------------------------------------------------------------- */
/*                                                                   */
/*  Copyright (c) 2008-2010  Nagoya Institute of Technology          */
/*                           Department of Computer Science          */
/*                                                                   */
/* All rights reserved.                                              */
/*                                                                   */
/* Redistribution and use in source and binary forms, with or        */
/* without modification, are permitted provided that the following   */
/* conditions are met:                                               */
/*                                                                   */
/* - Redistributions of source code must retain the above copyright  */
/*   notice, this list of conditions and the following disclaimer.   */
/* - Redistributions in binary form must reproduce the above         */
/*   copyright notice, this list of conditions and the following     */
/*   disclaimer in the documentation and/or other materials provided */
/*   with the distribution.                                          */
/* - Neither the name of the HTS working group nor the names of its  */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission.   */
/*                                                                   */
/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND            */
/* CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,       */
/* INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF          */
/* MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          */
/* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS */
/* BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,          */
/* EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED   */
/* TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,     */
/* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON */
/* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   */
/* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY    */
/* OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           */
/* POSSIBILITY OF SUCH DAMAGE.                                       */
/* ----------------------------------------------------------------- */

/*
  無声子音: k ky s sh t ty ch ts h f hy p py
  Rule 1 助動詞の「です」と「ます」の「す」が無声化
  Rule 2 続けて無声化しない
  Rule 3 アクセント核で無声化しない
  Rule 4 無声子音(k ky s sh t ty ch ts h f hy p py)に囲まれた「i」と「u」が無声化
*/

#define NJD_SET_UNVOICED_VOWEL_QUOTATION "’"
#define NJD_SET_UNVOICED_VOWEL_QUESTION "？"
#define NJD_SET_UNVOICED_VOWEL_TOUTEN "、"

#define NJD_SET_UNVOICED_VOWEL_JODOUSHI "助動詞"

static const char *njd_set_unvoiced_vowel_jodoushi_table[] = {
   "デス", "デス’", "2",
   "マス", "マス’", "2",
   NULL, NULL
};

static const char *njd_set_unvoiced_vowel_candidate_list[] = {
   "キュ",                      /* ky u */
   "シュ",                      /* sh u */
   "スィ",                      /* s i */
   "チュ",                      /* ch u */
   "ツィ",                      /* ts i */
   "ヒュ",                      /* hy u */
   "フィ",                      /* f i */
   "ピュ",                      /* py u */
   "テュ",                      /* ty u */
   "トゥ",                      /* t u */
   "ティ",                      /* t i */
   "キ",                        /* k i */
   "ク",                        /* k u */
   "シ",                        /* sh i */
   "ス",                        /* s u */
   "チ",                        /* ch i */
   "ツ",                        /* ts u */
   "ヒ",                        /* h i */
   "フ",                        /* f u */
   "ピ",                        /* p i */
   "プ",                        /* p u */
   NULL
};

static const char *njd_set_unvoiced_vowel_next_mora_list[] = {
   "カ",                        /* k ky */
   "キ",
   "ク",
   "ケ",
   "コ",
   "サ",                        /* s sh */
   "シ",
   "ス",
   "セ",
   "ソ",
   "タ",                        /* t ty ch ts */
   "チ",
   "ツ",
   "テ",
   "ト",
   "ハ",                        /* h f hy */
   "ヒ",
   "フ",
   "ヘ",
   "ホ",
   "パ",                        /* p py */
   "ピ",
   "プ",
   "ペ",
   "ポ",
   NULL
};

static const char *njd_set_unvoiced_vowel_mora_list[] = {
   "ヴョ",
   "ヴュ",
   "ヴャ",
   "ヴォ",
   "ヴェ",
   "ヴィ",
   "ヴァ",
   "ヴ",
   "ン",
   "ヲ",
   "ヱ",
   "ヰ",
   "ワ",
   "ロ",
   "レ",
   "ル",
   "リョ",
   "リュ",
   "リャ",
   "リェ",
   "リ",
   "ラ",
   "ヨ",
   "ョ",
   "ユ",
   "ュ",
   "ヤ",
   "ャ",
   "モ",
   "メ",
   "ム",
   "ミョ",
   "ミュ",
   "ミャ",
   "ミェ",
   "ミ",
   "マ",
   "ポ",
   "ボ",
   "ホ",
   "ペ",
   "ベ",
   "ヘ",
   "プ",
   "ブ",
   "フォ",
   "フェ",
   "フィ",
   "ファ",
   "フ",
   "ピョ",
   "ピュ",
   "ピャ",
   "ピェ",
   "ピ",
   "ビョ",
   "ビュ",
   "ビャ",
   "ビェ",
   "ビ",
   "ヒョ",
   "ヒュ",
   "ヒャ",
   "ヒェ",
   "ヒ",
   "パ",
   "バ",
   "ハ",
   "ノ",
   "ネ",
   "ヌ",
   "ニョ",
   "ニュ",
   "ニャ",
   "ニェ",
   "ニ",
   "ナ",
   "ドゥ",
   "ド",
   "トゥ",
   "ト",
   "デョ",
   "デュ",
   "デャ",
   "デェ",
   "ディ",
   "デ",
   "テョ",
   "テュ",
   "テャ",
   "ティ",
   "テ",
   "ヅ",
   "ツォ",
   "ツェ",
   "ツィ",
   "ツァ",
   "ツ",
   "ッ",
   "ヂ",
   "チョ",
   "チュ",
   "チャ",
   "チェ",
   "チ",
   "ダ",
   "タ",
   "ゾ",
   "ソ",
   "ゼ",
   "セ",
   "ズィ",
   "ズ",
   "スィ",
   "ス",
   "ジョ",
   "ジュ",
   "ジャ",
   "ジェ",
   "ジ",
   "ショ",
   "シュ",
   "シャ",
   "シェ",
   "シ",
   "ザ",
   "サ",
   "ゴ",
   "コ",
   "ゲ",
   "ケ",
   "グ",
   "ク",
   "ギョ",
   "ギュ",
   "ギャ",
   "ギェ",
   "ギ",
   "キョ",
   "キュ",
   "キャ",
   "キェ",
   "キ",
   "ガ",
   "カ",
   "オ",
   "ォ",
   "エ",
   "ェ",
   "ウォ",
   "ウェ",
   "ウィ",
   "ウ",
   "ゥ",
   "イェ",
   "イ",
   "ィ",
   "ア",
   "ァ",
   "ー",
   NULL
};
