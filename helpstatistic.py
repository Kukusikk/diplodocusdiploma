import psycopg2


# топ 10 стран по приезду в них
from psycopg2 import sql



import matplotlib.pyplot as plt



for_colump=[97000000, 1500000000, 2300000000, 126000000, 500000000,200000000,9000000, 300000000, 5000000]
for_name_colump=['Vkontakte','YouTube','Facebook','Twitter','Instagram','Telegram','Одноклассики','Tumblr','МойМир']

s = [1, 2, 1, 5]
x = range(len(for_colump))
ax = plt.gca()
ax.bar(x, for_colump, align='edge') # align='edge' - выравнивание по границе, а не по центру
ax.set_xticks(x)
ax.set_xticklabels(for_name_colump)
plt.show()