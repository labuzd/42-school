int ft_strlen(char *str)
{
	int i = 0;

	while (str[i] != '\0')
	++i;
	return (i);
}

char    *ft_strrev(char *str)
{
	int l = 0;
	int r = ft_strlen(str) - 1;
	int  rev;

	while (l < r)
	{
		rev = str[l];
		str[l] = str[r];
		str[r] = rev;
		++l;
		--r;
	}
	return (str);
}

#include <stdio.h>

int main (void)
{
	char str[] = "hello world";

	printf("%s\n", ft_strrev(str));
}
