#include <stdio.h>
#include <string.h>
int main(void){
    char buf1[50]="abcdefghij";
    char buf2[50];
    size_t n=strlen(buf1);
    if(n<sizeof buf2) memmove(buf2,buf1,n+1);
    printf("%s\n",buf2);
    return 0;
}
