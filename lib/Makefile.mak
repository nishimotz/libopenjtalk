# Makefile.mak
# libopenjtalk by Takuya Nishimoto
# for nmake 
# based on Open-JTalk

target: libopenjtalk.obj libopenjtalk.dll

CC = cl
LINK = link
CFLAGS = /O2 /Ob2 /Oi /Ot /Oy /GT /GL /TC 

INCLUDES = -I ../text2mecab \
           -I ../mecab/src \
           -I ../mecab2njd \
           -I ../njd \
           -I ../njd_set_pronunciation \
           -I ../njd_set_digit \
           -I ../njd_set_accent_phrase \
           -I ../njd_set_accent_type \
           -I ../njd_set_unvoiced_vowel \
           -I ../njd_set_long_vowel \
           -I ../njd2jpcommon \
           -I ../mecab2njd \
           -I ../jpcommon \
           -I ../../htsengineapi/include \
           -I. \
           -I../mecab

LDADD = ../text2mecab/text2mecab.lib \
           ../mecab2njd/mecab2njd.lib \
           ../njd/njd.lib \
           ../njd_set_pronunciation/njd_set_pronunciation.lib \
           ../njd_set_digit/njd_set_digit.lib \
           ../njd_set_accent_phrase/njd_set_accent_phrase.lib \
           ../njd_set_accent_type/njd_set_accent_type.lib \
           ../njd_set_unvoiced_vowel/njd_set_unvoiced_vowel.lib \
           ../njd_set_long_vowel/njd_set_long_vowel.lib \
           ../njd2jpcommon/njd2jpcommon.lib \
           ../jpcommon/jpcommon.lib \
           ../../htsengineapi/lib/HTS_Engine_API.lib

libopenjtalk.obj: libopenjtalk.c		   
	$(CC) $(INCLUDES) $(CFLAGS) /c libopenjtalk.c

libopenjtalk.dll: libopenjtalk.obj
	$(LINK) /DLL /RELEASE /MACHINE:x86 /LTCG /OUT:libopenjtalk.dll \
	libopenjtalk.obj $(LDADD) /DEF:libopenjtalk.def

clean:	
	del *.dll
	del *.obj
