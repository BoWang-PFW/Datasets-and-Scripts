 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  size_t len;
  char src[10];
  char buf[10];

  memset(src, 'A', 10);
  src[10 - 1] = '\0';
  len = 10;

   
  strncpy(buf, src, len);


  return 0;
}
