import getopt
import sys

ret = getopt.gnu_getopt(sys.argv[1:], "a", ["f"])
print(ret)
