#include <stdio.h>
#include <string.h>
int main(void){
    char dest[20];
    const char *src="123456789012345";
    if(strlen(src)+1<=sizeof dest) memcpy(dest,src,strlen(src)+1);
    else dest[0]=0;
    puts(dest);
    return 0;
}
