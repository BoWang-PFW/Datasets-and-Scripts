#include <stdio.h>
#include <string.h>
int main(void){
    char data[64];
    size_t used=0;
    const char *part="hello";
    size_t want=strlen(part);
    if(used+want+1<=sizeof data){
        memcpy(data+used,part,want);
        used+=want;
        data[used]=0;
    }
    puts(data);
    return 0;
}