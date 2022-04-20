#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main() {
	

	uint32_t seed = 0x561000;
	while (1) {
		printf("%x\n", seed);
		int pid = fork();
		if (pid == 0) {
			srand(seed);
			uint32_t a = rand();
			uint32_t b = rand();
			uint32_t c = rand();
			printf("%x %x %x\n", a, b, c);
			if ((a == 306291429) && (b == 442612432) && (c == 110107425)){
			printf("Success %x\n", seed);
			printf("\n\n");
			char* buf;
			read(0, buf, 5);
			}
			exit(1);
		}
		wait(NULL);
		seed ++;
	}

}
