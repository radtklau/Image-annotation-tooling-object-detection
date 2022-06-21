import matplotlib.pyplot as plt

x = [1,2,3,4]
plt.xticks(x)
y1 = [0.045,0.012,0.044,0.074]
plt.plot(x, y1, label = "deleted", color = "red")

y2 = [0.28,0.1,0.084,0.0056]
plt.plot(x, y2, label = "added", color = "blue")

y3 = [0.026,0.05,0.047,0.028]
plt.plot(x, y3, label = "adjusted", color = "green")

y3 = [0.351,0.162,0.175,0.1076]
plt.plot(x, y3, label = "GTM score", color = "black")

plt.axhline(y=0.24, color='r', linestyle='--',label='GTM labeling from scratch')
#plt.axhline(y=0.27, color='r', linestyle='--',label='GTM labeling from scratch')
'''
x3 = [1,2,3,4]
y3 = [1.0881,0.32076,0.3395,0.13988]
plt.plot(x3, y3, label = "line 3", color = "orange")
'''
# naming the x axis
plt.xlabel('Iteration')
# naming the y axis
plt.ylabel('Combined modified bounding boxes per image')
 
# giving a title to my graph
#plt.title('Development of avg del, added and corr values per image')
 
plt.legend()
# function to show the plot
plt.show()