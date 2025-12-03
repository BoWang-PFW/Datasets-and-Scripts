 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  size_t len;
  char src[18];
  char buf[10];

  memset(src, 'A', 18);
  src[18 - 1] = '\0';
  len = 18;

   
  strncpy(buf, src, len);


  return 0;
}
