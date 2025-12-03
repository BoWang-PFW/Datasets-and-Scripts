 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  char src[11];
  char buf[10];

  memset(src, 'A', 11);
  src[11 - 1] = '\0';

   
  strcpy(buf, src);


  return 0;
}
