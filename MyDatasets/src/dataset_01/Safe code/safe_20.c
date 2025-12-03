#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(void){
    char *buf=NULL;
    size_t len=32;
    buf=malloc(len);
    if(!buf) return 1;
    snprintf(buf,len,"%s","safe");
    puts(buf);
    free(buf);
    return 0;
}
