# bellman_ford_algoritm_Map_Unib

FUNGSI BellmanFord(graph, start, goal):
    Inisialisasi jarak ke semua simpul dengan ∞ (tak hingga)
    Inisialisasi pendahulu semua simpul dengan None
    Set jarak[start] = 0

    ULANGI (jumlah simpul - 1) KALI:
        UNTUK setiap simpul dalam graf:
            UNTUK setiap tetangga dan bobot dari simpul:
                JIKA jarak[simpul] + bobot < jarak[tetangga]:
                    Update jarak[tetangga] = jarak[simpul] + bobot
                    Update pendahulu[tetangga] = simpul

    // Deteksi siklus negatif
    UNTUK setiap simpul dalam graf:
        UNTUK setiap tetangga dan bobot dari simpul:
            JIKA jarak[simpul] + bobot < jarak[tetangga]:
                KEMBALIKAN (None, "Terdapat siklus negatif di graf!")

    // Bangun kembali jalur dari goal ke start
    Buat list path kosong
    Set current = goal
    SELAMA current TIDAK None:
        Sisipkan current ke awal path
        Set current = pendahulu[current]

    JIKA jarak[goal] == ∞:
        KEMBALIKAN (None, "Tidak ada jalur dari start ke goal")

    KEMBALIKAN (path, jarak[goal])
