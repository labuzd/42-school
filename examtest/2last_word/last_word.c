#include <unistd.h>

int	main(int ac, char **av)
{
	if (ac == 2)
	{
		while (*av[1])
		++av[1];
			if (av[1] >= 0 && (*av[1] == ' ' || *av[1] == '\t' || *av[1] == '\0'))
		--av[1];
			else if (av[1] >= 0 && *av[1] != ' ' && *av[1] != '\t')
		--av[1];
			else if (*av[1]
		}
	}
}
