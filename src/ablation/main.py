from sklearn.datasets import load_wine
data = load_wine()
data.target[[10, 80, 140]]

list(data.target_names)