import numpy as np

class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = np.array(data)
        self.grad = np.zeros(self.data.shape)
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    @property
    def shape(self):
        return self.data.shape
    
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(np.zeros(self.shape) + other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(np.zeros(self.shape) + other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward

        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad

        out._backward = _backward

        return out

    def relu(self):
        out = Value(np.maximum(0, self.data), (self,), 'relu')

        def _backward():
            self.grad += (out.data > 0) * out.grad

        out._backward = _backward

        return out

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
        softmax = exp_data / np.sum(exp_data, axis=1, keepdims=True)
        out = Value(softmax, (self,), 'softmax')

        def _backward():
            s = np.sum(out.grad * softmax, axis=1, keepdims=True)
            self.grad += (out.grad - s) * softmax

        out._backward = _backward

        return out

    def log(self):
        out = Value(np.log(self.data), (self,), 'log')

        def _backward():
            self.grad += out.grad / self.data

        out._backward = _backward

        return out

    def sum(self, axis=None):
        out = Value(np.sum(self.data, axis=axis), (self,), 'SUM')

        def _backward():
            output_shape = np.array(self.data.shape)
            output_shape[axis] = 1
            tile_scaling = self.data.shape // output_shape
            grad = np.reshape(out.grad, output_shape)
            self.grad += np.tile(grad, tile_scaling)

        out._backward = _backward

        return out

    def cross_entropy(self, yb):
        log_probs = self.log()
        zb = yb * log_probs
        outb = zb.sum(axis=1)
        loss = -outb.sum()
        return loss

    def backward(self):
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = 1

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
