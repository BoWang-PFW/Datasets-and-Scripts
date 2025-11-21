#include <stdio.h>
#include <string.h>
int main(void){
    char src[16]="source";
    char dst[16];
    strncpy(dst,src,sizeof dst-1);
    dst[sizeof dst-1]=0;
    puts(dst);
    return 0;
}
