 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  char src[10];
  char buf[10];

  memset(src, 'A', 10);
  src[10 - 1] = '\0';

   
  strncpy(buf, src, 10);


  return 0;
}
