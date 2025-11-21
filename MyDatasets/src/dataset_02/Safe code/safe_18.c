#include <stdio.h>
#include <string.h>
int main(void){
    char dst[32];
    const char *in="input";
    size_t d=sizeof dst;
    if(strlen(in)+1<=d) memcpy(dst,in,strlen(in)+1);
    else dst[0]=0;
    puts(dst);
    return 0;
}
