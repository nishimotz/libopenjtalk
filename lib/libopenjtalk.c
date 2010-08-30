/* libopenjtalk.c    
 * based on ../bin/open_jtalk.c
 * by Takuya Nishimoto
 * since 2010-06-27    
 */

#define VOICE "../../../share/open_jtalk/hts_voice_nitech_jp_atr503_m001-1.01"
#define DIC   "../../../share/open_jtalk/open_jtalk_dic_utf_8-1.00"

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

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>

#define USE_MECAB 0

/* Main headers */
#if USE_MECAB
#include "mecab.h"
#endif
#include "njd.h"
#include "jpcommon.h"
#include "HTS_engine.h"

/* Sub headers */
#include "text2mecab.h"
#include "mecab2njd.h"
#include "njd_set_pronunciation.h"
#include "njd_set_digit.h"
#include "njd_set_accent_phrase.h"
#include "njd_set_accent_type.h"
#include "njd_set_unvoiced_vowel.h"
#include "njd_set_long_vowel.h"
#include "njd2jpcommon.h"

#define MAXBUFLEN 1024

typedef struct _OpenJTalk {
#if USE_MECAB
    Mecab mecab;
#endif
   NJD njd;
   JPCommon jpcommon;
   HTS_Engine engine;
} OpenJTalk;

void OpenJTalk_initialize(OpenJTalk * open_jtalk, int sampling_rate, int fperiod, double alpha,
                          int stage, double beta, int audio_buff_size, double uv_threshold,
                          HTS_Boolean use_log_gain, double gv_weight_mcp, double gv_weight_lf0)
{
#if USE_MECAB
    Mecab_initialize(&open_jtalk->mecab);
#endif
    NJD_initialize(&open_jtalk->njd);
   JPCommon_initialize(&open_jtalk->jpcommon);
   HTS_Engine_initialize(&open_jtalk->engine, 2);
   HTS_Engine_set_sampling_rate(&open_jtalk->engine, sampling_rate);
   HTS_Engine_set_fperiod(&open_jtalk->engine, fperiod);
   HTS_Engine_set_alpha(&open_jtalk->engine, alpha);
   HTS_Engine_set_gamma(&open_jtalk->engine, stage);
   HTS_Engine_set_log_gain(&open_jtalk->engine, use_log_gain);
   HTS_Engine_set_beta(&open_jtalk->engine, beta);
   HTS_Engine_set_audio_buff_size(&open_jtalk->engine, audio_buff_size);
   HTS_Engine_set_msd_threshold(&open_jtalk->engine, 1, uv_threshold);
   HTS_Engine_set_gv_weight(&open_jtalk->engine, 0, gv_weight_mcp);
   HTS_Engine_set_gv_weight(&open_jtalk->engine, 1, gv_weight_lf0);
}

void OpenJTalk_load(OpenJTalk * open_jtalk, char *dn_mecab, char *fn_ms_dur, char *fn_ts_dur,
                    char *fn_ms_mcp, char *fn_ts_mcp, char **fn_ws_mcp, int num_ws_mcp,
                    char *fn_ms_lf0, char *fn_ts_lf0, char **fn_ws_lf0, int num_ws_lf0,
                    char *fn_ms_gvm, char *fn_ts_gvm, char *fn_ms_gvl, char *fn_ts_gvl,
                    char *fn_gv_switch)
{
#if USE_MECAB
    Mecab_load(&open_jtalk->mecab, dn_mecab);
#endif
    HTS_Engine_load_duration_from_fn(&open_jtalk->engine, &fn_ms_dur, &fn_ts_dur, 1);
   HTS_Engine_load_parameter_from_fn(&open_jtalk->engine, &fn_ms_mcp, &fn_ts_mcp,
                                     fn_ws_mcp, 0, FALSE, num_ws_mcp, 1);
   HTS_Engine_load_parameter_from_fn(&open_jtalk->engine, &fn_ms_lf0, &fn_ts_lf0,
                                     fn_ws_lf0, 1, TRUE, num_ws_lf0, 1);
   if (fn_ms_gvm != NULL) {
      if (fn_ts_gvm != NULL)
         HTS_Engine_load_gv_from_fn(&open_jtalk->engine, &fn_ms_gvm, &fn_ts_gvm, 0, 1);
      else
         HTS_Engine_load_gv_from_fn(&open_jtalk->engine, &fn_ms_gvm, NULL, 0, 1);
   }
   if (fn_ms_gvl != NULL) {
      if (fn_ts_gvl != NULL)
         HTS_Engine_load_gv_from_fn(&open_jtalk->engine, &fn_ms_gvl, &fn_ts_gvl, 1, 1);
      else
         HTS_Engine_load_gv_from_fn(&open_jtalk->engine, &fn_ms_gvl, NULL, 1, 1);
   }
   if (fn_gv_switch != NULL)
      HTS_Engine_load_gv_switch_from_fn(&open_jtalk->engine, fn_gv_switch);
}

