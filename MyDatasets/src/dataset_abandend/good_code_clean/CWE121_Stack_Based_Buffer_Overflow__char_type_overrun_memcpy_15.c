

#include "std_testcase.h"

#define SRC_STR "0123456789abcdef0123456789abcde"

typedef struct _charVoid
{
    char charFirst[16];
    void * voidSecond;
    void * voidThird;
} charVoid;

static void good1()
{
    switch(5)
    {
    case 6:
        
        printLine("Benign, fixed string");
        break;
    default:
    {
        charVoid structCharVoid;
        structCharVoid.voidSecond = (void *)SRC_STR;
        
        printLine((char *)structCharVoid.voidSecond);
        
        memcpy(structCharVoid.charFirst, SRC_STR, sizeof(structCharVoid.charFirst));
        structCharVoid.charFirst[(sizeof(structCharVoid.charFirst)/sizeof(char))-1] = '\0'; 
        printLine((char *)structCharVoid.charFirst);
        printLine((char *)structCharVoid.voidSecond);
    }
    break;
    }
}

static void good2()
{
    switch(6)
    {
    case 6:
    {
        charVoid structCharVoid;
        structCharVoid.voidSecond = (void *)SRC_STR;
        
        printLine((char *)structCharVoid.voidSecond);
        
        memcpy(structCharVoid.charFirst, SRC_STR, sizeof(structCharVoid.charFirst));
        structCharVoid.charFirst[(sizeof(structCharVoid.charFirst)/sizeof(char))-1] = '\0'; 
        printLine((char *)structCharVoid.charFirst);
        printLine((char *)structCharVoid.voidSecond);
    }
    break;
    default:
        
        printLine("Benign, fixed string");
        break;
    }
}

void CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_15_good()
{
    good1();
    good2();
}

int main(int argc, char * argv[])
{
    
    srand( (unsigned)time(NULL) );
    printLine("Calling good()...");
    CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_15_good();
    printLine("Finished good()");
    return 0;
}

