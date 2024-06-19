class Value:
    
    def __init__(self, data, _children=(), _op=''):
        self.data = data  ### 儲存數值或變量的值
        self.grad = 0  ### 初始導數值為0
        self._backward = lambda: None  ### 初始反向傳播函數為空函數
        self._prev = set(_children)  ### 儲存相關的子節點
        self._op = _op  ### 儲存操作符或功能的名稱
    
    ### 加法運算的重載
    def __add__(self, other):
        ### 如果 other 不是 Value 的實例，則通過 Value(other) 將其轉換為 Value
        ### 為了確保 other 變量最終都是以 Value 對象的形式
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
       ### 定義加法操作的反向傳播函數
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        
        return out
    
    ### 乘法運算的重載
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        
        
        def _backward():
        ###self.grad 是用來存儲當前 Value 對象的梯度值，通常在反向傳播過程中，它會累加每個操作對應的損失函數的梯度
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        ### 計算 out 對象相對於損失函數的梯度時，可以通過調用 out._backward() 來執行乘法操作的梯度計算
        out._backward = _backward
        
        return out
    
    ### 指數運算的重載
    def __pow__(self, other):
        assert isinstance(other, (int, float))
        out = Value(self.data**other, (self,), f'**{other}')
        
        ### 定義指數操作的反向傳播函數
        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward
        
        return out
    
    ### ReLU 函數的定義
    def relu(self):
        ### 將負數輸入映射為 0，而將非負數保持不變
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')
        
        ### 定義 ReLU 函數的反向傳播函數
        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        
        return out
    
    ### 反向傳播的實現
    def backward(self):
        topo = []  ### 用來保存計算圖的拓撲序列
        visited = set()  ### 用來標記節點是否已經訪問過
        
        ### 構建計算圖的拓撲序列
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        
        ### 從自身節點開始構建拓撲序列
        build_topo(self)
        
        self.grad = 1  ### 設置最終節點的梯度為1
        for v in reversed(topo):
            v._backward()  ### 執行每個節點的反向傳播函數
    
    ### 負號運算的重載
    def __neg__(self):
        return self * -1
    
    ### 右加法運算的重載
    def __radd__(self, other):
        ### 將當前對象 self 與 other 進行加法運算
        return self + other
    
    ### 減法運算的重載
    def __sub__(self, other):
        return self + (-other)
    
    ### 右減法運算的重載
    def __rsub__(self, other):
        return other + (-self)
    
   ### 右乘法運算的重載
    def __rmul__(self, other):
        return self * other
    
    ### 除法運算的重載
    def __truediv__(self, other):
        return self * other**-1
    
    ### 右除法運算的重載
    def __rtruediv__(self, other):
        return other * self**-1
    
    ### 對象的表示方法
    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
