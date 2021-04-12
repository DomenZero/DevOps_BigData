'''
You have had AWK homework (3-4), please find a document in a homework Slack thread.
Do all the same AWK tasks using Python.
'''
'''
1.1 What is the most frequent browser (user agent)?
[root@localhost shared-folder]# sudo sudo awk -F"\"" '{print $6}' access.log | awk ' {print $1}' | awk '{if (max < ++c[$1]) {max = c[$1]; browser = $1}} END {print browser, max}'
Mozilla/4.0 43666

1.2 Show number of requests per month for ip 95.108.129.196 (for example: Sep 2016 - 100500 reqs, Oct 2016 - 0 reqs, Nov 2016 - 2 reqs...)
[root@localhost shared-folder]# grep 193.106.31.130 access.log | awk -F[:\ ] '{print $4}' | awk -F[/] '{print $2, $1}' | awk -F' ' '{print $1, "- " $2 " reqs"}' | awk 'BEGIN { count=0;count12=0;count2=0;count3=0;count4=0;count5=0;count6=0;count7=0;count8=0;count9=0;count10=0;count11=0} {if ($1 ~ /Jan/) count++;} {if ($1 ~ /Dec/) count12++;} {if ($1 ~ /Feb/) count2++;} {if ($1 ~ /Mar/) count3++;} {if ($1 ~ /Apr/) count4++;} {if ($1 ~ /May/) count5++;} {if ($1 ~ /Jun/) count6++;} {if ($1 ~ /Jul/) count7++;} {if ($1 ~ /Aug/) count8++;} {if ($1 ~ /Sep/) count9++;} {if ($1 ~ /Oct/) count10++;} {if ($1 ~ /Nov/) count11++;}  END {print "Jun - " count"\n","Feb - " count2"\n","Mar - " count3"\n","Apr - " count4"\n","May - " count5"\n","Jun - " count6"\n","Jul - " count7"\n","Aug - " count8"\n","Sep - " count9"\n","Oct - " count10"\n","Nov - " count11"\n","Dec - " count12"\n"}'

1.3 Show total amount of data which server has provided for each unique ip (i.e. 100500 bytes for 1.2.3.4; 9001 bytes for 5.4.3.2 and so on)
[root@localhost shared-folder]# awk '{ sum_byte[$1] += $10 } END { for (ip in sum_byte) { print ip, sum_byte[ip]} }' access.log
....
'''
import csv
import re
from collections import Counter
from collections import defaultdict

# 1.1 Task
regex = r'\"(\w*)\/|\ (\w{5,})\/+\d'
regex_2 = r"\'(\w+)"
regex_3 = r"\'(.*?)\'"

file_name = "access.log"
with open(file_name) as f:
    with open("list_out.csv", "w", newline='') as file_out:
        for line in f:
            parts = re.findall(regex, line)
            parts_2 = re.findall(regex_2, str(parts))
            parts_3 = re.findall(regex_2, str(parts_2))
            csv.writer(file_out, lineterminator=',').writerow(parts_3)

new_dict = defaultdict(int)

for word in open('list_out.csv').read().split(','):
    new_dict[word] += 1

max = max(new_dict.keys(), key=(lambda k: new_dict[k]))
print(max)
