

#include "std_testcase.h"

#define SRC_STR "0123456789abcdef0123456789abcde"

typedef struct _charVoid
{
    char charFirst[16];
    void * voidSecond;
    void * voidThird;
} charVoid;

static int staticTrue = 1; 
static int staticFalse = 0; 

static void good1()
{
    if(staticFalse)
    {
        
        printLine("Benign, fixed string");
    }
    else
    {
        {
            charVoid structCharVoid;
            structCharVoid.voidSecond = (void *)SRC_STR;
            
            printLine((char *)structCharVoid.voidSecond);
            
            memcpy(structCharVoid.charFirst, SRC_STR, sizeof(structCharVoid.charFirst));
            structCharVoid.charFirst[(sizeof(structCharVoid.charFirst)/sizeof(char))-1] = '\0'; 
            printLine((char *)structCharVoid.charFirst);
            printLine((char *)structCharVoid.voidSecond);
        }
    }
}

static void good2()
{
    if(staticTrue)
    {
        {
            charVoid structCharVoid;
            structCharVoid.voidSecond = (void *)SRC_STR;
            
            printLine((char *)structCharVoid.voidSecond);
            
            memcpy(structCharVoid.charFirst, SRC_STR, sizeof(structCharVoid.charFirst));
            structCharVoid.charFirst[(sizeof(structCharVoid.charFirst)/sizeof(char))-1] = '\0'; 
            printLine((char *)structCharVoid.charFirst);
            printLine((char *)structCharVoid.voidSecond);
        }
    }
}

void CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_05_good()
{
    good1();
    good2();
}

int main(int argc, char * argv[])
{
    
    srand( (unsigned)time(NULL) );
    printLine("Calling good()...");
    CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_05_good();
    printLine("Finished good()");
    return 0;
}