void OpenJTalk_synthesis(OpenJTalk * open_jtalk, char *txt, FILE * wavfp, FILE * logfp)
{
   char *buff = (char *) calloc(2 * strlen(txt) + 1, sizeof(char));

   text2mecab(buff, txt);
#if USE_MECAB
   Mecab_analysis(&open_jtalk->mecab, buff);
#endif
   free(buff);
#if USE_MECAB
   mecab2njd(&open_jtalk->njd, Mecab_get_feature(&open_jtalk->mecab),
             Mecab_get_size(&open_jtalk->mecab));
#else
   mecab2njd(&open_jtalk->njd, (char **)NULL, 0);
#endif
   njd_set_pronunciation(&open_jtalk->njd);
   njd_set_digit(&open_jtalk->njd);
   njd_set_accent_phrase(&open_jtalk->njd);
   njd_set_accent_type(&open_jtalk->njd);
   njd_set_unvoiced_vowel(&open_jtalk->njd);
   njd_set_long_vowel(&open_jtalk->njd);
   njd2jpcommon(&open_jtalk->jpcommon, &open_jtalk->njd);
   JPCommon_make_label(&open_jtalk->jpcommon);
   if (JPCommon_get_label_size(&open_jtalk->jpcommon) > 2) {
      HTS_Engine_load_label_from_string_list(&open_jtalk->engine,
                                             JPCommon_get_label_feature(&open_jtalk->jpcommon),
                                             JPCommon_get_label_size(&open_jtalk->jpcommon));
      HTS_Engine_create_sstream(&open_jtalk->engine);
      HTS_Engine_create_pstream(&open_jtalk->engine);
      HTS_Engine_create_gstream(&open_jtalk->engine);
#if 0
      if (wavfp != NULL)
         HTS_Engine_save_riff(&open_jtalk->engine, wavfp);
#else
      /* based on HTS_engine_API:
       * HTS_Engine_save_generated_speech: output generated speech */
      {
        HTS_Engine *engine = &open_jtalk->engine;
        int i;
        short temp;
        HTS_GStreamSet *gss = &engine->gss;
        for (i = 0; i < HTS_GStreamSet_get_total_nsample(gss); i++) {
          temp = HTS_GStreamSet_get_speech(gss, i);
          fwrite(&temp, sizeof(short), 1, wavfp);
        }
      }
#endif
#if 0
      if (logfp != NULL) {
         fprintf(logfp, "[Text analysis result]\n");
         NJD_fprint(&open_jtalk->njd, logfp);
         fprintf(logfp, "\n[Output label]\n");
         HTS_Engine_save_label(&open_jtalk->engine, logfp);
         fprintf(logfp, "\n");
         HTS_Engine_save_information(&open_jtalk->engine, logfp);
      }
#endif
      HTS_Engine_refresh(&open_jtalk->engine);
   }
   JPCommon_refresh(&open_jtalk->jpcommon);
   NJD_refresh(&open_jtalk->njd);
#if USE_MECAB
    Mecab_refresh(&open_jtalk->mecab);
#endif
}

void OpenJTalk_clear(OpenJTalk * open_jtalk)
{
#if USE_MECAB
    Mecab_clear(&open_jtalk->mecab);
#endif
   NJD_clear(&open_jtalk->njd);
   JPCommon_clear(&open_jtalk->jpcommon);
   HTS_Engine_clear(&open_jtalk->engine);
}

