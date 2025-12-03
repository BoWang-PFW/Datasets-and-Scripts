 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  int i;
  char src[18];
  char buf[10];

  memset(src, 'A', 18);
  src[18 - 1] = '\0';
  i = 4;

   
  strncpy(buf, src, (4 * i) + 2);


  return 0;
}
