import subprocess
import xml.etree.ElementTree as ET
import os

def nmap_taramasi(hedef_ip):
    print(f"\n[*] {hedef_ip} adresi için Nmap SYN ve Versiyon taraması başlatılıyor...")
    
    # Nmap çıktısını kaydetmek için geçici bir XML dosyası adı belirliyoruz
    xml_dosyasi = "nmap_cikti.xml"
    
    # Yeni Komutumuz: 
    # -sS : SYN Tarama
    # -sV : Versiyon tespiti
    # -F  : Hızlı tarama
    # -oX : Çıktıyı XML formatında kaydet
    komut = ["sudo", "nmap", "-sS", "-sV", "-F", "-oX", xml_dosyasi, hedef_ip]
    
    try:
        # Komutu çalıştırıyoruz
        subprocess.run(komut, check=True, stdout=subprocess.DEVNULL)
        
        print("\n[+] Nmap Taraması Tamamlandı. XML Parse Ediliyor...\n")
        
        # Çıktıyı düzenli göstermek için tablo başlığı
        print(f"{'PORT':<10} | {'SERVİS':<15} | {'VERSİYON'}")
        print("-" * 60)
        
        # --- XML PARSE İŞLEMİ BURADA BAŞLIYOR ---
        tree = ET.parse(xml_dosyasi)
        root = tree.getroot()
        
        bulgular = []
        
        # XML içindeki host ve port etiketlerini (tag) geziyoruz
        for host in root.findall('host'):
            for ports in host.findall('ports'):
                for port in ports.findall('port'):
                    state = port.find('state').get('state')
                    
                    # Sadece açık (open) portları listeliyoruz
                    if state == 'open':
                        port_id = port.get('portid')
                        protocol = port.get('protocol')
                        service = port.find('service')
                        
                        # Servis adı ve versiyon bilgilerini XML'den çekiyoruz
                        if service is not None:
                            service_name = service.get('name', 'Bilinmiyor')
                            service_product = service.get('product', '')
                            service_version = service.get('version', '')
                            tam_versiyon = f"{service_product} {service_version}".strip()
                        else:
                            service_name = "Bilinmiyor"
                            tam_versiyon = "Versiyon Bulunamadı"
                            
                        if not tam_versiyon:
                            tam_versiyon = "Versiyon Bulunamadı"
                            
                        # Ekrana hocanın istediği formatta yazdırıyoruz
                        print(f"{port_id}/{protocol:<6} | {service_name:<15} | {tam_versiyon}")
                        
                        # Gelecekte AI'a göndermek üzere listeye kaydediyoruz
                        bulgular.append({"port": port_id, "servis": service_name, "versiyon": tam_versiyon})
        
        # İşimiz bitince kalabalık yapmaması için oluşturulan XML dosyasını siliyoruz
        if os.path.exists(xml_dosyasi):
            os.remove(xml_dosyasi)
            
        return bulgular
        
    except Exception as hata:
        print(f"[-] Tarama sırasında bir hata oluştu: {hata}")
        return None

if __name__ == "__main__":
    print("-" * 60)
    print("Yapay Zeka Destekli Ağ Güvenlik Tarayıcısı - Modül 1")
    print("-" * 60)
    
    hedef = input("Lütfen hedef IP adresini girin: ")
    nmap_taramasi(hedef)
