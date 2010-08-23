# Makefile.shlib
# by Takuya Nishimoto
# usage:
# $ make -f Makefile.shlib

target: libopen_jtalk.o ojt_mecab.dll libopenjtalk.dll dlmain.exe

CC = gcc -mno-cygwin
CXX = g++ -mno-cygwin

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
           -I ../jpcommon \
           -I ../../htsengineapi/include \
           -I. \
           -I../mecab

LDADD = ../text2mecab/libtext2mecab.a \
           ../mecab2njd/libmecab2njd.a \
           ../njd/libnjd.a \
           ../njd_set_pronunciation/libnjd_set_pronunciation.a \
           ../njd_set_digit/libnjd_set_digit.a \
           ../njd_set_accent_phrase/libnjd_set_accent_phrase.a \
           ../njd_set_accent_type/libnjd_set_accent_type.a \
           ../njd_set_unvoiced_vowel/libnjd_set_unvoiced_vowel.a \
           ../njd_set_long_vowel/libnjd_set_long_vowel.a \
           ../njd2jpcommon/libnjd2jpcommon.a \
           ../jpcommon/libjpcommon.a \
           ../../htsengineapi/lib/libHTSEngine.a

ojt_mecab.dll:
	$(CC) -shared -o ojt_mecab.dll ../mecab/src/libmecab.a -lstdc++ \
	-Wl,--output-def,ojt_mecab.def,--out-implib,ojt_mecab_imp.lib

libopen_jtalk.o: libopen_jtalk.c
	$(CC) -c -o libopen_jtalk.o -DHAVE_CONFIG_H $(INCLUDES) libopen_jtalk.c

libopenjtalk.dll: libopen_jtalk.o ojt_mecab_imp.lib
	$(CC) -shared -o libopenjtalk.dll \
	libopen_jtalk.o $(LDADD) \
	-Wl,--output-def,libopenjtalk.def,--out-implib,libopenjtalk_implib.lib

#ojt_mecab_imp.lib 

#libopenjtalk_static.a: libopen_jtalk.o
#	ar crus libopenjtalk_static.a libopen_jtalk.o

dlmain.exe:
	$(CC) dlmain.c -o dlmain

test: libopenjtalk.dll ojt_mecab.dll dlmain.exe
	./dlmain 

clean:
	\rm -f libopenjtalk.dll dlmain.exe libopen_jtalk.o ojt_mecab.dll
