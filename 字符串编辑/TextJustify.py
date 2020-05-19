# -*- coding: utf-8 -*-


def handle_last_line_or_one_word(lineNode):
    wordsWithSpaces = " ".join(lineNode.words)
    remaingSpaces = " " * (lineNode.maxWidth - len(wordsWithSpaces))
    return wordsWithSpaces + remaingSpaces


def handle_unevenly_spaced_line(lineNode):
    # total spaces = X, gaps = Y
    # Assign each gap with X / Y spaces, X % Y = Z spaces remained
    # From left to right, assign one extra space, decrease Z by 1, until Z = 0
    remainingSpacesCount = lineNode.getTotalSpacesCount() % lineNode.getWordGapsCount()
    res = ""
    for word in lineNode.words[:-1]:
        word += " " * lineNode.getEvenSpacesPerGap()
        if remainingSpacesCount > 0:
            word += " "
            remainingSpacesCount -= 1
        res += word
    return res + lineNode.words[-1]


def handle_evenly_spaced_line(lineNode):
    res = ""
    for word in lineNode.words[:-1]:
        res += word + " " * lineNode.getEvenSpacesPerGap()
    return res + lineNode.words[-1]


class LineNode(object):
    def __init__(self, word, maxWidth):
        self.words = list([word])
        self.totalCharLen = len(word)
        self.maxWidth = maxWidth

    def addWord(self, word):
        self.words.append(word)
        self.totalCharLen += len(word)

    def isLineFull(self):
        return self.maxWidth <= self.totalCharLen + len(self.words) - 1

    def isLineFullWithNewWord(self, word):
        return self.isLineFull() or self.maxWidth <= self.totalCharLen + len(word) + len(self.words)

    def addWordWithDelimiter(self, word):
        new_len = self.totalCharLen + len(self.words) + len(word)
        endIndex = new_len - self.maxWidth + 1
        splitWord = word[:endIndex]
        self.addWord(splitWord + "-")
        return word[endIndex:]

    def canAddNewWord(self, newWord):
        return self.totalCharLen + len(self.words) + len(newWord) <= self.maxWidth

    def isOneWordLine(self):
        return len(self.words) == 1

    def canBeEvenlySpaced(self):
        # assuming has more than one word
        # if self.isOneWordLine(): raise Exception("Only one word")
        return self.getTotalSpacesCount() % self.getWordGapsCount() == 0

    def getTotalSpacesCount(self):
        # max width - total chars of words
        return self.maxWidth - self.totalCharLen

    def getWordGapsCount(self):
        # assuming has more than one word
        # if self.isOneWordLine(): raise Exception("Only one word")
        return len(self.words) - 1

    def getEvenSpacesPerGap(self):
        return self.getTotalSpacesCount() / self.getWordGapsCount()

    def __str__(self):
        return " ".join(self.words)


class Solution(object):
    def fullJustify(self, words, maxWidth):
        def text_justify_single_line(line, isLastLine):
            if line.isOneWordLine() or isLastLine:
                return handle_last_line_or_one_word(line)
            elif line.canBeEvenlySpaced():
                return handle_evenly_spaced_line(line)
            return handle_unevenly_spaced_line(line)

        results = list([])
        i = 0
        while i < len(words):
            lineNode = LineNode(words[i], maxWidth)
            j = i + 1
            while j < len(words) and lineNode.canAddNewWord(words[j]):
                # add this word to line node if after that the total char len plus one space <= max
                lineNode.addWord(words[j])
                j += 1
            # finish one line, process it; if last line, j should reach to the end
            res = text_justify_single_line(lineNode, j == len(words))
            results.append(res)
            i = j
        return results


sol = Solution()
print sol.fullJustify(["This", "is", "justification", "example", "of", "text", "justification."], 16)
