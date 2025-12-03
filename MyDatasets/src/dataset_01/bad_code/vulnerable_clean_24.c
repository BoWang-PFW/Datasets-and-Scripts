 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  int i;
  char src[11];
  char buf[10];

  memset(src, 'A', 11);
  src[11 - 1] = '\0';
  i = 2;

   
  strncpy(buf, src, (4 * i) + 3);


  return 0;
}
