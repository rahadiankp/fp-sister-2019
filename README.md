## Proyek Akhir Sistem Terdistribusi 2019
### Arsitektur
![Arsitektur](assets/architecture.png)
### Data Consistency Protocol
#### Replication
1. Klien mengirimkan perintah/instruksi kepada Server melalui Proxy
2. Perintah akan masuk ke *queue* yang berada di Proxy
3. Setiap perintah yang ada di *queue* akan di-*dequeue* dan didistribusikan ke seluruh server yang tersedia/*up* dan juga ke Transactions Manager untuk di-*track*
4. Perintah yang dikirim ke Server akan diproses sesuai dengan protokol game Tic-Tac-Toe yang telah ditentukan
5. Seluruh Server menyimpan *state* yang sama sekarang
#### Failover Recovery
1. Server yang baru saja *down* dan di-*restart* akan bertanya URI Transactions Manager kepada Proxy
2. Server membangun koneksi dengan Transaction Manager dan menyatakan dirinya NOT READY
3. Kepada Transactions Manager, Server bertanya seluruh perintah yang sudah dieksekusi secara berurutan
4. Secara berurutan, Server akan mengeksekusi satu per satu perintah yang sebelumnya sudah dieksekusi oleh Server lain
5. Server bertanya kembali ke Transactions Manager mengenai jumlah perintah yang tersimpan di Transactions Manager
6. Jika jumlahnya sama dengan perintah yang dieksekusi oleh Server, maka ke no. 8; Jika tidak, ke no. 7
7. Ambil sisa perintah yang belum ter-*fetch* oleh Server di Transactions Manager. Kembali ke no. 5
8. *Recovery* sudah sukses dilaksanakan, Server menyatakan dirinya READY dan siap untuk menerima koneksi
