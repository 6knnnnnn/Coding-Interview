def parse_line(line):
    items = line.split(",")
    fields = list([])
    i = 0
    while i < len(items):
        item = str(items[i])
        # an empty string, or a paired double quotes, will be an empty field
        field = ''
        if len(item) != 0 and item != '""':
            field = item
            if item[0] == '"':
                # first char is double quotes, check two cases
                if item[-1] != '"':
                    # there is a ',' in the original field, need to get the next one
                    next_item = items[i+1]
                    if next_item[0] != '"' and next_item[-1] == '"':
                        # so we have a '"Seattle' and 'WA"'
                        field = item[1:]+","+next_item[:-1]
                        i += 1
                else:
                    # a paired item between two double quotes "....."
                    # first replace "" to ", then remove the first and last double quote
                    field = item[1:-1].replace('""','"')
        fields.append(field)
        i += 1

    return "|".join(fields)


inputs = [
'"John ""Brandon"" Smith",john.smith@gmail.com,"","Seattle, WA",  1',
'Jane Roberts,jane.roberts@gmail.com,"San Francisco, CA",2'
    ,'Alice Strong,alice_strong@aaa.com,"San Francisco, CA", 3'
]

for line in inputs:
    print line
    print parse_line(line)
    print "------"
