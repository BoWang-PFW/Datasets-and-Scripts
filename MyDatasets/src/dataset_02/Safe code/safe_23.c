#include <stdio.h>
#include <string.h>
int main(void){
    const char *src="data";
    char dst[5];
    if(strlen(src)<sizeof dst) strcpy(dst,src);
    else dst[0]=0;
    puts(dst);
    return 0;
}
