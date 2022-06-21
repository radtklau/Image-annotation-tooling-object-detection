import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
 
N = 4
'''
df = pd.DataFrame(dict(
    cat_1_deleted=[0.0028, 0.0048, 0.02, 0.069],
    cat_1_added=[0.076, 0.056, 0.056, 0.00033],
    cat_1_corrected=[0.0034,0.026,0.028,0.027],
    cat_2_deleted = [0.043, 0.0074, 0.025, 0.005],
    cat_2_added = [0.21, 0.05, 0.029, 0.0053],
    cat_2_corrected = [0.023,0.025,0.019,0.0017]
))
'''
ind = [1,2,3,4] 
cat_1_deleted = np.array([0.0028, 0.0048, 0.02, 0.069])
cat_1_added = np.array([0.076, 0.056, 0.056, 0.00033])
cat_1_corrected = np.array([0.0034,0.026,0.028,0.027])
cat_2_deleted = np.array([0.043, 0.0074, 0.025, 0.005])
cat_2_added = np.array([0.21, 0.05, 0.029, 0.0053])
cat_2_corrected = np.array([0.023,0.025,0.019,0.0017])

width = 0.35       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots()

ax.set_xticks(ind)

ax.bar(ind, cat_1_deleted, width, color='darkgreen', label='cat 1 del')
ax.bar(ind, cat_1_added, width, color='forestgreen', label='cat 1 added',bottom=cat_1_deleted)
ax.bar(ind, cat_1_corrected, width, color='limegreen', label='cat 1 corr',bottom=cat_1_deleted + cat_1_added)
ax.bar(ind, cat_2_deleted, width, color='firebrick', label='cat 2 del',bottom=cat_1_deleted + cat_1_added + cat_1_corrected)
ax.bar(ind, cat_2_added, width, color='indianred',label='cat 2 added', bottom=cat_1_deleted + cat_1_added + cat_1_corrected + cat_2_deleted)
ax.bar(ind, cat_2_corrected, width, color='lightcoral', label='cat 2 corr', bottom=cat_1_deleted + cat_1_added + cat_1_corrected + cat_2_deleted + cat_2_added)

ax.set_ylabel('GTM score')
ax.set_xlabel('Iteration')
ax.set_title('Correction effort required to perfect dataset')
ax.legend()

plt.show()
'''
#df.diff(axis=1).fillna(df).astype(df.dtypes).plot.bar(stacked=True)


cat_1_deleted = (0.0028, 0.0048, 0.02, 0.069)
cat_1_added = (0.076, 0.056, 0.056, 0.00033)
cat_1_corrected = (0.0034,0.026,0.028,0.027)

cat_2_deleted = (0.043, 0.0074, 0.025, 0.005)
cat_2_added = (0.21, 0.05, 0.029, 0.0053)
cat_2_corrected = (0.023,0.025,0.019,0.0017)


width = 0.35 
 
fig = plt.subplots(figsize =(10, 7))
p1 = plt.bar(ind, cat_1_added, width)
p2 = plt.bar(ind, cat_1_deleted, width)
p3 = plt.bar(ind, cat_1_corrected, width)

p4 = plt.bar(ind, cat_2_deleted, width)
p5 = plt.bar(ind, cat_2_added, width)
p6 = plt.bar(ind, cat_2_corrected, width)

plt.ylabel('Contribution')
plt.title('Contribution by the teams')
plt.xticks(ind, ('1', '2', '3', '4'))
plt.yticks(np.arange(0, 0.5, 0.1))
#plt.legend((p1[0], p2[0]), ('cat 1 added', 'cat 1 deleted'))
 
plt.show()
'''