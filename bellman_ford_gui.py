import tkinter as tk  # GUI utama
from tkinter import ttk, messagebox  # Widget dan pesan pop-up
import folium  # Buat dan tampilkan peta
import webbrowser  # Buka file HTML di browser
import os  # Akses file system (path)
import openrouteservice  # API rute dari OpenRouteService
from datetime import datetime  # Ambil waktu saat ini

# Kunci API dari OpenRouteService
ORS_API_KEY = "5b3ce3597851110001cf624843e7043993ae43cd8330f3d91dab22c4"

# Koordinat lokasi penting di kampus UNIB
coordinates = {
    "Gerbang Depan": [-3.7597051, 102.2677983],
    "Gerbang Keluar Depan": [-3.759170,102.266890],
    "Pasca Hukum": [-3.7602660, 102.2686734],
    "MAKSI (Ged C)": [-3.7590706, 102.2679177],
    "Ged. B": [-3.7593362, 102.2692196],
    "Ged. A": [-3.7592326, 102.2701266],
    "Masjid Darul Ulum": [-3.7572782, 102.2675868],
    "Gedung F": [-3.7617198, 102.2686238],
    "Lab. Hukum": [-3.7605831, 102.2684417],
    "Ged. I": [-3.7603011, 102.2697707],
    "Ged. MM": [-3.7611429, 102.2699081],
    "Ged. MPP": [-3.7614596, 102.2717675],
    "Ged. J": [-3.7607740, 102.2703630],
    "Ged. UPT B. Inggris": [-3.7607740, 102.2703630],
    "Dekanat Pertanian": [-3.7593362, 102.2692196],
    "Ged. T": [-3.7580992, 102.2719195],
    "Ged. V": [-3.7571162, 102.2728366],
    "Ged. Renper": [-3.7570165, 102.2727136],
    "Lab. Agro": [-3.7566360, 102.2757012],
    "Ged. Basic Sains": [-3.7560288, 102.2747136],
    "GKB I": [-3.7568032, 102.2737209],
    "Dekanat MIPA": [-3.7560288, 102.2747136],
    "UPT Puskom": [-3.7584458, 102.2730644],
    "Rektorat": [-3.7590495, 102.2723146],
    "Gerbang Rektorat": [-3.760548, 102.272627],
    "Dekanat FISIP": [-3.7590310, 102.2741732],
    "Gerbang Belakang": [-3.7596149, 102.2752156],
    "Gerbang Keluar Belakang": [-3.759388, 102.276225],
    "Dekanat Teknik": [-3.7584642, 102.2767009],
    "Gedung Serba Guna (GSG)": [-3.7575361, 102.2765579],
    "Stadion Olahraga": [-3.757130,102.277950],
    "GKB II": [-3.7578575, 102.2740375],
    "Dekanat FKIP": [-3.7575341, 102.2750444],
    "GKB III": [-3.7560850, 102.2766449],
    "Kedokteran": [-3.7551337, 102.2780320],
    "PSPD": [-3.7553463, 102.2765021],
    "PKM": [-3.7585034, 102.2750154],
    "GKB V": [-3.755526, 102.276445],
    "CZAL": [-3.756803, 102.271345],
    "LPTIK": [-3.758394,102.275057]
}
# Representasi graf lokasi (node, jarak dalam meter dan waktu tempuh dalam detik)
graph = {
    "Gerbang Depan": [("Pasca Hukum", {"jarak": 200, "waktu": 120}),("MAKSI (Ged C)", {"jarak": 300, "waktu": 180})],
    "Gerbang Keluar Depan": [("Pasca Hukum", {"jarak": 200, "waktu": 120}),("Gerbang Depan", {"jarak": 200, "waktu": 120}),("MAKSI (Ged C)", {"jarak": 300, "waktu": 180})],
    "Pasca Hukum": [("Gerbang Depan", {"jarak": 200, "waktu": 120}), ("MAKSI (Ged C)", {"jarak": 300, "waktu": 180}), ("Gedung F", {"jarak": 500, "waktu": 300})],
    "MAKSI (Ged C)": [("Pasca Hukum", {"jarak": 300, "waktu": 180}), ("Ged. B", {"jarak": 200, "waktu": 120})],
    "Ged. B": [("MAKSI (Ged C)", {"jarak": 200, "waktu": 120}), ("Ged. A", {"jarak": 400, "waktu": 240})],
    "Ged. A": [("Ged. B", {"jarak": 400, "waktu": 240}), ("Masjid Darul Ulum", {"jarak": 200, "waktu": 120})],
    "Masjid Darul Ulum": [("Ged. A", {"jarak": 200, "waktu": 120})],
    "Gedung F": [("Pasca Hukum", {"jarak": 500, "waktu": 300}), ("Lab. Hukum", {"jarak": 300, "waktu": 180}), ("Ged. I", {"jarak": 400, "waktu": 240}), ("Ged. J", {"jarak": 600, "waktu": 360}), ("Dekanat Pertanian", {"jarak": 500, "waktu": 300})],
    "Lab. Hukum": [("Gedung F", {"jarak": 300, "waktu": 180})],
    "Ged. I": [("Gedung F", {"jarak": 400, "waktu": 240}), ("Ged. MM", {"jarak": 200, "waktu": 120})],
    "Ged. MM": [("Ged. I", {"jarak": 200, "waktu": 120}), ("Ged. MPP", {"jarak": 300, "waktu": 180})],
    "Ged. MPP": [("Ged. MM", {"jarak": 300, "waktu": 180}), ("Ged. UPT B. Inggris", {"jarak": 400, "waktu": 240})],
    "Ged. J": [("Gedung F", {"jarak": 600, "waktu": 360}), ("Ged. UPT B. Inggris", {"jarak": 200, "waktu": 120})],
    "Ged. UPT B. Inggris": [("Ged. J", {"jarak": 200, "waktu": 120}), ("Rektorat", {"jarak": 500, "waktu": 300})],
    "Dekanat Pertanian": [("Gedung F", {"jarak": 500, "waktu": 300}), ("Ged. T", {"jarak": 300, "waktu": 180})],
    "Ged. T": [("Dekanat Pertanian", {"jarak": 300, "waktu": 180}), ("Ged. V", {"jarak": 200, "waktu": 120})],
    "Ged. V": [("Ged. T", {"jarak": 200, "waktu": 120}), ("Ged. Renper", {"jarak": 400, "waktu": 240}), ("Rektorat", {"jarak": 500, "waktu": 300}), ("CZAL", {"jarak": 300, "waktu": 200})],
    "Ged. Renper": [("Ged. V", {"jarak": 400, "waktu": 240}), ("Lab. Agro", {"jarak": 300, "waktu": 180})],
    "Lab. Agro": [("Ged. Renper", {"jarak": 300, "waktu": 180}), ("Ged. Basic Sains", {"jarak": 500, "waktu": 300})],
    "Ged. Basic Sains": [("Lab. Agro", {"jarak": 500, "waktu": 300}), ("GKB I", {"jarak": 200, "waktu": 120}), ("Dekanat MIPA", {"jarak": 400, "waktu": 240})],
    "UPT Puskom": [("Ged. V", {"jarak": 400, "waktu": 240}), ("GKB I", {"jarak": 200, "waktu": 120})],
    "Rektorat": [("Ged. UPT B. Inggris", {"jarak": 500, "waktu": 300}), ("Ged. V", {"jarak": 500, "waktu": 300}), ("Dekanat FISIP", {"jarak": 300, "waktu": 180}), ("Gerbang Rektorat", {"jarak": 50, "waktu": 200})],
    "Gerbang Rektorat": [("Rektorat", {"jarak": 50, "waktu": 200})],  # Sudah dua arah sekarang
    "Dekanat FISIP": [("Rektorat", {"jarak": 300, "waktu": 180}), ("Gerbang Belakang", {"jarak": 200, "waktu": 120}), ("GKB II", {"jarak": 300, "waktu": 180}),("LPTIK", {"jarak": 300, "waktu": 180})],
    "Gerbang Belakang": [("Dekanat FISIP", {"jarak": 200, "waktu": 120}), ("Dekanat Teknik", {"jarak": 400, "waktu": 240})],
    "Gerbang Keluar Belakang": [("Dekanat Teknik", {"jarak": 100, "waktu": 200})],
    "Dekanat Teknik": [("Gerbang Belakang", {"jarak": 400, "waktu": 240}), ("Gedung Serba Guna (GSG)", {"jarak": 300, "waktu": 180}), ("Gerbang Keluar Belakang", {"jarak": 100, "waktu": 200})],
    "Gedung Serba Guna (GSG)": [("Dekanat Teknik", {"jarak": 300, "waktu": 180}), ("Stadion Olahraga", {"jarak": 400, "waktu": 240}), ("GKB III", {"jarak": 200, "waktu": 120}), ("Dekanat FKIP", {"jarak": 500, "waktu": 300}),("LPTIK", {"jarak": 300, "waktu": 200})],
    "GKB I": [("UPT Puskom", {"jarak": 200, "waktu": 120}), ("GKB II", {"jarak": 300, "waktu": 180}), ("Ged. Basic Sains", {"jarak": 200, "waktu": 120}),("Ged. Basic Sains", {"jarak": 200, "waktu": 120}), ],
    "GKB II": [("GKB I", {"jarak": 300, "waktu": 180}), ("Dekanat FKIP", {"jarak": 200, "waktu": 120}), ("Dekanat FISIP", {"jarak": 300, "waktu": 180})],
    "Dekanat FKIP": [("GKB II", {"jarak": 200, "waktu": 120}), ("Gedung Serba Guna (GSG)", {"jarak": 500, "waktu": 300}), ("LPTIK", {"jarak": 300, "waktu": 180})],
    "GKB V": [("PKM", {"jarak": 300, "waktu": 180}), ("PSPD", {"jarak": 400, "waktu": 240}), ("Kedokteran", {"jarak": 250, "waktu": 120}),("GKB III", {"jarak": 150, "waktu": 100})],
    "Stadion Olahraga": [("GKB III", {"jarak": 200, "waktu": 120}), ("PSPD", {"jarak": 500, "waktu": 300})],
    "Dekanat MIPA": [("Ged. Basic Sains", {"jarak": 400, "waktu": 240}), ("CZAL", {"jarak": 500, "waktu": 280}), ("LPTIK", {"jarak": 200, "waktu": 120}),("Ged. Basic Sains", {"jarak": 200, "waktu": 120})],
    "PSPD": [("Stadion Olahraga", {"jarak": 500, "waktu": 300}), ("GKB V", {"jarak": 300, "waktu": 180})],
    "GKB III": [("Gedung Serba Guna (GSG)", {"jarak": 200, "waktu": 120}), ("Stadion Olahraga", {"jarak": 400, "waktu": 240}),("GKB V", {"jarak": 150, "waktu": 100}),("PKM", {"jarak": 200, "waktu": 120})],
    "PKM": [("GKB V", {"jarak": 300, "waktu": 180}), ("Ged. MPP", {"jarak": 400, "waktu": 240}),("Dekanat MIPA", {"jarak": 250, "waktu": 150})],
    "Kedokteran": [("GKB V", {"jarak": 250, "waktu": 120}), ("Dekanat FKIP", {"jarak": 350, "waktu": 180})],
    "CZAL": [("Ged. V", {"jarak": 300, "waktu": 200}),("Dekanat MIPA", {"jarak": 500, "waktu": 280})],
    "LPTIK" : [("Gedung Serba Guna (GSG)", {"jarak": 300, "waktu": 200}),("Dekanat FKIP", {"jarak": 200, "waktu": 120}),("Dekanat FISIP", {"jarak": 300, "waktu": 180})]
}


