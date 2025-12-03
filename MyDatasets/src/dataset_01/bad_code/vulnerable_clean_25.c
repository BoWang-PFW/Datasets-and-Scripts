 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  int i;
  char src[10];
  char buf[10];

  memset(src, 'A', 10);
  src[10 - 1] = '\0';
  i = 2;

   
  strncpy(buf, src, (4 * i) + 2);


  return 0;
}
