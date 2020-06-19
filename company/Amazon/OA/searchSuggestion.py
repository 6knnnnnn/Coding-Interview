def suggestedProducts(products, word, size=3):
    results = []
    products.sort()
    for i in xrange(len(word)):
        prefix = word[:i+1]
        matchedWords = []
        for product in products:
            if len(matchedWords) == size:
                break
            if i > len(product):
                continue
            if product[:i+1] == prefix:
                matchedWords.append(product)
        results.append(matchedWords[:3])
    return results


products = ["mobile","mouse","moneypot","monitor","mousepad"]
searchWord = "mouse"

print suggestedProducts(products, searchWord)


products = ["mobile"]
searchWord = "mob"

print suggestedProducts(products, searchWord)

products = ["bags","baggage","banner","box","cloths"]
searchWord = "bags"
print suggestedProducts(products, searchWord)