void Usage()
{
   fprintf(stderr, "\n");
   fprintf(stderr, "The HMM-based speech synthesis system (HTS)\n");
   fprintf(stderr, "Open JTalk version 1.01 (http://open-jtalk.sourceforge.net/)\n");
   fprintf(stderr, "Copyright (C) 2008-2010  Nagoya Institute of Technology\n");
   fprintf(stderr, "All rights reserved.\n");
   HTS_show_copyright(stderr);
   fprintf(stderr, "\n");
   fprintf(stderr, "Yet Another Part-of-Speech and Morphological Analyzer (Mecab)\n");
   fprintf(stderr, "mecab version 0.98 (http://mecab.sourceforge.net/)\n");
   fprintf(stderr, "Copyright (C) 2001-2008  Taku Kudo\n");
   fprintf(stderr, "              2004-2008  Nippon Telegraph and Telephone Corporation\n");
   fprintf(stderr, "All rights reserved.\n");
   fprintf(stderr, "\n");
   fprintf(stderr, "NAIST Japanese dictionary\n");
   fprintf(stderr, "mecab-naist-jdic version 0.6.1-20090630 (http://naist-jdic.sourceforge.jp/)\n");
   fprintf(stderr, "Copyright (C) 2009  Nara Institute of Science and Technology\n");
   fprintf(stderr, "All rights reserved.\n");
   fprintf(stderr, "\n");
   fprintf(stderr, "open_jtalk - An HMM-based text to speech system\n");
   fprintf(stderr, "\n");
   fprintf(stderr, "  usage:\n");
   fprintf(stderr, "       open_jtalk [ options ] [ infile ] \n");
   fprintf(stderr,
           "  options:                                                                   [  def][ min--max]\n");
   fprintf(stderr,
           "    -x dir         : dictionary directory                                    [  N/A]\n");
   fprintf(stderr,
           "    -td tree       : decision trees file for state duration                  [  N/A]\n");
   fprintf(stderr,
           "    -tf tree       : decision trees file for Log F0                          [  N/A]\n");
   fprintf(stderr,
           "    -tm tree       : decision trees file for spectrum                        [  N/A]\n");
   fprintf(stderr,
           "    -md pdf        : model file for state duration                           [  N/A]\n");
   fprintf(stderr,
           "    -mf pdf        : model file for Log F0                                   [  N/A]\n");
   fprintf(stderr,
           "    -mm pdf        : model file for spectrum                                 [  N/A]\n");
   fprintf(stderr,
           "    -df win        : window files for calculation delta of Log F0            [  N/A]\n");
   fprintf(stderr,
           "    -dm win        : window files for calculation delta of spectrum          [  N/A]\n");
   fprintf(stderr,
           "    -ow s          : filename of output wav audio (generated speech)         [  N/A]\n");
   fprintf(stderr,
           "    -ot s          : filename of output trace information                    [  N/A]\n");
   fprintf(stderr,
           "    -s  i          : sampling frequency                                      [16000][   1--48000]\n");
   fprintf(stderr,
           "    -p  i          : frame period (point)                                    [   80][   1--]\n");
   fprintf(stderr,
           "    -a  f          : all-pass constant                                       [ 0.42][ 0.0--1.0]\n");
   fprintf(stderr,
           "    -g  i          : gamma = -1 / i (if i=0 then gamma=0)                    [    0][   0-- ]\n");
   fprintf(stderr,
           "    -b  f          : postfiltering coefficient                               [  0.0][-0.8--0.8]\n");
   fprintf(stderr,
           "    -l             : regard input as log gain and output linear one (LSP)    [  N/A]\n");
   fprintf(stderr,
           "    -u  f          : voiced/unvoiced threshold                               [  0.5][ 0.0--1.0]\n");
   fprintf(stderr,
           "    -ef tree       : decision tree file for GV of Log F0                     [  N/A]\n");
   fprintf(stderr,
           "    -em tree       : decision tree file for GV of spectrum                   [  N/A]\n");
   fprintf(stderr,
           "    -cf pdf        : filename of GV for Log F0                               [  N/A]\n");
   fprintf(stderr,
           "    -cm pdf        : filename of GV for spectrum                             [  N/A]\n");
   fprintf(stderr,
           "    -jf f          : weight of GV for Log F0                                 [  0.7][ 0.0--2.0]\n");
   fprintf(stderr,
           "    -jm f          : weight of GV for spectrum                               [  1.0][ 0.0--2.0]\n");
   fprintf(stderr,
           "    -k  tree       : use GV switch                                           [  N/A]\n");
   fprintf(stderr,
           "    -z  i          : audio buffer size                                       [ 1600][   0--48000]\n");
   fprintf(stderr, "  infile:\n");
   fprintf(stderr,
           "    text file                                                                [stdin]\n");
   fprintf(stderr, "  note:\n");
   fprintf(stderr, "    option '-d' may be repeated to use multiple delta parameters.\n");
   fprintf(stderr, "    generated spectrum and log F0 sequences are saved in natural\n");
   fprintf(stderr, "    endian, binary (float) format.\n");
   fprintf(stderr, "\n");

   exit(0);
}

