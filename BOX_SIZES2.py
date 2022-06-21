import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


fig = plt.figure()
ax = fig.add_subplot(111)
#ax.set_xticks([0,1,2,3,4])
ax.set_xticks([100,200,300,400])   
ax.set_xticklabels([1,2,3,4])

it1_cat1_del = Rectangle((61.16,0),77.68,102.15,color = 'darkgreen')
it1_cat1_add = Rectangle((83.92,112.15),32.16,54.13,color = 'forestgreen')
it1_cat1_corr_pre = Rectangle((64.12,286.15),71.77,94.4,color = 'limegreen')#286.15
it1_cat1_corr_post = Rectangle((77,293.07),46,80.57,color = 'springgreen')#

it1_cat2_del = Rectangle((61.9,390.55),76.2,113.81,color = 'firebrick')
it1_cat2_add = Rectangle((74.55,514.36),50.9,83.51,color = 'indianred')
it1_cat2_corr_pre = Rectangle((47.92,669.36),104.17,158.36,color = 'lightcoral') #669.36
it1_cat2_corr_post = Rectangle((58.83,679.91),82.34,137.27,color = 'lightsalmon')

it2_cat1_del = Rectangle((169.4,0),61.19,91.47,color = 'darkgreen')
it2_cat1_add = Rectangle((183.02,112.15),33.96,54.68,color = 'forestgreen')
it2_cat1_corr_pre = Rectangle((171.62,286.15),56.76,79.66,color = 'limegreen')
it2_cat1_corr_post = Rectangle((181.2,293.75),37.6,64.46,color = 'springgreen')

it2_cat2_del = Rectangle((168.83,390.55),62.35,105.9,color = 'firebrick')
it2_cat2_add = Rectangle((177.24,514.36),45.53,72.35,color = 'indianred')
it2_cat2_corr_pre = Rectangle((169.66,669.36),60.69,96.24,color = 'lightcoral')
it2_cat2_corr_post = Rectangle((172.57,671.98),54.87,91.01,color = 'lightsalmon')

it3_cat1_del = Rectangle((280.22,0),39.57,59.11,color = 'darkgreen')
it3_cat1_add = Rectangle((284.63,112.15),30.73,49.78,color = 'forestgreen')
it3_cat1_corr_pre = Rectangle((274.38,286.15),51.24,74.64,color = 'limegreen')#286.15
it3_cat1_corr_post = Rectangle((282.05,293.75),35.9,59.88,color = 'springgreen')#282.05

it3_cat2_del = Rectangle((268.69,390.55),62.63,101.92,color = 'firebrick')
it3_cat2_add = Rectangle((278.61,514.36),42.78,69.46,color = 'indianred')
it3_cat2_corr_pre = Rectangle((272.3,669.36),55.4,86.65,color = 'lightcoral')
it3_cat2_corr_post = Rectangle((275.66,671.98),48.69,78.83,color = 'lightsalmon')

it4_cat1_del = Rectangle((379.28,0),41.51,61.94,color = 'darkgreen')
it4_cat1_add = Rectangle((352,112.15),96.0,164.0,color = 'forestgreen')
it4_cat1_corr_pre = Rectangle((378.5,286.15),42.99,61.15,color = 'limegreen')#
it4_cat1_corr_post = Rectangle((383.16,293.75),33.68,48.6,color = 'springgreen') #!!

it4_cat2_del = Rectangle((378.04,390.55),43.92,67.89,color = 'firebrick')
it4_cat2_add = Rectangle((356.06,514.36),87.88,145.0,color = 'indianred')
it4_cat2_corr_pre = Rectangle((374.46,683.88),51.9,80.17,color = 'lightcoral')
it4_cat2_corr_post = Rectangle((368,669.36),64.0,109.2,color = 'lightsalmon')

ax.add_patch(it1_cat1_del)
ax.add_patch(it1_cat1_add)
ax.add_patch(it1_cat1_corr_pre)
ax.add_patch(it1_cat1_corr_post)

ax.add_patch(it1_cat2_del)
ax.add_patch(it1_cat2_add)
ax.add_patch(it1_cat2_corr_pre)
ax.add_patch(it1_cat2_corr_post)

ax.add_patch(it2_cat1_del)
ax.add_patch(it2_cat1_add)
ax.add_patch(it2_cat1_corr_pre)
ax.add_patch(it2_cat1_corr_post)

ax.add_patch(it2_cat2_del)
ax.add_patch(it2_cat2_add)
ax.add_patch(it2_cat2_corr_pre)
ax.add_patch(it2_cat2_corr_post)

ax.add_patch(it3_cat1_del)
ax.add_patch(it3_cat1_add)
ax.add_patch(it3_cat1_corr_pre)
ax.add_patch(it3_cat1_corr_post)

ax.add_patch(it3_cat2_del)
ax.add_patch(it3_cat2_add)
ax.add_patch(it3_cat2_corr_pre)
ax.add_patch(it3_cat2_corr_post)

ax.add_patch(it4_cat1_del)
ax.add_patch(it4_cat1_add)
ax.add_patch(it4_cat1_corr_pre)
ax.add_patch(it4_cat1_corr_post)

ax.add_patch(it4_cat2_del)
ax.add_patch(it4_cat2_add)
ax.add_patch(it4_cat2_corr_post)
ax.add_patch(it4_cat2_corr_pre)

#plt.autoscale(False)

plt.xlim([0, 500])
plt.ylim([0, 500])
plt.axis('scaled')
plt.xlabel('iteration')
plt.ylabel('height')

plt.show()