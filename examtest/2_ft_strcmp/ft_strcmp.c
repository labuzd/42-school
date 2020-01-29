int	ft_strcmp(char *s1, char *s2)
{
	int	i = 0;
	
	while (s1[i] != '\0' && s2[i] != '\0' && s1[i] == s2[i])
		++i;
		if (s1[i] == s2[i])
		return (0);
		else if (s1[i] > s2[i])
		return (1);
		else
		return (-1);
}

#include <stdio.h>
#include <string.h>

int main(void)
{
	printf("%d\n", strcmp("abc", "abz"));
	printf("%d\n", ft_strcmp("abc", "abz"));
}
