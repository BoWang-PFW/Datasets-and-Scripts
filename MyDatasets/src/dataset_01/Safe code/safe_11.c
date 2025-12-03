#include <stdio.h>
#include <string.h>
int main(void){
    char buf[40];
    const char *a="one";
    const char *b="two";
    int r=snprintf(buf,sizeof buf,"%s:%s",a,b);
    if(r<0 || (size_t)r>=sizeof buf) return 1;
    puts(buf);
    return 0;
}
