#include <stdio.h>

int main(void) {
  int number = 0x12345678;
  char first_byte = *((char *)(&number));

  if (0x78 == first_byte) {
    printf("Little Endian\n");
  } else {
    printf("Big Endian\n");
  }

  return 0;
}