#include <stdio.h>
#include <string.h>
int main(void){
    char s[64]="alpha beta gamma";
    char *tok=strtok(s," ");
    while(tok){
        printf("%s\n",tok);
        tok=strtok(NULL," ");
    }
    return 0;
}
