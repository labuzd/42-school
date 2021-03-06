/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   repeat_alpha.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/24 12:51:01 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/24 13:24:14 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int		count(char c)
{
	int rep;

	if (c >= 'A' && c <= 'Z')
		rep = c - 'A' + 1;
	else if (c >= 'a' && c <= 'z')
		rep = c - 'a' + 1;
	else
		rep = 1;
	return (rep);
}

#include <unistd.h>

int	main(int ac, char **av)
{
	int rep;

	if (ac == 2)
	{
		while (*av[1])
		{
			rep = count(*av[1]);
			while (rep--)
				write(1, av[1], 1);
			av[1]++;
		}
	}
	write(1, "\n", 1);
}
