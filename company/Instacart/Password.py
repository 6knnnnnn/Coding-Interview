# -*- coding: utf-8 -*-

# For this challenge, you will need to parse data from STDIN to find a character in a matrix.
# Below is an example of the input you will receive from STDIN:
#
# PART 1:
#
# [2, 4]
# AFKPU
# BGLQV
# CHMRW
# DINSX
# EJOTY
#
#
# The first line is the [X, Y] coordinates of the character in the matrix ([0, 0] is the bottom
# left character).
# The remaining lines contain a matrix of random characters, with a character located at the
#  coordinates from line 1.
#
# So, in the example above, we're looking for a character at the coordinates [2, 4].
# Moving right 2 spaces, and up 4, we find the character K. So, K is the character.
#
#
# PART 2:
#
# For this challenge, the goal is to construct a password from a series of chunks.
# The chunks will now look like:
#
# 1
# [5, 6]
# RXIBDIBF
# DVMPXTBG
# BMWAERXR
# UPEIJGMW
# YTALDXDH
# JNPMOUEJ
# XDRHCHWG
#
#
# 0
# [0, 1]
# HUTQW3
# NLEVCU
#
#
# You will notice each chunk looks similar to the previous challenge with one addition — the first
# line is the (0-based) index of the password character.
#
# In our example
# – First chunk: password character index 1, character at [5, 6] is I
# – Second chunk: password character index 0, character at [0, 1] is H
#
#
# Once you have processed all of the chunks you have the entire password and should print it to
# STDOUT. In our example the password is HI.
#
# Chunks are separated by empty lines.
#
# Please write a program that reads from STDIN and prints the answer to STDOUT. Use the "Run Tests"
# button to check your solution against the test cases.


def parsePassword(inputs):
    inputs = inputs.split("\n")
    if not inputs:
        return None
    positions = inputs[0]


def parseOneChunk(matrix, x, y):
    lenX = len(matrix)
    line = matrix[lenX-x-1]
    return line[y] if len(line) > y else ""


matrix = """AFKPU
BGLQV
CHMRW
DINSX
EJOTY""".split("\n")
for i in xrange(len(matrix)):
    for j in xrange(len(matrix[i])):
        print i, j, parseOneChunk(matrix, i, j)
