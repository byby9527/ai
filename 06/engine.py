import numpy as np

class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = np.array(data)  ### 存儲數據
        self.grad = np.zeros(self.data.shape)  ### 存儲梯度，初始化為零
        self._backward = lambda: None  ###反向傳播函數，初始為空函數
        self._prev = set(_children)  ### 該值的前驅節點集合
        self._op = _op  ###操作符，用於構建計算圖

    @property
    def shape(self):
        return self.data.shape  ###返回數據的形狀
    
    ### 運算符重載：加法
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(np.zeros(self.shape) + other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

   ### 運算符重載：乘法
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(np.zeros(self.shape) + other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward

        return out
    
    ###運算符重載：冪次
    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad

        out._backward = _backward

        return out

    ### ReLU 函數
    def relu(self):
        out = Value(np.maximum(0, self.data), (self,), 'relu')

        def _backward():
            self.grad += (out.data > 0) * out.grad

        out._backward = _backward

        return out

   ### 矩陣乘法
    def matmul(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(np.matmul(self.data, other.data), (self, other), 'matmul')

        def _backward():
            self.grad += np.dot(out.grad, other.data.T)
            other.grad += np.dot(self.data.T, out.grad)

        out._backward = _backward

        return out

    
    def softmax(self):
        exp_data = np.exp(self.data)
        ## axis 計算每行的總和
        softmax = exp_data / np.sum(exp_data, axis=1, keepdims=True) ###exp_data 的每個元素分別除以 np.sum對應的元素
        out = Value(softmax, (self,), 'softmax') ### 創建一個新的 Value 物件，用於保存 softmax 的結果和計算圖信息

        def _backward():
           
            
            s = np.sum(out.grad * softmax, axis=1, keepdims=True)  ### 計算得到的 softmax 函數的輸出
            self.grad += (out.grad - s) * softmax ### 更新自身的梯度

        out._backward = _backward

        return out

   
    def log(self):
        out = Value(np.log(self.data), (self,), 'log')

        def _backward():
            self.grad += out.grad / self.data ###計算對數函數的反向傳播梯度，並更新自身梯度

        out._backward = _backward

        return out

   
    def sum(self, axis=None):
        out = Value(np.sum(self.data, axis=axis), (self,), 'SUM')

        def _backward():
            output_shape = np.array(self.data.shape)
            output_shape[axis] = 1
            tile_scaling = self.data.shape // output_shape # 維度比例
            grad = np.reshape(out.grad, output_shape)
            self.grad += np.tile(grad, tile_scaling)

        out._backward = _backward

        return out

    ### 使用了對數概率和真實標籤來計算交叉熵損失，來衡量模型預測值與真實標籤之間的差異
    def cross_entropy(self, yb):
        log_probs = self.log() ### log_probs包含了 self.data 的每個元素的自然對數值
        zb = yb * log_probs ### zb 在真實標籤下的對數概率
        outb = zb.sum(axis=1) ### 每個樣本的總對數概率
        loss = -outb.sum()
        return loss

   
    def backward(self):
        topo = []
        visited = set()

        ### 建立計算圖的拓撲排序
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = 1  ### 初始化梯度為1，從最終結果出發反向傳播

        ### 反向傳播過程
        for v in reversed(topo):
            v._backward()

    
    def __neg__(self):
        return self * -1

    
    def __radd__(self, other):
        return self + other

    
    def __sub__(self, other):
        return self + (-other)

    
    def __rsub__(self, other):
        return other + (-self)

    
    def __rmul__(self, other):
        return self * other

    
    def __truediv__(self, other):
        return self * other**-1

    
    def __rtruediv__(self, other):
        return other * self**-1

    
    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
