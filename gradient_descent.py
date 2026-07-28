import numpy as np

X = [[1 ,6], [2, 5], [8, 7], [9, 8], [3, 4]]
y= [0, 0, 1, 1, 0]
weights = [0.1, 0.1]
bias = 0.0
learning_rate = 0.01

def sigmoid(z):
    return 1/(1+np.exp(-z))

for epoch in range(1000):
    for i in range(len(X)):
        z = np.dot(weights, X[i]) + bias
        prediction = sigmoid(z)
        error = prediction - y[i]

        for j in range(len(weights)):
            weights[j] = weights[j] - learning_rate*error*X[i][j]
        bias = bias - learning_rate*error

print(weights, bias)
z = np.dot(weights, [8, 7]) + bias
print(sigmoid(z))

