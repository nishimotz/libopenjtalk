/* dlmain.c
 * by Takuya Nishimoto
 */

#if 0
#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
 
int main(int argc, char **argv)
{
    void *handle;
    int (*func_jtalk)(int ac, char **av);
    char *error;
    int ret;
    handle = dlopen("libopenjtalk.dll", RTLD_LAZY);
    if (!handle) {
        fputs (dlerror(), stderr);
        exit(1);
    }
    func_jtalk = dlsym(handle, "libopen_jtalk_main");
    if ((error = dlerror()) != NULL)  {
        fputs(error, stderr);
        exit(1);
    }
    ret = (*func_jtalk)(argc, argv);
    dlclose(handle);
    return ret;
}

#else
#include <windows.h>

int main(int argc, char **argv)
{
    HMODULE hModule;
    int (*func_jtalk)(char *buff, char *owfile);
    int ret = 1;

    hModule = LoadLibrary( "libopenjtalk.dll" );
    if (hModule != NULL) {
	func_jtalk = (void *)GetProcAddress( hModule, "libopen_jtalk_main" );
	if (func_jtalk != NULL) {
	    char *buff = "こんにちは"; // UTF-8
	    char *owfile = "out1.wav";
	    ret = (*func_jtalk)(buff, owfile);
	}
	FreeLibrary(hModule);
    }
    return ret;
}

#endif
