// MeCab -- Yet Another Part-of-Speech and Morphological Analyzer
//
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
#include <fstream>
#include <cstring>

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#ifdef HAVE_SYS_TYPES_H
#include <sys/types.h>
#endif

#ifdef HAVE_DIRENT_H
#include <dirent.h>
#endif

#ifdef HAVE_WINDOWS_H
#include <windows.h>
#endif

/* for Open JTalk
#if defined(_WIN32) && !defined(__CYGWIN__)
extern HINSTANCE DllInstance;
#endif
*/

#include "mecab.h"
#include "common.h"
#include "utils.h"
#include "param.h"

using namespace std;

namespace MeCab {

int decode_charset(const char *charset) {
  std::string tmp = charset;
  toLower(&tmp);
  if (tmp == "sjis"  || tmp == "shift-jis" ||
      tmp == "shift_jis" || tmp == "cp932")
    return CP932;
  else if (tmp == "euc"   || tmp == "euc_jp" ||
           tmp == "euc-jp")
    return EUC_JP;
  else if (tmp == "utf8" || tmp == "utf_8" ||
           tmp == "utf-8")
    return UTF8;
  else if (tmp == "utf16" || tmp == "utf_16" ||
           tmp == "utf-16")
    return UTF16;
  else if (tmp == "utf16be" || tmp == "utf_16be" ||
           tmp == "utf-16be")
    return UTF16BE;
  else if (tmp == "utf16le" || tmp == "utf_16le" ||
           tmp == "utf-16le")
    return UTF16LE;
  else if (tmp == "ascii")
    return ASCII;

  return UTF8;  // default is UTF8
}

std::string create_filename(const std::string &path,
                            const std::string &file) {
  std::string s = path;
#if defined(_WIN32) && !defined(__CYGWIN__)
  if (s.size() && s[s.size()-1] != '\\') s += '\\';
#else
  if (s.size() && s[s.size()-1] != '/') s += '/';
#endif
  s += file;
  return s;
}

void remove_filename(std::string *s) {
  int len = static_cast<int>(s->size()) - 1;
  bool ok = false;
  for (; len >= 0; --len) {
#if defined(_WIN32) && !defined(__CYGWIN__)
    if ((*s)[len] == '\\') {
      ok = true;
      break;
    }
#else
    if ((*s)[len] == '/')  {
      ok = true;
      break;
    }
#endif
  }
  if (ok)
    *s = s->substr(0, len);
  else
    *s = ".";
}

void remove_pathname(std::string *s) {
  int len = static_cast<int>(s->size()) - 1;
  bool ok = false;
  for (; len >= 0; --len) {
#if defined(_WIN32) && !defined(__CYGWIN__)
    if ((*s)[len] == '\\') {
      ok = true;
      break;
    }
#else
    if ((*s)[len] == '/')  {
      ok = true;
      break;
    }
#endif
  }
  if (ok)
    *s = s->substr(len + 1, s->size() - len);
  else
    *s = ".";
}

void replace_string(std::string *s,
                    const std::string &src,
                    const std::string &dst) {
  size_t pos = s->find(src);
  if (pos != std::string::npos)
    s->replace(pos, src.size(), dst);
}

void enum_csv_dictionaries(const char *path,
                           std::vector<std::string> *dics) {
  dics->clear();

#if defined(_WIN32) && !defined(__CYGWIN__)
  WIN32_FIND_DATA wfd;
  HANDLE hFind;
  const std::string pat = create_filename(path, "*.csv");
  hFind = FindFirstFile(pat.c_str(), &wfd);
  CHECK_DIE(hFind != INVALID_HANDLE_VALUE)
      << "Invalid File Handle. Get Last Error reports";
  do {
    std::string tmp = create_filename(path, wfd.cFileName);
    dics->push_back(tmp);
  } while (FindNextFile(hFind, &wfd));
  FindClose(hFind);
#else
  DIR *dir = opendir(path);
  CHECK_DIE(dir) << "no such directory: " << path;

  for (struct dirent *dp = readdir(dir);
       dp;
       dp = readdir(dir)) {
    const std::string tmp = dp->d_name;
    if (tmp.size() >= 5) {
      std::string ext = tmp.substr(tmp.size() - 4, 4);
      toLower(&ext);
      if (ext == ".csv")
        dics->push_back(create_filename(path, tmp));
    }
  }
  closedir(dir);
#endif
}

bool toLower(std::string *s) {
  for (size_t i = 0; i < s->size(); ++i) {
    char c = (*s)[i];
    if ((c >= 'A') && (c <= 'Z')) {
      c += 'a' - 'A';
      (*s)[i] = c;
    }
  }
  return true;
}

bool escape_csv_element(std::string *w) {
  if (w->find(',') != std::string::npos ||
      w->find('"') != std::string::npos) {
    std::string tmp = "\"";
    for (size_t j = 0; j < w->size(); j++) {
      if ((*w)[j] == '"') tmp += '"';
      tmp += (*w)[j];
    }
    tmp += '"';
    *w = tmp;
  }
  return true;
}

int progress_bar(const char* message, size_t current, size_t total) {
  static char bar[] = "###########################################";
  static int scale = sizeof(bar) - 1;
  static int prev = 0;

  int cur_percentage  = static_cast<int>(100.0 * current/total);
  int bar_len = static_cast<int>(1.0 * current*scale/total);

  if (prev != cur_percentage) {
    printf("%s: %3d%% |%.*s%*s| ", message, cur_percentage,
           bar_len, bar, scale - bar_len, "");
    if (cur_percentage == 100)
      printf("\n");
    else
      printf("\r");
    fflush(stdout);
  }

  prev = cur_percentage;

  return 1;
}

bool load_dictionary_resource(Param *param) {
  std::string rcfile = param->get<std::string>("rcfile");

#ifdef HAVE_GETENV
  if (rcfile.empty()) {
    const char *homedir = getenv("HOME");
    if (homedir) {
      std::string s = MeCab::create_filename(std::string(homedir),
                                             ".mecabrc");
      std::ifstream ifs(s.c_str());
      if (ifs) rcfile = s;
    }
  }

  if (rcfile.empty()) {
    const char *rcenv = getenv("MECABRC");
    if (rcenv) rcfile = rcenv;
  }
#endif

#if defined (HAVE_GETENV) && defined(_WIN32) && !defined(__CYGWIN__)
  if (rcfile.empty()) {
    char buf[BUF_SIZE];
    DWORD len = GetEnvironmentVariable("MECABRC",
                                       buf,
                                       sizeof(buf));
    if (len < sizeof(buf) && len > 0) {
      rcfile = buf;
    }
  }
#endif

#if defined(_WIN32) && !defined(__CYGWIN__)
  HKEY hKey;
  char v[BUF_SIZE];
  DWORD vt;
  DWORD size = sizeof(v);

  if (rcfile.empty()) {
    RegOpenKeyEx(HKEY_LOCAL_MACHINE, "software\\mecab", 0, KEY_READ, &hKey);
    RegQueryValueEx(hKey, "mecabrc", 0, &vt,
                    reinterpret_cast<BYTE *>(v), &size);
    RegCloseKey(hKey);
    if (vt == REG_SZ) rcfile = v;
  }

  if (rcfile.empty()) {
    RegOpenKeyEx(HKEY_CURRENT_USER, "software\\mecab", 0, KEY_READ, &hKey);
    RegQueryValueEx(hKey, "mecabrc", 0, &vt,
                    reinterpret_cast<BYTE *>(v), &size);
    RegCloseKey(hKey);
    if (vt == REG_SZ) rcfile = v;
  }

  /* for Open JTalk
  if (rcfile.empty()) {
    vt = GetModuleFileName(DllInstance, v, size);
    if (vt != 0) {
      char drive[_MAX_DRIVE];
      char dir[_MAX_DIR];
      _splitpath(v, drive, dir, NULL, NULL);
      std::string s = std::string(drive)
          + std::string(dir) + std::string("mecabrc");
      std::ifstream ifs(s.c_str());
      if (ifs) rcfile = s;
    }
  }
  */
#endif

  /* for Open JTalk
  if (rcfile.empty()) rcfile = MECAB_DEFAULT_RC;

  if (!param->load(rcfile.c_str())) return false;
  */

  std::string dicdir = param->get<std::string>("dicdir");
  if (dicdir.empty()) dicdir = ".";  // current
  remove_filename(&rcfile);
  replace_string(&dicdir, "$(rcpath)", rcfile);
  param->set<std::string>("dicdir", dicdir, true);
  dicdir = create_filename(dicdir, DICRC);

  if (!param->load(dicdir.c_str())) return false;

  return true;
}
}
