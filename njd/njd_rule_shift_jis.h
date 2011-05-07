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

#ifndef NJD_RULE_H
#define NJD_RULE_H

#ifdef __cplusplus
#define NJD_RULE_H_START extern "C" {
#define NJD_RULE_H_END   }
#else
#define NJD_RULE_H_START
#define NJD_RULE_H_END
#endif                          /* __CPLUSPLUS */

NJD_RULE_H_START;

static const char *njd_mora_list[] = {
   "����",
   "����",
   "����",
   "���H",
   "���F",
   "���B",
   "���@",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "����",
   "����",
   "����",
   "���F",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "��",
   "�~��",
   "�~��",
   "�~��",
   "�~�F",
   "�~",
   "�}",
   "�|",
   "�{",
   "�z",
   "�y",
   "�x",
   "�w",
   "�v",
   "�u",
   "�t�H",
   "�t�F",
   "�t�B",
   "�t�@",
   "�t",
   "�s��",
   "�s��",
   "�s��",
   "�s�F",
   "�s",
   "�r��",
   "�r��",
   "�r��",
   "�r�F",
   "�r",
   "�q��",
   "�q��",
   "�q��",
   "�q�F",
   "�q",
   "�p",
   "�o",
   "�n",
   "�m",
   "�l",
   "�k",
   "�j��",
   "�j��",
   "�j��",
   "�j�F",
   "�j",
   "�i",
   "�h�D",
   "�h",
   "�g",
   "�f��",
   "�f��",
   "�f��",
   "�f�F",
   "�f�B",
   "�f",
   "�e��",
   "�e��",
   "�e��",
   "�e�B",
   "�e",
   "�d",
   "�c�H",
   "�c�F",
   "�c�B",
   "�c�@",
   "�c",
   "�b",
   "�a",
   "�`��",
   "�`��",
   "�`��",
   "�`�F",
   "�`",
   "�_",
   "�^",
   "�]",
   "�\",
   "�[",
   "�Z",
   "�Y�B",
   "�Y",
   "�X�B",
   "�X",
   "�W��",
   "�W��",
   "�W��",
   "�W�F",
   "�W",
   "�V��",
   "�V��",
   "�V��",
   "�V�F",
   "�V",
   "�U",
   "�T",
   "�S",
   "�R",
   "�Q",
   "�P",
   "�O",
   "�N",
   "�M��",
   "�M��",
   "�M��",
   "�M�F",
   "�M",
   "�L��",
   "�L��",
   "�L��",
   "�L�F",
   "�L",
   "�K",
   "�J",
   "�I",
   "�H",
   "�G",
   "�F",
   "�E�H",
   "�E�F",
   "�E�B",
   "�E",
   "�D",
   "�C�F",
   "�C",
   "�B",
   "�A",
   "�@",
   "�[",
   NULL
};

NJD_RULE_H_END;

#endif                          /* !NJD_RULE_H */
