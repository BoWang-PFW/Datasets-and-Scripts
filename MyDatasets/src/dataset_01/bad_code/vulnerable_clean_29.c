 

 

#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40
void
test(char *str1, char *str2)
{
	char buf[MAXSIZE];
	char *p;
	int l, x;

	p = buf;
	l = sizeof buf;

	snprintf(p, l, "<%s>", str1);
	x = strlen(p);
	p += x;
	l -= x;

	 
	*p++ = ' ';					 
	*p++ = '-';					 
	l -= 2;						 

	 
	snprintf(p, l, "<%s>\n", str2);			 
	x = strlen(p);
	p += x;
	l -= x;

	printf("result: %s\n", buf);
}

int
main(int argc, char **argv)
{
	char *userstr, *userstr2;

	if(argc > 2) {
		userstr = argv[1];
		userstr2 = argv[2];
		test(userstr, userstr2);
	}
	return 0;
}

