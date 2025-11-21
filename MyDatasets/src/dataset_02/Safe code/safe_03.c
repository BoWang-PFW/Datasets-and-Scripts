#include <stdio.h>
#include <string.h>
int main(void){
    char a[32]="hello";
    char b[32]="world";
    char out[64];
    snprintf(out,sizeof out,"%s %s",a,b);
    puts(out);
    return 0;
}
