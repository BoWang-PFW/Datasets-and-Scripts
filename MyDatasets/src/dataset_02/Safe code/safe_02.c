#include <stdio.h>
int main(int argc,char**argv){
    char buf[64];
    if(argc>1) snprintf(buf,sizeof buf,"%s",argv[1]);
    printf("%s\n",buf);
    return 0;
}
