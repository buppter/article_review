# -*- coding: utf-8 -*-
_Author_ = 'BUPPT'


class UserKeywords:
    def __init__(self, keywords):
        self.keywords_list = []

        self.__parse(keywords)

    def __parse(self, keywords):
        for keyword in keywords:
            if keyword is not None:
                self.keywords_list.append(keyword)
