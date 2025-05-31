import math
import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def step(x):
    return 1 if x > 0 else 0

def mse_loss(y_true, y_pred):
    return 0.5 * math.pow(y_true - y_pred, 2) 

class Perceptron(object):

    def __init__(self):
        self.w = np.array([0.0, 0.0])
        self.b = 0.0
        self.lr = 0.1 # 学习率
        self.epoch = 100 # 迭代次数

    def train(self, x, y):
        for i in range(self.epoch):
            all_correct = True
            for j in range(len(x)):
                x1, x2 = x[j]
                y_ = step(np.dot(self.w, [x1, x2]) + self.b)
                error = y[j] - y_
                
                if error != 0:
                    all_correct = False
                    self.w[0] += self.lr * error * x1
                    self.w[1] += self.lr * error * x2
                    self.b += self.lr * error

            if all_correct:
                break
    
    def predict(self, x):
        outputs = []
        for x1, x2 in x:
            linear_output = self.w[0] * x1 + self.w[1] * x2 + self.b
            outputs.append(step(linear_output))
        return outputs


class MultiPerceptron(object):
    def __init__(self, n_inputs, n_hidden, n_outputs):
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_outputs = n_outputs

        self.weights = {
            "W1": np.random.randn(n_hidden, n_inputs),  # 隐藏层权重 (2x2)
            "b1": np.random.randn(n_hidden),             # 隐藏层偏置 (2,)
            "W2": np.random.randn(n_outputs, n_hidden),  # 输出层权重 (1x2)
            "b2": np.random.randn(n_outputs)             # 输出层偏置 (1,)
        }
    
    def forward(self, X):
        # 前向传播
        Z1 = np.dot(self.weights["W1"], X) + self.weights["b1"]
        A1 = sigmoid(Z1)
        
        Z2 = np.dot(self.weights["W2"], A1) + self.weights["b2"]
        A2 = sigmoid(Z2)

        return Z1, A1, Z2, A2

    def train(self, X_train, y_train, epochs=10000, learning_rate=0.5):
        for epoch in range(epochs):
            total_loss = 0
            for i in range(len(X_train)):
                x = X_train[i]
                y = y_train[i]

                # 前向传播
                Z1, A1, Z2, A2 = self.forward(x)

                # 计算损失（均方误差）
                loss = 0.5 * (y - A2)**2
                total_loss += loss

                # 反向传播
                dA2 = A2 - y
                dZ2 = dA2 * sigmoid_derivative(Z2)
                
                dW2 = np.outer(dZ2, A1)
                db2 = dZ2
                
                dA1 = np.dot(self.weights["W2"].T, dZ2)
                dZ1 = dA1 * sigmoid_derivative(Z1)
                
                dW1 = np.outer(dZ1, x)
                db1 = dZ1

                # 更新参数
                self.weights["W1"] -= learning_rate * dW1
                self.weights["b1"] -= learning_rate * db1
                self.weights["W2"] -= learning_rate * dW2
                self.weights["b2"] -= learning_rate * db2

            if epoch % 1000 == 0:
                print(f"Epoch {epoch}, Loss: {np.mean(total_loss):.6f}")


    def predict(self, X_test):
        predictions = []
        for x in X_test:
            _, _, _, A2 = self.forward(x)
            predictions.append(round(float(A2)))
        return np.array(predictions)

def single_preptron():
    # 数据集：AND 运算
    X_train = [(0, 0), (1, 0), (1, 1), (0, 1)]
    y_train = [0, 0, 1, 0]

    # 创建并训练模型
    andp = Perceptron()
    andp.train(X_train, y_train)

    # 预测结果
    predictions = andp.predict(X_train)
    print("权重:", andp.w, "偏置:", andp.b)
    print("预测结果:", predictions)

    orp = Perceptron()
    y_train = [0, 1, 1, 1]
    orp.train(X_train, y_train)
    # 预测结果
    predictions = orp.predict(X_train)
    print("权重:", orp.w, "偏置:", orp.b)
    print("预测结果:", predictions)

def multi_preptron():
    # 数据集定义
    X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_train = np.array([0, 1, 1, 0])

    # 创建模型
    mlp = MultiPerceptron(n_inputs=2, n_hidden=2, n_outputs=1)

    # 训练模型
    mlp.train(X_train, y_train, epochs=10000, learning_rate=0.5)

    # 测试模型
    predictions = mlp.predict(X_train)

    # 打印结果
    print("\nFinal Predictions:")
    for i in range(len(X_train)):
        print(f"Input: {X_train[i]} → Predicted Output: {predictions[i]}, True Output: {y_train[i]}")


if __name__ == '__main__':
    multi_preptron()
