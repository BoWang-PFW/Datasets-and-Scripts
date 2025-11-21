#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void){
    char *s=malloc(100);
    if(!s) return 1;
    if(fgets(s,100,stdin)){
        s[strcspn(s,"\n")]=0;
        puts(s);
    }
    free(s);
    return 0;
}
