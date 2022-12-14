import numpy as np
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------------------------------------------------------------
def test_train(X,y):
    X_train = X
    y_train = y
    X_test = X
    y_test = y 
    X_train = X_train.T
    y_train = y_train.reshape(1, y_train.shape[0])
    X_test = X_test.T
    y_test = y_test.reshape(1, y_test.shape[0])
    return [X_train,y_train,X_test,y_test]
#------------------------------------------------------------------------------------------------------------------------------------
def define_structure(X, Y):
    input_unit = X.shape[0] 
    hidden_unit = 2
    output_unit = Y.shape[0] 
    return (input_unit, hidden_unit, output_unit)
#------------------------------------------------------------------------------------------------------------------------------------
def parameters_initialization(input_unit, hidden_unit, output_unit):
    np.random.seed(2) 
    W1 = np.random.randn(hidden_unit, input_unit)*0.01
    b1 = np.zeros((hidden_unit, 1))
    W2 = np.random.randn(output_unit, hidden_unit)*0.01
    b2 = np.zeros((output_unit, 1))
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    return parameters
#------------------------------------------------------------------------------------------------------------------------------------
def sigmoid(z):
    return 1/(1+np.exp(-z))
#------------------------------------------------------------------------------------------------------------------------------------
def forward_propagation(X, parameters):
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    Z1 = np.dot(W1, X) + b1
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = sigmoid(Z2)
    cache = {"Z1": Z1,"A1": A1,"Z2": Z2,"A2": A2}
    return A2, cache
#------------------------------------------------------------------------------------------------------------------------------------
def cross_entropy_cost(A2, Y, parameters):
    m = Y.shape[1] 
    logprobs = np.multiply(np.log(A2), Y) + np.multiply((1-Y), np.log(1 - A2))
    cost = - np.sum(logprobs) / m
    cost = float(np.squeeze(cost))                 
    return cost
#------------------------------------------------------------------------------------------------------------------------------------
def backward_propagation(parameters, cache, X, Y):
    m = X.shape[1]
    W1 = parameters['W1']
    W2 = parameters['W2']
    A1 = cache['A1']
    A2 = cache['A2']
    dZ2 = A2-Y
    dW2 = (1/m) * np.dot(dZ2, A1.T)
    db2 = (1/m) * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = np.multiply(np.dot(W2.T, dZ2), 1 - np.power(A1, 2))
    dW1 = (1/m) * np.dot(dZ1, X.T) 
    db1 = (1/m)*np.sum(dZ1, axis=1, keepdims=True)
    grads = {"dW1": dW1, "db1": db1, "dW2": dW2,"db2": db2}
    return grads
#------------------------------------------------------------------------------------------------------------------------------------
def gradient_descent(parameters, grads, learning_rate = 0.1):
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    dW1 = grads['dW1']
    db1 = grads['db1']
    dW2 = grads['dW2']
    db2 = grads['db2']
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2
    parameters = {"W1": W1, "b1": b1,"W2": W2,"b2": b2}
    return parameters
#------------------------------------------------------------------------------------------------------------------------------------
def neural_network_model(X, Y, hidden_unit, num_iterations = 1000):
    np.random.seed(3)
    input_unit = define_structure(X, Y)[0]
    output_unit = define_structure(X, Y)[2]
    parameters = parameters_initialization(input_unit, hidden_unit, output_unit)
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    for i in range(0, num_iterations):
        A2, cache = forward_propagation(X, parameters)
        cost = cross_entropy_cost(A2, Y, parameters)
        grads = backward_propagation(parameters, cache, X, Y)
        parameters = gradient_descent(parameters, grads)
    return parameters
#------------------------------------------------------------------------------------------------------------------------------------
def prediction(parameters, X):
    A2, cache = forward_propagation(X, parameters)
    predictions = np.round(A2)
    return predictions
#------------------------------------------------------------------------------------------------------------------------------------
def final_plot(parameters,X,Y):
    x = np.arange(-1,5,1)
    b = parameters['b1']
    w1 = parameters['W1']
    a1 = w1[0,0]
    a2 = w1[0,1]
    a3 = w1[1,0]
    a4 = w1[1,1]
    b1 = b[0,0]
    b2 = b[1,0]
    y1 = (-a1/a2)*x + (-b1/a2)
    y2 = (-a3/a4)*x + (-b2/a4)
    plt.scatter(X[:,0],X[:,1],c = Y)
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.show()
#------------------------------------------------------------------------------------------------------------------------------------
X = np.array([[0,0],[1,1],[1,-1],[2,2],[2,-2],[3,3],[3,-3],[2,0],[2.5,0],[3,0]])
y = np.array([[1],[1],[1],[1],[1],[1],[1],[0],[0],[0]])
#------------------------------------------------------------------------------------------------------------------------------------
X_train,y_train,X_test,y_test = test_train(X,y)
(input_unit, hidden_unit, output_unit) = define_structure(X_train, y_train)
parameters = neural_network_model(X_train, y_train, hidden_unit, num_iterations=1000)   
predictions = prediction(parameters, X_train)
print ('Accuracy Train: %d' % float((np.dot(y_train, predictions.T) + np.dot(1 - y_train, 1 - predictions.T))/float(y_train.size)*100) + '%')
predictions = prediction(parameters, X_test)
print ('Accuracy Test: %d' % float((np.dot(y_test, predictions.T) + np.dot(1 - y_test, 1 - predictions.T))/float(y_test.size)*100) + '%')
final_plot(parameters,X,y)
print("parameters:")
print(parameters)
#------------------------------------------------------------------------------------------------------------------------------------
