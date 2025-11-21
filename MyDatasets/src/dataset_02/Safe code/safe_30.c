#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void){
    size_t n=16;
    char *p=malloc(n);
    if(!p) return 1;
    const char *s="safecontent";
    if(strlen(s)+1<=n) memcpy(p,s,strlen(s)+1);
    else p[0]=0;
    puts(p);
    free(p);
    return 0;
}
