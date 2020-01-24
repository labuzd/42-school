/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   repeat_alpha.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/23 22:36:51 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/23 23:44:12 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int main(int ac, char **av)
{
	int repeat;

	if (ac == 2)
	{
		while (*av[1])
		{
			if (*av[1] >= 'A' && *av[1] <= 'Z')
				repeat = *av[1] - 'A' + 1;
			else if (*av[1] >= 'a' && *av[1] <= 'z')
				repeat = *av[1] - 'a' + 1;
			else
				repeat = 1;
			return (repeat);
			while (repeat--)
            write(1, av[1], 1);
        av[1]++;
		}
//		while (repeat--)
//			write(1, av[1], 1);
//		av[1]++;
	}
	write(1, "\n", 1);	
}
