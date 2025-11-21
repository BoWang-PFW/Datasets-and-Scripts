#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void){
    size_t n=50;
    char *p=malloc(n);
    if(!p) return 1;
    memset(p,0,n);
    strncpy(p,"ok",n-1);
    puts(p);
    free(p);
    return 0;
}
