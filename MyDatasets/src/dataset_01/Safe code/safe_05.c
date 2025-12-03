#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(void){
    char *s=malloc(20);
    if(!s) return 1;
    strncpy(s,"short string",19);
    s[19]=0;
    puts(s);
    free(s);
    return 0;
}
