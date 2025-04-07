import tkinter as tk
from tkinter import ttk, messagebox

# Representasi graf berbobot (node: [(tetangga, bobot)])
graph = {
    "Pintu Gerbang Depan": [("Pasca Hukum", 2)],
    "Pasca Hukum": [("Pintu Gerbang Depan", 2), ("MAKSI (Ged C)", 3), ("Gedung F", 5)],
    "MAKSI (Ged C)": [("Pasca Hukum", 3), ("Ged. B", 2)],
    "Ged. B": [("MAKSI (Ged C)", 2), ("Ged. A", 4)],
    "Ged. A": [("Ged. B", 4), ("Masjid UNIB", 2)],
    "Masjid UNIB": [("Ged. A", 2)],
    "Gedung F": [("Pasca Hukum", 5), ("Lab. Hukum", 3), ("Ged. I", 4), ("Ged. J", 6), ("Dekanat Pertanian", 5)],
    "Lab. Hukum": [("Gedung F", 3)],
    "Ged. I": [("Gedung F", 4), ("Ged. MM", 2)],
    "Ged. MM": [("Ged. I", 2), ("Ged. MPP", 3)],
    "Ged. MPP": [("Ged. MM", 3), ("Ged. UPT B. Inggris", 4)],
    "Ged. J": [("Gedung F", 6), ("Ged. UPT B. Inggris", 2)],
    "Ged. UPT B. Inggris": [("Ged. J", 2), ("REKTORAT", 5)],
    "Dekanat Pertanian": [("Gedung F", 5), ("Ged. T", 3)],
    "Ged. T": [("Dekanat Pertanian", 3), ("Ged. V", 2)],
    "Ged. V": [("Ged. T", 2), ("Ged. Renper", 4), ("REKTORAT", 5)],
    "Ged. Renper": [("Ged. V", 4), ("Lab. Agro", 3)],
    "Lab. Agro": [("Ged. Renper", 3), ("Ged. Basic Sains", 5)],
    "Ged. Basic Sains": [("Lab. Agro", 5), ("GKB I", 2), ("Dekanat MIPA", 4)],
    "UPT Puskom": [("Ged. V", 4), ("GKB I", 2)],
    "REKTORAT": [("Ged. UPT B. Inggris", 5), ("Ged. V", 5), ("Dekanat FISIP", 3)],
    "Dekanat FISIP": [("REKTORAT", 3), ("Pintu Gerbang", 2), ("GKB II", 3)],
    "Pintu Gerbang": [("Dekanat FISIP", 2), ("Dekanat Teknik", 4)],
    "Dekanat Teknik": [("Pintu Gerbang", 4), ("Gedung Serba Guna (GSG)", 3)],
    "Gedung Serba Guna (GSG)": [("Dekanat Teknik", 3), ("Stadion Olahraga", 4), ("GKB III", 2), ("Dekanat FKIP", 5)],
    "GKB I": [("UPT Puskom", 2), ("GKB II", 3), ("Ged. Basic Sains", 2)],
    "GKB II": [("GKB I", 3), ("Dekanat FKIP", 2), ("Dekanat FISIP", 3)],
    "Dekanat FKIP": [("GKB II", 2), ("Gedung Serba Guna (GSG)", 5)],
    "GKB V": [("PKM", 3), ("PSPD", 4)],
    "Stadion Olahraga": [("GKB III", 2), ("PSPD", 5)],
    "Dekanat MIPA": [("Ged. Basic Sains", 4)],
    "PSPD": [("Stadion Olahraga", 5), ("GKB V", 3)],
    "GKB III": [("Gedung Serba Guna (GSG)", 2), ("Stadion Olahraga", 4)],
    "PKM": [("GKB V", 3), ("Ged. MPP", 4)],
}

def bellman_ford(graph, start, goal):
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    predecessors[neighbor] = node

    for node in graph:
        for neighbor, weight in graph[node]:
            if distances[node] + weight < distances[neighbor]:
                return None, "Terdapat siklus negatif di graf!"

    path = []
    current = goal
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]

    if distances[goal] == float('inf'):
        return None, "Tidak ada jalur dari {} ke {}".format(start, goal)

    return path, distances[goal]

def find_path():
    start_node = start_combobox.get()
    goal_node = goal_combobox.get()

    if start_node not in graph or goal_node not in graph:
        messagebox.showerror("Error", "Titik awal atau tujuan tidak ditemukan dalam graf.")
        return

    path, cost = bellman_ford(graph, start_node, goal_node)

    if path:
        result_label.config(text=f"Jalur: {' -> '.join(path)}\nTotal Bobot: {cost}")
    else:
        result_label.config(text=cost)

root = tk.Tk()
root.title("Pencarian Jalur Terpendek - Bellman-Ford")
root.geometry("450x400")
root.configure(bg="#aee9ff")

places = list(graph.keys())


tk.Label(root, text="Pilih Titik Awal:", fg="black", bg="#aee9ff", font=("Times New Roman", 12)).pack(pady=5)
start_combobox = ttk.Combobox(root, values=places, state="readonly")
start_combobox.pack(pady=5)

tk.Label(root, text="Pilih Tujuan:", fg="black", bg="#aee9ff", font=("Times New Roman", 12)).pack(pady=5)
goal_combobox = ttk.Combobox(root, values=places, state="readonly")
goal_combobox.pack(pady=5)

tk.Button(root, text="Cari Jalur Terpendek", command=find_path, bg="#007acc", fg="white", font=("Times New Roman", 12)).pack(pady=5)

result_label = tk.Label(root, text="", fg="black", bg="#aee9ff", font=("Arial", 12), wraplength=400, justify="left")
result_label.pack()

root.mainloop()
