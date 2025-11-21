#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void){
    size_t len=10;
    char *p=malloc(len+1);
    if(!p) return 1;
    for(size_t i=0;i<len;i++) p[i]='x';
    p[len]=0;
    puts(p);
    free(p);
    return 0;
}
