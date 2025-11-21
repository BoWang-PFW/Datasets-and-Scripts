#include <stdio.h>
#include <string.h>
int safe_copy(char *dst,size_t dlen,const char*src){
    size_t sl=strlen(src);
    if(sl>=dlen) return -1;
    memcpy(dst,src,sl+1);
    return 0;
}
int main(void){
    char d[20];
    if(safe_copy(d,sizeof d,"ok")==0) puts(d);
    return 0;
}
