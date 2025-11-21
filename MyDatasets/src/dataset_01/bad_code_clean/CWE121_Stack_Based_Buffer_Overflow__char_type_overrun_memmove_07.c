

#include "std_testcase.h"

#define SRC_STR "0123456789abcdef0123456789abcde"

typedef struct _charVoid
{
    char charFirst[16];
    void * voidSecond;
    void * voidThird;
} charVoid;

static int staticFive = 5;

void CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memmove_07_bad()
{
    if(staticFive==5)
    {
        {
            charVoid structCharVoid;
            structCharVoid.voidSecond = (void *)SRC_STR;
            
            printLine((char *)structCharVoid.voidSecond);
            
            memmove(structCharVoid.charFirst, SRC_STR, sizeof(structCharVoid));
            structCharVoid.charFirst[(sizeof(structCharVoid.charFirst)/sizeof(char))-1] = '\0'; 
            printLine((char *)structCharVoid.charFirst);
            printLine((char *)structCharVoid.voidSecond);
        }
    }
}

int main(int argc, char * argv[])
{
    
    srand( (unsigned)time(NULL) );
    printLine("Calling bad()...");
    CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memmove_07_bad();
    printLine("Finished bad()");
    return 0;
}

