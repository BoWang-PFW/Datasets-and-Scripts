 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  char src[11];
  char buf[10];

  memset(src, 'A', 11);
  src[11 - 1] = '\0';

   
  strncpy(buf, src, 11);


  return 0;
}
