/* libopenjtalk.c    
 * based on ../bin/open_jtalk.c
 * by Takuya Nishimoto
 * since 2010-06-27    
 * Notice: some functions in this file is dummy 
 * (to export functions inside the *.a)
 */

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

/* Main headers */
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

char *jt_version()
{
	return "libopenjtalk 20120222 (github)";
}

void *jt_malloc(unsigned int size)
{
    return (void *)malloc(size);
}

void jt_free(void *ptr)
{
    free(ptr);
}

void jt_save_logs(char *filename, HTS_Engine *engine, NJD *njd)
{
    FILE *logfp;
    logfp = fopen(filename, "at");
    if (logfp != NULL) {
         fprintf(logfp, "[Text analysis result]\n");
         NJD_fprint(njd, logfp);
         fprintf(logfp, "\n[Output label]\n");
         HTS_Engine_save_label(engine, logfp);
         fprintf(logfp, "\n");
         HTS_Engine_save_information(engine, logfp);
         fprintf(logfp, "\n");
         fprintf(logfp, "\n");
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

int jt_total_nsample(HTS_Engine * engine)
{
   HTS_GStreamSet *gss = &engine->gss;
   return HTS_GStreamSet_get_total_nsample(gss);
}

short *jt_speech_ptr(HTS_Engine * engine)
{
   HTS_GStreamSet *gss = &engine->gss;
   return gss->gspeech;
}

/* level = 0..32767 */
void jt_speech_normalize(HTS_Engine * engine, short level)
{
	int ns, i;
	short *data;
	short max = 0;
	level = abs(level);
	ns = jt_total_nsample(engine);
	data = jt_speech_ptr(engine);
	for (i = 0; i < ns; i++) {
		int a;
		a = abs(data[i]);
		if (max < a) max = a;
	}
	for (i = 0; i < ns; i++) {
		data[i] = (int)((double)(data[i]) * level / max);
	}
}

/* returns: new sample count */
int jt_trim_silence(HTS_Engine * engine, short begin_thres, short end_thres)
{
	int ns, i, size;
	short *data;
	int begin_pos = 0, end_pos = 0;
	ns = jt_total_nsample(engine);
	data = jt_speech_ptr(engine);
	if (begin_thres >= 0) {
		begin_thres = abs(begin_thres);
		for (i = 0; i < ns; i++) {
			if (abs(data[i]) > begin_thres) {
				begin_pos = i;
				break;
			}
		}
	}
	end_pos = ns - 1;
	if (end_thres >= 0) {
		end_thres = abs(end_thres);
		for (i = ns - 1; i >= 0; i--) {
			if (abs(data[i]) > end_thres) {
				end_pos = i;
				break;
			}
		}
	}
	size = end_pos - begin_pos + 1;
	memmove(data, &(data[begin_pos]), sizeof(short) * size);
	return size;
}
