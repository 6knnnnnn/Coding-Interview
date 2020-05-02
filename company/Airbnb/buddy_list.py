# -*- coding: utf-8 -*-


class Traveler(object):
    def __init__(self, name, cities):
        self.name = name
        self.cities = cities

    def find_similarities(self, others_city_set):
        count = 0
        different_cities = set([])
        for city in self.cities:
            if city in others_city_set:
                count += 1
            else:
                different_cities.add(city)
        return count, different_cities

    def __repr__(self):
        return "%s, %s of cities" % (self.name, len(self.cities))


class BuddyRecommender(object):
    def __init__(self, mine, others_cities):
        self.mine = set(mine)
        self.others_cities = others_cities
        self.buddy_list = list([])

    def get_buddies(self):
        for name, cities in self.others_cities.items():
            if not cities:
                continue
            traveler = Traveler(name, cities)
            count, different_cities = traveler.find_similarities(self.mine)
            if float(count) / float(len(cities)) >= 0.5:
                self.buddy_list.append([count, traveler, different_cities])
        self.buddy_list.sort(key=lambda item: item[0], reverse=True)
        return self.buddy_list

    def recommend_cities(self, k):
        res = list([])
        # buddy list already sorted by the count of same cities as mine
        for _, _, candidate_cities in self.buddy_list:
            if len(res) == k:
                break
            if candidate_cities:
                # only need some items in candidate
                for c in candidate_cities:
                    if len(res) == k:
                        break
                    res.append(c)
        return res


mine = ["LA", "NYC", "SF", "Seattle"]
others = {
    "Tom": ["LA", "NYC", "SF", "DC"],
    "Peter": ["LA", "HK", "London", "Boston"],
    "Kun": ["LA", "Beijing", "NYC", "SF"],
    "Tina": ["LA", "NYC", "SF", "Seattle", "Shanghai"]
}

recom = BuddyRecommender(mine, others)

for count, buddy, cc in recom.get_buddies():
    print count, buddy, cc

print recom.recommend_cities(3)
