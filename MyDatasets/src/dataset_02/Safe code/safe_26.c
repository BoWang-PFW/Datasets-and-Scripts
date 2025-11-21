#include <stdio.h>
#include <string.h>
int main(void){
    char a[16]="part1";
    char b[16]="part2";
    char out[32];
    size_t rem=sizeof out;
    int r=snprintf(out,rem,"%s-%s",a,b);
    if(r<0 || (size_t)r>=rem) return 1;
    puts(out);
    return 0;
}
