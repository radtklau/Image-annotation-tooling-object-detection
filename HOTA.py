import matplotlib.pyplot as plt


x = [1,2,3,4]
plt.xticks(x)
"""
y = [29.95,38.94,43.51,46.91]
plt.plot(x, y, label = "line 1")

y1 = [18.59,49.96,51.21,56.68]
plt.plot(x, y1, label = "line 2")
"""
#nur detection
y2 = [45.71,51.44,54.42,57.96]
plt.plot(x, y2, label = "Hectometer sign")

y3 = [43.82,62.78,63.69,67.17]
plt.plot(x, y3, label = "Signal screen")

# naming the x axis
plt.xlabel('Iteration')
# naming the y axis
plt.ylabel('Detection accuracy')
 
# giving a title to my graph
#plt.title('Development of CenterTracks detection performance')
plt.legend(loc='lower right',prop={'size': 12})
 
# function to show the plot
plt.show()