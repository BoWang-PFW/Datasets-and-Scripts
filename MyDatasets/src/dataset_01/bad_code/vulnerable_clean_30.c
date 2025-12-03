 

 

#include <stdio.h>
#include <string.h>

 
#define	MAXSIZE		5

void
test(char *str)
{
	char buf[MAXSIZE];

	 
	sprintf(buf, "<%.5s>", str);		 
	printf("result: %s\n", buf);
}

int
main(int argc, char **argv)
{
	char *userstr;

	if(argc > 1) {
		userstr = argv[1];
		test(userstr);
	}
	return 0;
}