/* Getfp: wrapper for fopen */
FILE *Getfp(const char *name, const char *opt)
{
   FILE *fp = fopen(name, opt);

   if (fp == NULL) {
      fprintf(stderr, "ERROR: Getfp() in open_jtalk.c: Cannot open %s.\n", name);
      exit(1);
   }

   return (fp);
}

void *jt_malloc(unsigned int size)
{
    return (void *)malloc(size);
}

void jt_free(void *ptr)
{
    free(ptr);
}

void jt_mem_test()
{
    void *ptr;
    ptr = jt_malloc(100);
    jt_free(ptr);
}

void jt_save_logs(char *filename, HTS_Engine *engine, NJD *njd)
{
    FILE *logfp;
    logfp = fopen(filename, "wt");
    if (logfp != NULL) {
         fprintf(logfp, "[Text analysis result]\n");
         NJD_fprint(njd, logfp);
         fprintf(logfp, "\n[Output label]\n");
         HTS_Engine_save_label(engine, logfp);
         fprintf(logfp, "\n");
         HTS_Engine_save_information(engine, logfp);
    }
    fclose(logfp);
}

void jt_save_riff(char *filename, HTS_Engine *engine)
{
    FILE *wavfp;
    wavfp = fopen(filename, "wb");
    if (wavfp != NULL) {
        HTS_Engine_save_riff(engine, wavfp);
    }
    fclose(wavfp);
}

