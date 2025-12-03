#include <stdio.h>
#include <string.h>
int main(void){
    char buf[40]="";
    const char *parts[]={"one","two","three"};
    for(int i=0;i<3;i++){
        size_t remain=sizeof buf-strlen(buf)-1;
        strncat(buf,parts[i],remain);
        if(i<2) strncat(buf," ",remain>0?1:0);
    }
    puts(buf);
    return 0;
}
