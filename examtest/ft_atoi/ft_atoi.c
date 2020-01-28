/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/27 19:45:18 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/27 20:03:06 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_atoi(const char *str)
{
	int	result = 0;
	int sign = 1;
	int digit;

	if (*str == '-')
	{
		sign = -1;
		++str;
	}
	while  (*str >= '0' && *str <= '9')
	{
		result = result * 10;
		digit = *str - '0';
		result = result + (digit * sign);
		++str;
	}
	return (result);
}

#include <stdio.h>

int main()
{
	printf("%d\n", ft_atoi("123456"));
}
