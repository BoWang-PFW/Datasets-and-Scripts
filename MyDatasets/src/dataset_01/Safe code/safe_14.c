#include <stdio.h>
#include <string.h>
#include <stdint.h>
int main(void){
    char dest[32];
    char src[32];
    memset(src,'A',31);
    src[31]=0;
    size_t n=sizeof dest;
    if(strlen(src)+1<=n) memcpy(dest,src,strlen(src)+1);
    else dest[0]=0;
    puts(dest);
    return 0;
}
