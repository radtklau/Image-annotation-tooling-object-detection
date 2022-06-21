import matplotlib.pyplot as plt

"""
x = [24.45,44.45,47.36,51.795]
y = [0.351,0.162,0.175,0.1076]
plt.plot(x, y, label = "line 1")
"""
#neu
x = [44.77,57.11,59.06,62.57]
y = [0.351,0.162,0.175,0.1076]
plt.plot(x, y, label = "Relationship GTM score and detection accuracy")

x1 = [44.77,62.57]
y1 = [0.35,0.11]
plt.plot(x1, y1, label = "line 2")
##

"""
x1 = [24.45,51.795]
y1 = [0.350,0.1145]
plt.plot(x1, y1, label = "line 2")
"""
plt.axhline(y=0.24, color='r', linestyle='--',label='GTM when score labeling from scratch')
plt.axvline(x=52.82, ymax = 0.54, color='b',label='hintern',linestyle=':')
# naming the x axis
plt.xlabel('detection accuracy')
# naming the y axis
plt.ylabel('GTM score')
 
# giving a title to my graph
plt.title('Relationship between detection accuracy and ground truth quality')
#plt.legend()
 
# function to show the plot
plt.show()