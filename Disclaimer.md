​This tool is for educational and authorized security testing only. Using it on targets without permission is illegal.

Setelah semua file di atas kamu buat di dalam folder `GhoztRecon`, jalankan perintah ini satu kali saja:

```bash
# Instal library
pip install -r requirements.txt

# Instal GhoztRecon secara global
pip install .

Sekarang, di mana pun kamu berada (folder mana pun), kamu tinggal ketik:
ghoztrecon -d target.com --param
​, [PARAM], and [SECRET] tags alongside HTTP status codes.]
​Pro Tips:
​Gunakan bendera --live jika kamu ingin memastikan link tersebut tidak 404 (tapi ini akan sedikit lebih lambat).
​Gunakan output -o untuk menyimpan hasil agar bisa kamu teruskan ke tool lain seperti nuclei atau sqlmap.
