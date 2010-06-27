/* dlmain.c
 * by Takuya Nishimoto
 */

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
    handle = dlopen("libopenjtalk.so.1.0.1", RTLD_LAZY);
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
