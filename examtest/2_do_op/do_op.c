/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   do_op.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/28 17:09:56 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/28 18:08:17 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>

int main(int ac, char **av)
{
	if (ac == 4)
	{
		int x = atoi(av[1]);
		int y = atoi(av[3]);
		int z = *av[2];

		if (z == '+')
			printf("%d", x + y);
		else if (z == '-')
            printf("%d", x - y);
		else if (z == '*')
			printf("%d", x * y);
		else if (y == 0)
			printf("impossible");
		else if (z == '/')
			printf("%d", x / y);
		else if (z == '%')
			printf("%d", x % y);
	}
	printf("\n");
	return (0);
}
