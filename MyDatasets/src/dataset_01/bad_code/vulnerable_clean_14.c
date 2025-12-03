 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  char src[4106];
  char buf[10];

  memset(src, 'A', 4106);
  src[4106 - 1] = '\0';

   
  strncpy(buf, src, 4106);


  return 0;
}
