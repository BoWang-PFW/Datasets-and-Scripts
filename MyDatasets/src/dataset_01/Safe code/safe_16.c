#include <stdio.h>
#include <string.h>
int main(void){
    char a[20];
    char b[20];
    snprintf(a,sizeof a,"%s","alpha");
    snprintf(b,sizeof b,"%s",a);
    puts(b);
    return 0;
}
