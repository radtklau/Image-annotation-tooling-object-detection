import matplotlib.pyplot as plt

x = [1,2,3,4]
plt.xticks(x)
y = [3.1,1.98,1.94,1.3]
plt.plot(x, y, label = "Correction time (CT)")

plt.axhline(y=2.19, color='r', linestyle='--',label='CT when labeling from scratch')

# naming the x axis
plt.xlabel('Iteration')
# naming the y axis
plt.ylabel('Avg corr time per image')
 
# giving a title to my graph
#plt.title('Development of corr time over all iterations')
 
plt.legend()
# function to show the plot
plt.show()