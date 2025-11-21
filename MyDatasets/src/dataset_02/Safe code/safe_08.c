#include <stdio.h>
#include <string.h>
int main(void){
    char buf[128];
    if(fgets(buf,sizeof buf,stdin)){
        size_t n=strcspn(buf,"\n");
        buf[n]=0;
        puts(buf);
    }
    return 0;
}
