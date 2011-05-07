//  MeCab -- Yet Another Part-of-Speech and Morphological Analyzer
//
//  Copyright(C) 2001-2006 Taku Kudo <taku@chasen.org>
//  Copyright(C) 2004-2006 Nippon Telegraph and Telephone Corporation

/* ----------------------------------------------------------------- */
/*           The Japanese TTS System "Open JTalk"                    */
/*           developed by HTS Working Group                          */
/*           http://open-jtalk.sourceforge.net/                      */
/* ----------------------------------------------------------------- */
/*                                                                   */
/*  Copyright (c) 2008-2011  Nagoya Institute of Technology          */
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

#include <iostream>
#include <map>
#include <vector>
#include <string>
#include "mecab.h"
#include "dictionary_rewriter.h"
#include "char_property.h"
#include "param.h"
#include "connector.h"
#include "dictionary.h"

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

namespace MeCab {

class DictionaryComplier {
 public:
  static int run(int argc, char **argv) {
    static const MeCab::Option long_options[] = {
      { "dicdir",   'd',   ".",   "DIR", "set DIR as dicdi (default \".\")" },
      { "outdir",   'o',   ".",   "DIR",
        "set DIR as output dir (default \".\")" },
      { "unknown",  'U',   0,   0,   "build parameters for unknown words" },
      { "userdic",  'u',   0,   "FILE",   "build user dictionary" },
      { "charcategory", 'C', 0, 0,   "build character category maps" },
      { "matrix",    'm',  0,   0,   "build connection matrix" },
      { "charset",   'c',  MECAB_DEFAULT_CHARSET, "ENC",
        "make charset of binary dictionary ENC (default "
        MECAB_DEFAULT_CHARSET ")"  },
      { "charset",   't',  MECAB_DEFAULT_CHARSET, "ENC", "alias of -c"  },
      { "dictionary-charset",  'f',  MECAB_DEFAULT_CHARSET,
        "ENC", "assume charset of input CSVs as ENC (default "
        MECAB_DEFAULT_CHARSET ")"  },
      { "wakati",    'w',  0,   0,   "build wakati-gaki only dictionary", },
      { "posid",     'p',  0,   0,   "assign Part-of-speech id" },
      { "node-format", 'F', 0,  "STR",
        "use STR as the user defined node format" },
      { "version",   'v',  0,   0,   "show the version and exit."  },
      { "help",      'h',  0,   0,   "show this help and exit."  },
      { 0, 0, 0, 0 }
    };

    Param param;

    if (!param.open(argc, argv, long_options)) {
      std::cout << param.what() << "\n\n" <<  COPYRIGHT
                << "\ntry '--help' for more information." << std::endl;
      return -1;
    }

    if (!param.help_version()) return 0;

    const std::string dicdir = param.get<std::string>("dicdir");
    const std::string outdir = param.get<std::string>("outdir");
    bool opt_unknown = param.get<bool>("unknown");
    bool opt_matrix = param.get<bool>("matrix");
    bool opt_charcategory = param.get<bool>("charcategory");
    bool opt_sysdic = param.get<bool>("sysdic");
    const std::string userdic = param.get<std::string>("userdic");

#define DCONF(file) create_filename(dicdir, std::string(file)).c_str()
#define OCONF(file) create_filename(outdir, std::string(file)).c_str()

    /* for Open JTalk
    CHECK_DIE(param.load(DCONF(DICRC)))
        << "no such file or directory: " << DCONF(DICRC);
    */

    std::vector<std::string> dic;
    if (userdic.empty())
      enum_csv_dictionaries(dicdir.c_str(), &dic);
    else
      dic = param.rest_args();

    if (!userdic.empty()) {
      CHECK_DIE(dic.size()) << "no dictionaries are specified";

      param.set("type", MECAB_USR_DIC);
      Dictionary::compile(param, dic,
                          DCONF(MATRIX_DEF_FILE),
                          DCONF(MATRIX_FILE),
                          DCONF(LEFT_ID_FILE),
                          DCONF(RIGHT_ID_FILE),
                          DCONF(REWRITE_FILE),
                          DCONF(POS_ID_FILE),
                          userdic.c_str());
    } else {
      if (!opt_unknown && !opt_matrix && !opt_charcategory && !opt_sysdic) {
        opt_unknown = opt_matrix = opt_charcategory = opt_sysdic = true;
      }

      if (opt_charcategory || opt_unknown) {
        CharProperty::compile(DCONF(CHAR_PROPERTY_DEF_FILE),
                              DCONF(UNK_DEF_FILE),
                              OCONF(CHAR_PROPERTY_FILE));
      }

      if (opt_unknown) {
        std::vector<std::string> tmp;
        tmp.push_back(DCONF(UNK_DEF_FILE));
        param.set("type", MECAB_UNK_DIC);
        Dictionary::compile(param, tmp,
                            DCONF(MATRIX_DEF_FILE),
                            DCONF(MATRIX_FILE),
                            DCONF(LEFT_ID_FILE),
                            DCONF(RIGHT_ID_FILE),
                            DCONF(REWRITE_FILE),
                            DCONF(POS_ID_FILE),
                            OCONF(UNK_DIC_FILE));
      }

      if (opt_sysdic) {
        CHECK_DIE(dic.size()) << "no dictionaries are specified";
        param.set("type", MECAB_SYS_DIC);
        Dictionary::compile(param, dic,
                            DCONF(MATRIX_DEF_FILE),
                            DCONF(MATRIX_FILE),
                            DCONF(LEFT_ID_FILE),
                            DCONF(RIGHT_ID_FILE),
                            DCONF(REWRITE_FILE),
                            DCONF(POS_ID_FILE),
                            OCONF(SYS_DIC_FILE));
      }

      if (opt_matrix) {
        Connector::compile(DCONF(MATRIX_DEF_FILE),
                           OCONF(MATRIX_FILE));
      }
    }

    std::cout << "\ndone!\n";

    return 0;
  }
};

#undef DCONF
#undef OCONF
}

int mecab_dict_index(int argc, char **argv) {
  return MeCab::DictionaryComplier::run(argc, argv);
}
