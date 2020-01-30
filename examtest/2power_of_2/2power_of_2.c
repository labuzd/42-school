/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   2power_of_2.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/30 12:27:34 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/30 12:54:32 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	    is_power_of_2(unsigned int n)
{
	unsigned long p = 1;

	while (p < n)
		p = 2 * p;

	if (p == n)
		return (1);
	else
		return (0);
}

#include <stdio.h>

int	main(void)
{
	unsigned int n = 4294967295;
	printf("Is %u a power of 2? %d\n", n, is_power_of_2(n));
}
