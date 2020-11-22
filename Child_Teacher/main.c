#include <stdio.h>
#include "Microcontroller/colors.h"
#include <string.h>
int main()
{
    char *sent = "this is my sampl example";

    if (strstr(sent, word_8) != NULL)
        printf("I have find it");
    else
        printf("NOP");
    return 0;
}