int _libopenjtalk_main(char *buff, char *owfile)
{
    fprintf(stderr, "buff %s\n", buff);
    fprintf(stderr, "owfile %s\n", owfile);
   //FILE *txtfp = stdin;
   char *txtfn = NULL;
   FILE *wavfp = NULL;
   FILE *logfp = NULL;

   /* text */
   // char buff[MAXBUFLEN];

   /* engine */
   OpenJTalk open_jtalk;

   /* directory name of dictionary */
   char *dn_mecab = NULL;

   /* file names of models */
   char *fn_ms_lf0 = NULL;
   char *fn_ms_mcp = NULL;
   char *fn_ms_dur = NULL;

   /* file names of trees */
   char *fn_ts_lf0 = NULL;
   char *fn_ts_mcp = NULL;
   char *fn_ts_dur = NULL;

   /* file names of windows */
   char **fn_ws_lf0;
   char **fn_ws_mcp;
   int num_ws_lf0 = 0, num_ws_mcp = 0;

   /* file names of global variance */
   char *fn_ms_gvl = NULL;
   char *fn_ms_gvm = NULL;

   /* file names of global variance trees */
   char *fn_ts_gvl = NULL;
   char *fn_ts_gvm = NULL;

   /* file names of global variance switch */
   char *fn_gv_switch = NULL;

   /* global parameter */
   int sampling_rate = 16000;
   int fperiod = 80;
   double alpha = 0.42;
   int stage = 0;               /* gamma = -1.0/stage */
   double beta = 0.0;
   int audio_buff_size = 1600;
   double uv_threshold = 0.5;
   double gv_weight_lf0 = 0.7;
   double gv_weight_mcp = 1.0;
   HTS_Boolean use_log_gain = FALSE;

   /* parse command line */
   //if (argc == 1)
   //   Usage();

   /* delta window handler for log f0 */
   fn_ws_lf0 = (char **) calloc(10 /*argc*/, sizeof(char *));
   /* delta window handler for mel-cepstrum */
   fn_ws_mcp = (char **) calloc(10 /*argc*/, sizeof(char *));

#if 0
    /* read command */
   while (--argc) {
      if (**++argv == '-') {
         switch (*(*argv + 1)) {
         case 'x':
            dn_mecab = *(++argv);
            --argc;
            break;
         case 't':
            switch (*(*argv + 2)) {
            case 'f':
            case 'p':
               fn_ts_lf0 = *(++argv); /* -tf $VOICE/tree-lf0.inf */
               break;
            case 'm':
               fn_ts_mcp = *(++argv); /* -tm $VOICE/tree-mgc.inf */
               break;
            case 'd':
               fn_ts_dur = *(++argv); /* -td $VOICE/tree-dur.inf */
               break;
            default:
               fprintf(stderr,
                       "ERROR: main() in open_jtalk.c: Invalid option '-t%c'.\n", *(*argv + 2));
               exit(1);
            }
            --argc;
            break;
         case 'm':
            switch (*(*argv + 2)) {
            case 'f':
            case 'p':
               fn_ms_lf0 = *(++argv); /* -mf $VOICE/lf0.pdf */
               break;
            case 'm':
               fn_ms_mcp = *(++argv); /* -mm $VOICE/mgc.pdf */
               break;
            case 'd':
               fn_ms_dur = *(++argv); /* -md $VOICE/dur.pdf */
               break;
            default:
               fprintf(stderr,
                       "ERROR: main() in open_jtalk.c: Invalid option '-m%c'.\n", *(*argv + 2));
               exit(1);
            }
            --argc;
            break;
         case 'd':
            switch (*(*argv + 2)) {
            case 'f':
            case 'p':
               fn_ws_lf0[num_ws_lf0] = *(++argv); /* -df $VOICE/lf0.win1 -df $VOICE/lf0.win2 -df $VOICE/lf0.win3 */
               num_ws_lf0++;
               break;
            case 'm':
               fn_ws_mcp[num_ws_mcp] = *(++argv); /* -dm $VOICE/mgc.win1 -dm $VOICE/mgc.win2 -dm $VOICE/mgc.win3 */
               num_ws_mcp++;
               break;
            default:
               fprintf(stderr,
                       "ERROR: main() in open_jtalk.c: Invalid option '-d%c'.\n", *(*argv + 2));
               exit(1);
            }
            --argc;
            break;
         case 'o':
            switch (*(*argv + 2)) {
            case 'w':
               wavfp = Getfp(*(++argv), "wb"); /* -ow _hoge.wav */
               break;
            case 't':
               logfp = Getfp(*(++argv), "w"); /* -ot _log.txt */
               break;
            default:
               fprintf(stderr, "ERROR: main() in open_jtalk.c: Invalid option '-o%c'.\n",
                       *(*argv + 2));
               exit(1);
            }
            --argc;
            break;
         case 'h':
            Usage();
            break;
         case 's':
            sampling_rate = atoi(*++argv);
            --argc;
            break;
         case 'p':
            fperiod = atoi(*++argv);
            --argc;
            break;
         case 'a':
            alpha = atof(*++argv);
            --argc;
            break;
         case 'g':
            stage = atoi(*++argv);
            --argc;
            break;
         case 'l':
            use_log_gain = TRUE;
            break;
         case 'b':
            beta = atof(*++argv);
            --argc;
            break;
         case 'u':
            uv_threshold = atof(*++argv);
            --argc;
            break;
         case 'e':
            switch (*(*argv + 2)) {
            case 'f':
            case 'p':
               fn_ts_gvl = *(++argv); /* -ef $VOICE/tree-gv-lf0.inf */
               break;
            case 'm':
               fn_ts_gvm = *(++argv); /* -em $VOICE/tree-gv-mgc.inf */
               break;
            default:
               fprintf(stderr,
                       "ERROR: main() in open_jtalk.c: Invalid option '-e%c'.\n", *(*argv + 2));
               exit(1);
            }
            --argc;
            break;
         case 'c':
            switch (*(*argv + 2)) {
            case 'f':
            case 'p':
               fn_ms_gvl = *(++argv); /* -cf $VOICE/gv-lf0.pdf */
               break;
            case 'm':
               fn_ms_gvm = *(++argv); /* -cm $VOICE/gv-mgc.pdf */
               break;
            default:
               fprintf(stderr,
                       "ERROR: main() in open_jtalk.c: Invalid option '-c%c'.\n", *(*argv + 2));
               exit(1);
            }
            --argc;
            break;
         case 'j':
            switch (*(*argv + 2)) {
            case 'f':
            case 'p':
               gv_weight_lf0 = atof(*(++argv));
               break;
            case 'm':
               gv_weight_mcp = atof(*(++argv));
               break;
            default:
               fprintf(stderr,
                       "ERROR: main() in open_jtalk.c: Invalid option '-j%c'.\n", *(*argv + 2));
               exit(1);
            }
            --argc;
            break;
         case 'k':
            fn_gv_switch = *++argv; /* -k $VOICE/gv-switch.inf */
            --argc;
            break;
         case 'z':
            audio_buff_size = atoi(*++argv);
            --argc;
            break;
         default:
            fprintf(stderr, "ERROR: main() in open_jtalk.c: Invalid option '-%c'.\n", *(*argv + 1));
            exit(1);
         }
      } else {
         txtfn = *argv;
         txtfp = Getfp(txtfn, "rt");
      }
   }
#endif
#if 0
   /* dictionary directory check */
   if (dn_mecab == NULL) {
      fprintf(stderr, "ERROR: main() in open_jtalk.c: No dictionary directory.\n");
      exit(1);
   }
   /* number of models,trees check */
   if (fn_ms_dur == NULL || fn_ms_mcp == NULL || fn_ms_lf0 == NULL ||
       fn_ts_dur == NULL || fn_ts_mcp == NULL || fn_ts_lf0 == NULL ||
       fn_ws_mcp == NULL || fn_ws_lf0 == NULL) {
      fprintf(stderr,
              "ERROR: main() in open_jtalk.c: Specify models (trees) for each parameter.\n");
      exit(1);
   }
#endif
   /* initialize and load */
   OpenJTalk_initialize(&open_jtalk, sampling_rate, fperiod, alpha, stage, beta, audio_buff_size,
                        uv_threshold, use_log_gain, gv_weight_mcp, gv_weight_lf0);
   fn_ws_mcp[0] = VOICE "/mgc.win1";
   fn_ws_mcp[1] = VOICE "/mgc.win2";
   fn_ws_mcp[2] = VOICE "/mgc.win3";
   fn_ws_lf0[0] = VOICE "/lf0.win1";
   fn_ws_lf0[1] = VOICE "/lf0.win2";
   fn_ws_lf0[2] = VOICE "/lf0.win3";
   OpenJTalk_load(&open_jtalk,
		  DIC, /* dn_mecab */ 
		  VOICE "/dur.pdf", /* fn_ms_dur */
		  VOICE "/tree-dur.inf", /* fn_ts_dur */
		  VOICE "/mgc.pdf", /* fn_ms_mcp */
		  VOICE "/tree-mgc.inf", /* fn_ts_mcp */
		  fn_ws_mcp,
		  3, /* num_ws_mcp */
		  VOICE "/lf0.pdf", /* fn_ms_lf0 */
		  VOICE "/tree-lf0.inf", /* fn_ts_lf0 */
		  fn_ws_lf0, 
		  3, /* num_ws_lf0 */
		  VOICE "/gv-mgc.pdf", /* fn_ms_gvm */
		  VOICE "/tree-gv-mgc.inf", /* fn_ts_gvm */
		  VOICE "/gv-lf0.pdf",  /* fn_ms_gvl */
		  VOICE "/tree-gv-lf0.inf", /* fn_ts_gvl */
		  VOICE "/gv-switch.inf" /* fn_gv_switch */
		  );

   /* synthesis */
   // fgets(buff, MAXBUFLEN - 1, txtfp);
   wavfp = Getfp("out.wav" /*owfile*/, "wb"); /* -ow _hoge.wav */
   OpenJTalk_synthesis(&open_jtalk, buff, wavfp, logfp);

   /* free */
   OpenJTalk_clear(&open_jtalk);
   free(fn_ws_mcp);
   free(fn_ws_lf0);
   //if (txtfn != NULL)
   //   fclose(txtfp);
   if (wavfp != NULL)
      fclose(wavfp);
   if (logfp != NULL)
      fclose(logfp);
    return 0;
}

