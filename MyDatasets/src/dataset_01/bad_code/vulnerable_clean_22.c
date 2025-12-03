 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  int i;
  char src[4106];
  char buf[10];

  memset(src, 'A', 4106);
  src[4106 - 1] = '\0';
  i = 1026;

   
  strncpy(buf, src, (4 * i) + 2);


  return 0;
}