def get_modified_graph():
    # Ambil waktu dan hari saat ini
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()

    # Salin isi graph asli ke graph yang akan dimodifikasi
    modified = {node: list(neighbors) for node, neighbors in graph.items()}

    # Set berisi simpul-simpul (gerbang) yang akan dihapus dari graf
    to_remove = set()

    # Jika waktu saat ini setelah pukul 16.00 (4 sore), beberapa gerbang dianggap tutup
    if hour >= 16:
        to_remove.add("Gerbang Depan")
        to_remove.add("Gerbang Keluar Depan")
        to_remove.add("Gerbang Keluar Belakang")
        to_remove.add("Gerbang Rektorat")

    # Jika waktu sebelum jam 6 pagi, tambahkan lebih banyak gerbang yang ditutup
    if hour <= 5:
        to_remove.add("Gerbang Depan")
        to_remove.add("Gerbang Keluar Depan")
        to_remove.add("Gerbang Keluar Belakang")
        to_remove.add("Gerbang Rektorat")
        to_remove.add("Gerbang Belakang")

    # Jika sudah lewat jam 10 malam, Gerbang Belakang juga ditutup
    if hour >= 22:
        to_remove.add("Gerbang Belakang")

    # Jika hari Sabtu (5) atau Minggu (6), beberapa gerbang juga ditutup
    if weekday >= 5:
        to_remove.add("Gerbang Depan")
        to_remove.add("Gerbang Keluar Depan")
        to_remove.add("Gerbang Keluar Belakang")
        to_remove.add("Gerbang Rektorat")

    # Hapus simpul-simpul gerbang dari graf yang dimodifikasi
    for node in to_remove:
        modified.pop(node, None)

    # Hapus koneksi (edge) ke simpul-simpul gerbang yang ditutup
    for node in modified:
        modified[node] = [edge for edge in modified[node] if edge[0] not in to_remove]

    # Kembalikan graf yang sudah dimodifikasi
    return modified


