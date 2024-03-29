
CC = cl

CFLAGS = /O2 /Ob2 /Oi /Ot /Oy /GT /GL /TC /D CHARSET_SHIFT_JIS /source-charset:shift_jis /execution-charset:shift_jis
LFLAGS = /LTCG

CORES = njd.obj njd_node.obj

all: njd.lib

njd.lib: $(CORES)
	lib $(LFLAGS) /OUT:$@ $(CORES)

.c.obj:
	$(CC) $(CFLAGS) /c $<

clean:
	del *.lib
	del *.obj
