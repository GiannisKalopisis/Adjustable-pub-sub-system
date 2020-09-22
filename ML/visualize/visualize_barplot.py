import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['Batch Size', 'Buffer Memory', 'Linger Ms', 'Max Request Size', 'Message Size', 'Batch Size +\n Buffer Memory', 'Batch Size +\n Linger Ms', 'Batch Size +\n Max Request Size', 'Buffer Memory +\n Linger Ms', 'Linger Ms +\n Max Request Size'] # 
linear = [0.1, 0.1, 0.11, 0.11, 0.07, 0.12, 0.12, 0.11, 0.1, 0.12] 
lasso = [0.1, 0.13, 0.11, 0.11, 0.06, 0.12, 0.11, 0.12, 0.13, 0.12] 
lassolars = [0.12, 0.14, 0.11, 0.11, 0.09, 0.11, 0.11, 0.12, 0.12, 0.11]
cart = [0, 0, 0, 0, 0.01, 0, 0, 0, 0, 0]





x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars
total_width = 0.8

fig, ax = plt.subplots()
rects1 = ax.bar(x - 1*width, linear, width*0.9, align='edge', label='Linear Regression')
rects2 = ax.bar(x + 0*width, lasso, width*0.9, align='edge', label='Lasso Regression')
rects3 = ax.bar(x + 1*width, lassolars, width*0.9, align='edge', label='LassoLARS Regression')
rects4 = ax.bar(x + 2*width, cart, width*0.9, align='edge', label='CART')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Score in %')
ax.set_xlabel('Files')
ax.set_title('Median Absolute Error using test-set data')
# ax.set_title('Explained Variance using test-set data')
ax.set_xticks(x + total_width/4)
ax.set_xticklabels(labels, rotation=0, fontsize=10)
ax.legend(loc='lower center')


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)

fig.tight_layout()

plt.show()
fig.savefig('./predicted_data_plots/MB_sec/MedAE_test_set.png')


#####################
#                   #
#    Records/sec    #
#                   #
#####################

# MAE_lr_cv = 0.12, 0.12, 0.12, 0.12, 0.09, 0.13, 0.13, 0.12, 0.13, 0.12
# MAE_l_cv = 0.12 , 0.12, 0.12, 0.12, 0.14, 0.13, 0.13, 0.12, 0.13 , 0.12
# MAE_ll_cv = 0.12, 0.12, 0.12, 0.12, 0.14, 0.13, 0.13, 0.12, 0.13, 0.12
# MAE_c_cv = 0.01, 0.01, 0.01, 0.01, 0.03, 0, 0, 0, 0, 0

# MSE_lr_cv = 0.02, 0.02, 0.02, 0.05, 0.02, 0.03, 0.02, 0.02, 0.03, 0.02
# MSE_l_cv = 0.02, 0.02, 0.02, 0.02, 0.03, 0.03, 0.02, 0.02, 0.03, 0.02
# MSE_ll_cv = 0.02, 0.02, 0.02, 0.02, 0.03, 0.03, 0.02, 0.02, 0.03, 0.02
# MSE_c_cv = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


# MedAE_lr_cv = 0.11, 0.11, 0.12, 0.11, 0.07, 0.12, 0.12, 0.12, 0.12, 0.11
# MedAE_l_cv = 0.11, 0.12, 0.12, 0.11, 0.13, 0.12, 0.12, 0.12, 0.12, 0.12
# MedAE_ll_cv = 0.11, 0.12, 0.11, 0.11, 0.13, 0.12, 0.12, 0.12, 0.12, 0.12
# MedAE_c_cv = 0, 0, 0, 0, 0.01, 0, 0, 0, 0, 0

###########################################################################

# EV_lr_test = 0.91, 0.93, 0.95, 0.94, 0.95, 0.92, 0.95, 0.94, 0.95, 0.92
# EV_l_test = 0.95, 0.92, 0.95, 0.94, 0.94, 0.93, 0.95, 0.94, 0.92, 0.95
# EV_ll_test = 0.93, 0.89, 0.95, 0.94, 0.91, 0.94, 0.94, 0.94, 0.92, 0.96
# EV_c_test = 1, 1, 1, 1, 0.98, 1, 1, 1, 1, 1

# MAE_lr_test = 0.14, 0.1, 0.11, 0.12, 0.09, 0.12, 0.13, 0.12, 0.11, 0.12
# MAE_l_test = 0.12, 0.13, 0.11, 0.11, 0.09, 0.13, 0.12, 0.13, 0.14, 0.12
# MAE_ll_test = 0.12, 0.14, 0.11, 0.11, 0.1, 0.12, 0.12, 0.12, 0.14, 0.11
# MAE_c_test = 0, 0.01, 0, 0.01, 0.03, 0, 0, 0, 0, 0

# MSE_lr_test = 0.05, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02
# MSE_l_test = 0.02, 0.02, 0.02, 0.01, 0.01, 0.02, 0.02, 0.02, 0.03, 0.02
# MSE_ll_test = 0.02, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.03, 0.01
# MSE_c_test = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


# MedAE_lr_test = 0.1, 0.1, 0.11, 0.11, 0.07, 0.12, 0.12, 0.11, 0.1, 0.12
# MedAE_l_test = 0.1, 0.13, 0.11, 0.11, 0.06, 0.12, 0.11, 0.12, 0.13, 0.12
# MedAE_ll_test = 0.12, 0.14, 0.11, 0.11, 0.09, 0.11, 0.11, 0.12, 0.12, 0.11
# MedAE_c_test = 0, 0, 0, 0, 0.01, 0, 0, 0, 0, 0

###########################################################################
###########################################################################

################
#              #
#    MB/sec    #
#              #
################