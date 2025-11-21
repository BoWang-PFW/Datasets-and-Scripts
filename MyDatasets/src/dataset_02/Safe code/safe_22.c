#include <stdio.h>
int main(void){
    char arr[8];
    for(int i=0;i<(int)sizeof arr-1;i++) arr[i]='0'+i;
    arr[sizeof arr-1]=0;
    puts(arr);
    return 0;
}
