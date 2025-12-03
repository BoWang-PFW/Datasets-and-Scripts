#include <stdio.h>
#include <string.h>
int main(void){
    char buf[100];
    if(fgets(buf,sizeof buf,stdin)){
        size_t l=strlen(buf);
        if(l && buf[l-1]=='\n') buf[l-1]=0;
        puts(buf);
    }
    return 0;
}
