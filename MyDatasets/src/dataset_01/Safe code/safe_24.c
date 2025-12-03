#include <stdio.h>
#include <string.h>
int main(void){
    char buf[64];
    fgets(buf,sizeof buf,stdin);
    size_t n=strnlen(buf,sizeof buf);
    if(n) buf[n-1]=0;
    puts(buf);
    return 0;
}
