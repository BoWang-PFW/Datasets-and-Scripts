#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void){
    size_t n=16;
    char *p=calloc(1,n);
    if(!p) return 1;
    if(n>1) strncpy(p,"data",n-1);
    p[n-1]=0;
    puts(p);
    free(p);
    return 0;
}
