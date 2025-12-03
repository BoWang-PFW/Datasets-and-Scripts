#include <stdio.h>
#include <string.h>
int main(void){
    char buf[16];
    const char *src="123456789";
    if(strlen(src)<sizeof buf) strcpy(buf,src);
    else buf[0]=0;
    puts(buf);
    return 0;
}
