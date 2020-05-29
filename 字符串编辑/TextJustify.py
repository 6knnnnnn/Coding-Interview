# -*- coding: utf-8 -*-


class LineNode(object):
    def __init__(self, word, maxWidth):
        self.words = list([word])
        self.nonSpaceCount = len(word)
        self.maxWidth = maxWidth

    def addWord(self, word):
        canAddWord = self.nonSpaceCount + len(self.words) + len(word) <= self.maxWidth
        if canAddWord:
            self.words.append(word)
            self.nonSpaceCount += len(word)
        return canAddWord

    def __str__(self):
        return " ".join(self.words)

    def getSpaceModuledByGap(self):
        # assuming more than one word
        return (self.maxWidth - self.nonSpaceCount) % (len(self.words) - 1)

    def getSpaceDiviedByGap(self):
        # assuming more than one word
        return int((self.maxWidth - self.nonSpaceCount) / (len(self.words) - 1))


def fullJustify(words, maxWidth):
    results = list([])
    i = 0
    while i < len(words):
        lineNode = LineNode(words[i], maxWidth)
        j = i + 1
        # add this word to line node if after that the total char len plus one space <= max
        while j < len(words) and lineNode.addWord(words[j]):
            j += 1
        # finish one line, process it
        if len(lineNode.words) == 1 or j == len(words):
            # if last line, j should reach to the end
            wordsWithOneSpace = " ".join(lineNode.words)
            remainedSpaces = " " * (lineNode.maxWidth - len(wordsWithOneSpace))
            lineRes = wordsWithOneSpace + remainedSpaces
        else:
            remainingSpacesCount = lineNode.getSpaceModuledByGap()
            k = 0
            while remainingSpacesCount > 0 and k < len(lineNode.words):
                # extra space for this word (from left to right)
                lineNode.words[k] += " "
                remainingSpacesCount -= 1
                k += 1
            # after assigning one extra space to words of this line, concatenate all those words
            lineRes = (" " * lineNode.getSpaceDiviedByGap()).join(lineNode.words)
        # finish one line
        results.append(lineRes)
        i = j
    return results


text = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"]
maxWidth = 20
print fullJustify(text, maxWidth)