# Fungsi Bellman-Ford untuk mencari jalur tercepat (berdasarkan waktu tempuh)
def bellman_ford(graph, start, goal, weight_type="waktu"):
    distance = {node: float('inf') for node in graph}
    predecessor = {node: None for node in graph}
    distance[start] = 0

# Melakukan relaksasi semua edge sebanyak (jumlah simpul - 1) kali
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, attr in graph[node]:
                # Ambil bobot berdasarkan jenis waktu tempuh (misalnya waktu berkendara)
                weight = attr.get(weight_type, float('inf'))
                # Jika ditemukan jalur yang lebih pendek, perbarui jarak dan simpul pendahulu
                if distance[node] + weight < distance[neighbor]:
                    distance[neighbor] = distance[node] + weight
                    predecessor[neighbor] = node
    # Bangun jalur dari tujuan ke awal dengan mengikuti simpul pendahulu
    path = []
    current = goal
    while current is not None:
        path.insert(0, current)
        current = predecessor[current]
    # Jika simpul awal bukan titik pertama dalam jalur, artinya tidak ada jalur yang valid
    if path[0] != start:
        return float("inf"), []
    # Kembalikan jarak total dari start ke goal dan urutan jalur
    return distance[goal], path

# --- Fungsi visualisasi berdasarkan lintasan Bellman-Ford ---
def show_map_from_path(path):
    # Jika path kosong, tidak ada yang ditampilkan
    if not path:
        return None

    # Ambil koordinat dari setiap titik pada path
    route_coords = [coordinates[node] for node in path]

    # Buat objek peta dengan posisi awal sebagai titik fokus
    m = folium.Map(location=route_coords[0], zoom_start=17)

    # Tambahkan marker untuk titik awal (hijau) dan akhir (merah)
    folium.Marker(location=route_coords[0], popup="Awal", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(location=route_coords[-1], popup="Tujuan", icon=folium.Icon(color="red")).add_to(m)

    # Gambar garis (polyline) untuk menunjukkan jalur
    folium.PolyLine(locations=route_coords, color="blue", weight=5).add_to(m)

    # Simpan peta ke file HTML dan buka di browser
    m.save("jalur_terpendek.html")
    webbrowser.open("file://" + os.path.abspath("jalur_terpendek.html"))

def ambil_info_kendaraan(path, graph):
    # Ambil informasi kendaraan yang diperbolehkan untuk tiap segmen jalur
    kendaraan_set = set()
    for i in range(len(path) - 1):
        for neighbor, attr in graph[path[i]]:
            if neighbor == path[i + 1]:
                # Tambahkan jenis kendaraan dari edge ke dalam set
                kendaraan_set.update(attr.get("kendaraan", []))
                break
    return kendaraan_set

def show_map_with_ors(path, mode_kendaraan):
    # Jika path kosong, tidak ada yang ditampilkan
    if not path:
        return None

    # Buat client OpenRouteService
    client = openrouteservice.Client(key=ORS_API_KEY)

    # Konversi nama kendaraan lokal ke profile ORS
    profile_map = {
        "Mobil": "driving-car",
        "Motor": "cycling-regular",
        "Jalan Kaki": "foot-walking"
    }

    profile = profile_map.get(mode_kendaraan, "foot-walking")

    try:
        # Ambil koordinat awal dan akhir dari path
        start = coordinates[path[0]]
        end = coordinates[path[-1]]

        # Request rute ke ORS
        route = client.directions(
            coordinates=[start[::-1], end[::-1]],  # ORS pakai format [lng, lat]
            profile=profile,
            format='geojson'
        )

        # Ambil geometri rute dan durasi perjalanan
        geometry = route['features'][0]['geometry']['coordinates']
        duration = route['features'][0]['properties']['summary']['duration']

        # Buat peta dengan titik awal sebagai fokus
        m = folium.Map(location=start, zoom_start=17)
        folium.Marker(location=start, popup="Awal", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(location=end, popup="Tujuan", icon=folium.Icon(color="red")).add_to(m)

        # Gambar garis rute berdasarkan koordinat dari ORS
        folium.PolyLine(locations=[(lat, lng) for lng, lat in geometry], color="blue", weight=5).add_to(m)

        # Simpan dan buka peta
        m.save("jalur_terpendek.html")
        webbrowser.open("file://" + os.path.abspath("jalur_terpendek.html"))

        return duration

    except Exception as e:
        # Tampilkan error jika gagal mendapatkan peta
        messagebox.showerror("Error saat menggambar peta", str(e))
        return None

def find_path():
    # Ambil input dari user (start, goal, kendaraan)
    start = start_combobox.get()
    goal = goal_combobox.get()
    kendaraan = kendaraan_combobox.get()

    # Validasi input
    if not start or not goal or not kendaraan:
        messagebox.showwarning("Input tidak lengkap", "Silakan pilih titik awal, tujuan, dan kendaraan.")
        return

    if start == goal:
        messagebox.showinfo("Info", "Titik awal dan tujuan tidak boleh sama.")
        return

    if start not in coordinates or goal not in coordinates:
        messagebox.showerror("Error", "Koordinat tidak ditemukan.")
        return

    # Dapatkan graf yang sudah dimodifikasi sesuai waktu/hari
    graph_now = get_modified_graph()

    # Jalankan algoritma Bellman-Ford
    cost, path = bellman_ford(graph_now, start, goal)

    if not path:
        messagebox.showerror("Tidak ditemukan", "Tidak ada jalur dari titik awal ke tujuan.")
        return

    # Dapatkan estimasi waktu tempuh menggunakan ORS
    waktu_detik = show_map_with_ors(path, kendaraan)
    if waktu_detik is None:
        return

    waktu_menit = round(waktu_detik / 60)

    # Ambil info kendaraan yang diperbolehkan pada jalur
    kendaraan_set = ambil_info_kendaraan(path, graph_now)
    kendaraan_text = ", ".join(sorted(kendaraan_set)) if kendaraan_set else "Tidak diketahui"

    # Format hasil ke label GUI
    result_text = f"Jalur tercepat dari '{start}' ke '{goal}' dengan {kendaraan}:\n\n"
    result_text += f"Estimasi waktu tempuh: {waktu_menit} menit\n"
    result_text += "Rute:\n" + " → ".join(path)

    # Tampilkan hasil
    result_label.config(text=result_text)

def update_combobox_values():
    # Perbarui isi combobox berdasarkan graf saat ini (yang aktif)
    modified = get_modified_graph()
    filtered_places = list(modified.keys())
    start_combobox['values'] = filtered_places
    goal_combobox['values'] = filtered_places

def reset_result(*args):
    # Reset hasil saat ada perubahan input
    result_label.config(text="")


# GUI
root = tk.Tk()
root.title("Jalur Terpendek UNIB - Bellman-Ford")
root.geometry("800x580")
root.configure(bg="#f1f9f9")  # Soft background

# ===== HEADER =====
header = tk.Label(
    root,
    text="🚀 Pencari Jalur Terpendek - UNIB",
    font=("Segoe UI", 20, "bold"),
    bg="#f1f9f9",
    fg="#2b6777"
)
header.pack(pady=(30, 15))

# ===== KARTU UTAMA / FRAME UTAMA =====
main_frame = tk.Frame(root, bg="#ffffff", bd=0, relief="flat", padx=30, pady=30)
main_frame.pack(pady=10, padx=20, fill="both", expand=False)

# Gaya label dan combobox
label_style = ("Segoe UI", 11)
combo_style = ("Segoe UI", 10)

def make_label(text, row):
    return tk.Label(main_frame, text=text, bg="#ffffff", font=label_style, anchor="w")

# === Titik Awal ===
make_label("Titik Awal:", 0).grid(row=0, column=0, sticky="w", pady=8)
start_combobox = ttk.Combobox(main_frame, state="readonly", width=50, font=combo_style)
start_combobox.grid(row=0, column=1, pady=8)
start_combobox.bind("<<ComboboxSelected>>", reset_result)

# === Titik Tujuan ===
make_label("Tujuan:", 1).grid(row=1, column=0, sticky="w", pady=8)
goal_combobox = ttk.Combobox(main_frame, state="readonly", width=50, font=combo_style)
goal_combobox.grid(row=1, column=1, pady=8)
goal_combobox.bind("<<ComboboxSelected>>", reset_result)

# === Kendaraan ===
make_label("Kendaraan:", 2).grid(row=2, column=0, sticky="w", pady=8)
kendaraan_combobox = ttk.Combobox(main_frame, state="readonly", width=30, font=combo_style, values=["Mobil", "Motor", "Jalan Kaki"])
kendaraan_combobox.grid(row=2, column=1, sticky="w", pady=8)
kendaraan_combobox.current(0)

# === TOMBOL ===
button_frame = tk.Frame(main_frame, bg="#ffffff")
button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 5))

search_btn = tk.Button(button_frame, text="🔍 Cari Jalur", command=find_path,
                       bg="#3faaa5", fg="white", font=("Segoe UI", 11, "bold"),
                       padx=20, pady=8, relief="flat", bd=0)
search_btn.grid(row=0, column=0, padx=10)

exit_btn = tk.Button(button_frame, text="❌ Keluar", command=root.quit,
                     bg="#ff6b6b", fg="white", font=("Segoe UI", 11, "bold"),
                     padx=20, pady=8, relief="flat", bd=0)
exit_btn.grid(row=0, column=1, padx=10)

# === HASIL OUTPUT ===
result_label = tk.Label(root, text="", bg="#f1f9f9", fg="#333333",
                        font=("Segoe UI", 11), wraplength=720,
                        justify="left", anchor="w", padx=30)
result_label.pack(pady=20, fill="x")

# === JALANKAN APLIKASI ===
update_combobox_values()
root.mainloop()
