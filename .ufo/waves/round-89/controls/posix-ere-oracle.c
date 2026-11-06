/* mado round 89 — independent POSIX ERE oracle for case expectations (not the candidate's code path).
 *
 * Mirrors mako 1.11.0 criteria.c: regcomp(&re, pattern, REG_EXTENDED | REG_NOSUB) then
 * regexec(&re, text, 0, NULL, 0). Like mako, it never calls setlocale, so it runs in the C locale.
 * Usage: posix-ere-oracle PATTERN TEXT   (the strings after the criteria tokenizer has run)
 * Prints one of: match | nomatch | invalid   and exits 0 (2 on usage error).
 * Build: cc -O0 -o posix-ere-oracle posix-ere-oracle.c
 */
#include <regex.h>
#include <stdio.h>

int main(int argc, char **argv) {
	regex_t re;
	if (argc != 3) {
		fprintf(stderr, "usage: posix-ere-oracle PATTERN TEXT\n");
		return 2;
	}
	if (regcomp(&re, argv[1], REG_EXTENDED | REG_NOSUB) != 0) {
		puts("invalid");
		return 0;
	}
	puts(regexec(&re, argv[2], 0, NULL, 0) == 0 ? "match" : "nomatch");
	regfree(&re);
	return 0;
}
