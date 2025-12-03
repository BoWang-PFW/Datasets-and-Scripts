#include <stdio.h>
#include <string.h>
int main(void){
    char base[32]="prefix";
    const char *s="suffix";
    size_t remain=sizeof base-strlen(base)-1;
    strncat(base,s,remain);
    puts(base);
    return 0;
}
