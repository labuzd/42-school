/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/18 15:49:11 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/18 16:19:18 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int	main(int ac, char **av)
{
	if (ac == 2)
	{
		while (*av[1])
		{
			if (*av[1] >= 'A' && *av[1] <= 'Z')
			{
				*av[1] += 32;
				write(1, av[1], 1);
			}
			else if (*av[1] >= 'a' && *av[1] <= 'z')
			{
				*av[1] -= 32;
				write(1, av[1], 1);
			}
			else if (*av[1] >= '0' && *av[1] <= '9')
				write(1, av[1], 1);
			av[1]++;
		}
	}
	write(1, "\n", 1);
		return (0);
}
