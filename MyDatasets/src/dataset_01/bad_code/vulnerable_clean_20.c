 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  size_t len;
  char src[11];
  char buf[10];

  memset(src, 'A', 11);
  src[11 - 1] = '\0';
  len = 11;

   
  strncpy(buf, src, len);


  return 0;
}
