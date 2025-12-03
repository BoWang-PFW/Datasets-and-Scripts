 

 

 

#include <string.h>

int main(int argc, char *argv[])
{
  size_t len;
  char src[4106];
  char buf[10];

  memset(src, 'A', 4106);
  src[4106 - 1] = '\0';
  len = 4106;

   
  strncpy(buf, src, len);


  return 0;
}
