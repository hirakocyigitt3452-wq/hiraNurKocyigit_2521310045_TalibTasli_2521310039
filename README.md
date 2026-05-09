# hiraNurKocyigit_2521310045_TalibTasli_2521310039

1-) Github'da proje için repository oluşturuldu. İçerisine README.md, requirements.txt ve .gitignore dosyaları
eklenip taslak oluşturuldu. .env dosyasıın içerisine api key koyuldu.
Api Key'in github'da görünmemesi için .gitignore içine .env yazıldı. 

2-) Kali Linux ve Github, Linux da terminale yazdığımız şu adımlar ile
birbirine bağlandı ve kali terminalinden commit-push edilmesi sağlandı:
git add . ,
git remote add origin https://github.com/"Github Repo urlsi" ,
git commit -m "ne yazmak istenirse ",
git push
kullanıcı adı ve şifre kısmında, Github kullanıcı adını ve Github'dan aldığımız token girildi.

3-) Proje klasörünün içerisine py uzantılı dosya oluşturuldu ve içine gerekli python kodları yazıldı.
sudo python3 tarayici.py komutu ile dosya çalıştırıldı ve aşağıdaki görüntü elde edildi.

![Modül 1 Nmap Tarama Sonucu](nmap_sonuc.png)

4-) tarayici.py dosyasında M4 Aktif Cihaz Keşfi için pyhton kodları eklendi.
sudo python3 tarayici.py komutu ile Çalıştırıldı ve aşağıdaki görüntü elde edildi.

![Modül 4 AKtif Cihaz Keşfi Sonucu](aktif_cihaz.png)


5-) tarayici.py dosyasında AI API ve gerekli kütüphaneler eklendi. (API olarak Google Gemini Flash kullanıldı)
sudo pyhton3 tarayici.py komutu ile çalıştırıldı ve aşağıdaki çıktı elde edildi.

![AI API sonucu](api1.png)
![AI API sonucu](api4,.png)

6-) HTML Raporu Oluşturma
Proje tamamlandığında tüm bulguları (Nmap sonuçları, Aktif Cihaz keşfi ve AI analizi) içeren düzenli bir HTML raporu otomatik olarak oluşturuldu. Bu rapor "guvenlik_raporu.html" adıyla kaydedildi.

![HTML Rapor Ekran Görüntüsü](html.png)

 
7-) tarayici.py dosyasındaki kodlar,ayrı py dosyalarına aktarıldı.

main.py: main.py: Programın ana giriş noktasıdır. Kullanıcıdan IP/Ağ bilgilerini alır, diğer modülleri sırasıyla çalıştırır ve sonuçları birleştirerek HTML raporu oluşturur.
m1.py: Nmap ile hedef IP üzerinde SYN taraması yapar. 
m4.py: yerel ağda (Subnet) ping taraması yaparak aktif cihazları, MAC adreslerini ve üretici bilgilerini listeler.






 
