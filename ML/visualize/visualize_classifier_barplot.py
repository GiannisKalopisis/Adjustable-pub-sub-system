import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

# 1) program.py
# 2) data file 
# 3) target (Records/sec, MB/sec etc)
# 4) starting offset (cv or test data)
# 5) step
# 6) title
# 7) path and name

labels = ['Batch Size', 'Buffer Memory', 'Linger Ms', 'Max Request Size', 'Message Size', 'Batch Size +\n Buffer Memory', 'Batch Size +\n Linger Ms', 'Batch Size +\n Max Request Size', 'Buffer Memory +\n Linger Ms', 'Linger Ms +\n Max Request Size'] 

bucket_2 = []
bucket_3 = []
bucket_5 = []
bucket_7 = []
bucket_10 = []

if len(sys.argv) < 7:
    print("Not enough arguments. Program needs 7 arguments, but you gave {}.".format(len(sys.argv)))
    sys.exit(1)

target = sys.argv[2]
offset = int(sys.argv[3])
step = int(sys.argv[4])
title = sys.argv[5]
save_path = sys.argv[6]

data = pd.read_csv(sys.argv[1], sep='\t', header=0, encoding='utf-8')[target].to_numpy()

# bucket 2
i = offset
while i < len(data):
    bucket_2.append(round(data[i], 2))
    i = i + step
print(bucket_2)

# bucket 3
i = offset + 3*1
while i < len(data):
    bucket_3.append(round(data[i], 2))
    i = i + step
print(bucket_3)

# bucket 5
i = offset + 3*2
while i < len(data):
    bucket_5.append(round(data[i], 2))
    i = i + step
print(bucket_5)

# bucket 7
i = offset + 3*3
while i < len(data):
    bucket_7.append(round(data[i], 2))
    i = i + step
print(bucket_7)

# bucket 10
i = offset + 3*4
while i < len(data):
    bucket_10.append(round(data[i], 2))
    i = i + step
print(bucket_10)



x = np.arange(len(labels))  # the label locations
width = 0.18  # the width of the bars
total_width = 1.0

fig, ax = plt.subplots()
rects1 = ax.bar(x - 1*width, bucket_2, width*0.9, align='center', label='2 Buckets')
rects2 = ax.bar(x - 0*width, bucket_3, width*0.9, align='center', label='3 Buckets')
rects3 = ax.bar(x + 1*width, bucket_5, width*0.9, align='center', label='5 Buckets')
rects4 = ax.bar(x + 2*width, bucket_7, width*0.9, align='center', label='7 Buckets')
rects5 = ax.bar(x + 3*width, bucket_10, width*0.9, align='center', label='10 Buckets')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Value of parameter Gamma')
ax.set_xlabel('Files')
ax.set_title(title, fontsize=15)
# ax.set_title('Explained Variance using test-set data')
ax.set_xticks(x + total_width/5)
ax.set_xticklabels(labels, rotation=0, fontsize=9)
ax.legend(loc='best')


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=90, weight='bold', fontsize=8) #  


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
autolabel(rects5)

fig.tight_layout()

plt.show()
fig.savefig(save_path)


