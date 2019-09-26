import re
str1 = 'wang皖浙赣safaf@!$@#.,.m,n'
res1 = ''.join(re.findall('[\u4e00-\u9fa5]',str1))
print(res1)
