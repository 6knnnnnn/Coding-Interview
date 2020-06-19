class LogRecord(object):
    def __init__(self, ID, content, originalStr):
        self.ID = ID
        self.content = content
        self.str = originalStr

    def __cmp__(self, other):
        if other.content > self.content:
            return -1
        elif other.content == self.content:
            return -1 if other.ID > self.ID else (0 if other.ID == self.ID else 1)

    def __str__(self):
        return self.str


def reorderLogFiles(logs):
    res = []
    if logs:
        letters, digits = [], []
        for log in logs:
            logID, content = log.split(" ", 1)
            record = LogRecord(logID, content, log)
            if 'a' <= content[0] <= 'z':
                # letter case
                letters.append(record)
            elif '0' <= content[0] <= '9':
                digits.append(record)
        # process letter logs, now sorting them
        letters.sort()
        for log in letters: res.append(str(log))
        for log in digits: res.append(str(log))
    return res

logs = ["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
print reorderLogFiles(logs)
