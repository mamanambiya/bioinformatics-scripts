/*	C program to create multiple redundancy in a fasta file for
	testing external redundancy scripts.
	Coded by Steve Moss
	Email: gawbul@gmail.com */

/* program includes */
#include <stdio.h>
#include <stdlib.h>

/* main program subroutine */
int main(int argc, char *argv[]) {
	
	/* declare variables */
	int i;
	long len;
	char *buffer;
	FILE *fasin, *fasout;

	/* check usage */
	if(argc != 4)
	{
		printf("Usage: create_redundancy <infile> <redundancy> <outfile>\n");
	}
	else 
	{
		/* Check files exist */
		if(fasin==NULL || !fasin) {
			fprintf(stderr,"%s: No such file or directory\n",argv[1]);
			return 0;
		}
		else if(fasout==NULL || !fasout) {
			fprintf(stderr,"%s: No such file or directory\n",argv[3]);
			return 0;
		}
		else {
			/* Read file to buffer */
			fasin=fopen(argv[1],"r");
			fseek(fasin,0,SEEK_END);
			len=ftell(fasin);
			fseek(fasin,0,SEEK_SET);
			buffer=(char *)malloc(len); 
			fread(buffer,len,1,fasin);
			fclose(fasin);

			fasout = fopen(argv[3], "a+");
			/* Create redundancy */
			for (i=1; i <= atoi(argv[2]); i++) {
				fwrite(buffer,1,(sizeof(buffer),len),fasout);
		}
		fclose(fasout);
		printf("Done\n");
		}

	}	
	return 0;
}
