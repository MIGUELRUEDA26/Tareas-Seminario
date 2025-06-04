from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

n = 3  # Número de qubits de entrada
oracle_type = "balanceado"  # Prueba también con "constante_0" o "constante_1"

# Crear circuito
qc = QuantumCircuit(n + 1, n)  # n+1 qubits (n entradas + 1 auxiliar), n bits clásicos

# Paso 1: Inicializar el qubit auxiliar en |1⟩
qc.x(n)

# Paso 2: Aplicar Hadamard a todos los qubits
qc.h(range(n + 1))

# Paso 3: Definir el oráculo CORREGIDO
if oracle_type == "constante_0":
    pass
elif oracle_type == "constante_1":
    qc.x(n)
elif oracle_type == "balanceado":
    # Implementación balanceada CORRECTA para n=3
    qc.cz(0, n)  # Condición 1: f(001)=1
    qc.cz(1, n)  # Condición 2: f(010)=1
    # Alternativa: qc.cx(0, n); qc.cx(1, n); qc.cx(2, n)

# Paso 4: Aplicar Hadamard a los qubits de entrada
qc.h(range(n))

# Paso 5: Medir
qc.measure(range(n), range(n))

# Simular
simulator = AerSimulator()
result = simulator.run(qc, shots=1000).result()
counts = result.get_counts()

# Resultados
print("Resultados:", counts)
if len(counts) == 1:
    print("La función es CONSTANTE")
else:
    print("La función es BALANCEADA")

# Visualización
qc.draw("mpl", style="iqp")
plt.show()
plot_histogram(counts)
plt.show()