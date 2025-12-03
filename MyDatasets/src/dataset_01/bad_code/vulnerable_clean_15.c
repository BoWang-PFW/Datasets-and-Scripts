 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  char src[18];
  char buf[10];

  memset(src, 'A', 18);
  src[18 - 1] = '\0';

   
  strncpy(buf, src, 18);


  return 0;
}
