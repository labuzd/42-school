/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/23 17:03:57 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/23 18:58:24 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

char	*ft_strcpy(char *s1, char *s2)
{
	int i;

	i = 0;
	while (s2[i] != '\0')
	{
		s1[i] = s2[i];
		++i;
	}
	s1[i] = '\0';
	return (s1);
}

#include <stdio.h>

int main(void)
{
	char src[]  = "Flavio";
	char dst[]  = "Gaucho";

	ft_strcpy(dst, src);
	printf ("%s\n", dst);
}
