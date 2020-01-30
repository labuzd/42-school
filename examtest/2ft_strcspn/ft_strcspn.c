/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strcspn.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dlabuz <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/01/29 19:35:51 by dlabuz            #+#    #+#             */
/*   Updated: 2020/01/29 20:20:22 by dlabuz           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <string.h>

char *ft_strchr(const char *s, int c)
{
	while (*s != '\0')
	{
		if (*s == c)
			return ((char*)s);
		s++;
	}	
	return (0);
}

size_t	ft_strcspn(const char *s, const char *reject)
{
	size_t i = 0;

	while (s[i] != '\0')
	{
		if (ft_strchr(reject, s[i]) != 0)
				break;
				++i;
	}
	return (i);
}

#include <stdio.h>

int main(void)
{
	printf("%zu\n", strcspn("hello world", "ol"));
	printf("%zu\n", ft_strcspn("hello world", "ol"));
}
