#include <stdio.h>
#include <string.h>
int main(void){
    char s1[16]="short";
    char s2[16];
    size_t copy=sizeof s2-1;
    strncpy(s2,s1,copy);
    s2[copy]=0;
    puts(s2);
    return 0;
}
