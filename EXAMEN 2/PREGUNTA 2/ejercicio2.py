import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Inicialización de los pesos y sesgos de manera aleatoria (usando np.random.uniform)
        self.weights_input_hidden = np.random.uniform(-0.5, 0.5, (self.input_size, self.hidden_size))
        self.bias_input_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.uniform(-0.5, 0.5, (self.hidden_size, self.output_size))
        self.bias_hidden_output = np.zeros((1, self.output_size))
    
    def activation_function(self, x):
        # Función de activación sigmoide
        return 1 / (1 + np.exp(-x))
    
    def forward_propagation(self, input_data):
        # Propagación hacia adelante
        
        # Capa oculta
        hidden_input = np.dot(input_data, self.weights_input_hidden) + self.bias_input_hidden
        hidden_output = self.activation_function(hidden_input)
        
        # Capa de salida
        output = np.dot(hidden_output, self.weights_hidden_output) + self.bias_hidden_output
        
        return hidden_output, output
    
    def backward_propagation(self, input_data, target_data, hidden_output, output):
        # Retropropagación (propagación hacia atrás)
        
        # Cálculo del error
        error = target_data - output
        
        # Gradiente de la capa de salida
        delta_output = error * output * (1 - output)
        
        # Actualización de pesos y bias entre capa oculta y capa de salida
        self.weights_hidden_output += self.learning_rate * np.dot(hidden_output.T, delta_output)
        self.bias_hidden_output += self.learning_rate * np.sum(delta_output, axis=0, keepdims=True)
        
        # Gradiente de la capa oculta
        delta_hidden = np.dot(delta_output, self.weights_hidden_output.T) * hidden_output * (1 - hidden_output)
        
        # Actualización de pesos y bias entre capa de entrada y capa oculta
        self.weights_input_hidden += self.learning_rate * np.dot(input_data.T, delta_hidden)
        self.bias_input_hidden += self.learning_rate * np.sum(delta_hidden, axis=0, keepdims=True)
    
    def train(self, input_data, target_data, epochs):
        # Entrenamiento de la red neuronal
        for epoch in range(epochs):
            hidden_output, output = self.forward_propagation(input_data)
            self.backward_propagation(input_data, target_data, hidden_output, output)
            
            if epoch % 1000 == 0:
                loss = np.mean(np.abs(target_data - output))
                print(f"Epocas {epoch}, Perdida: {loss}")
    
    def predict(self, input_data):
        # Predicción con la red neuronal entrenada
        _, output = self.forward_propagation(input_data)
        return output

# Ejemplo de uso para clasificación binaria
# Datos de entrada y salida
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

# Crear la red neuronal
input_size = X.shape[1]
hidden_size = 4  # Número de neuronas en la capa oculta
output_size = y.shape[1]
learning_rate = 0.2
epochs = 10000

nn = NeuralNetwork(input_size, hidden_size, output_size, learning_rate)

# Entrenar la red neuronal
nn.train(X, y, epochs)

# Realizar predicciones
predictions = nn.predict(X)
print("\nPredicciones:")
print(predictions)
