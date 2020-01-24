/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   a_aff.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/17 15:18:33 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/17 15:50:01 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int		main(int ac, char **av)
{
	if (ac != 2)
		write(1, "a", 1);
	else
	{
		while (*av[1] != '\0')
		{
			if (*av[1] == 'a')
			{
				write(1, "a", 1);
				break ;
			}
			av[1]++;
		}
	}
	write(1, "\n", 1);
	return (0);
}
