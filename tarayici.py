import subprocess
import xml.etree.ElementTree as ET
import os

# --- MODÜL 1: PORT VE VERSİYON TARAMASI ---
def nmap_taramasi(hedef_ip):
    print(f"\n[*] {hedef_ip} adresi için Modül 1 (Port/Versiyon Taraması) başlatılıyor...")
    xml_dosyasi = "nmap_cikti.xml"
    komut = ["sudo", "nmap", "-sS", "-sV", "-F", "-oX", xml_dosyasi, hedef_ip]
    
    try:
        subprocess.run(komut, check=True, stdout=subprocess.DEVNULL)
        print("\n[+] Modül 1 Tamamlandı. Açık Portlar:\n")
        print(f"{'PORT':<10} | {'SERVİS':<15} | {'VERSİYON'}")
        print("-" * 60)
        
        tree = ET.parse(xml_dosyasi)
        root = tree.getroot()
        bulgular = []
        
        for host in root.findall('host'):
            for ports in host.findall('ports'):
                for port in ports.findall('port'):
                    if port.find('state').get('state') == 'open':
                        port_id = port.get('portid')
                        protocol = port.get('protocol')
                        service = port.find('service')
                        
                        service_name = service.get('name', 'Bilinmiyor') if service is not None else "Bilinmiyor"
                        service_product = service.get('product', '') if service is not None else ""
                        service_version = service.get('version', '') if service is not None else ""
                        tam_versiyon = f"{service_product} {service_version}".strip() or "Versiyon Bulunamadı"
                            
                        print(f"{port_id}/{protocol:<6} | {service_name:<15} | {tam_versiyon}")
                        bulgular.append({"port": port_id, "servis": service_name, "versiyon": tam_versiyon})
        
        if os.path.exists(xml_dosyasi): os.remove(xml_dosyasi)
        return bulgular
    except Exception as hata:
        print(f"[-] Modül 1 Hatası: {hata}")
        return None

# --- M4: AKTİF CİHAZ KEŞFİ ---
def aktif_cihaz_kesfi(hedef_ag):
    print(f"\n[*] {hedef_ag} ağı için Modül 2 (Aktif Cihaz Keşfi) başlatılıyor...")
    xml_dosyasi = "cihaz_kesfi.xml"
    
    # Nmap -sn parametresi Ping Sweep yapar (Port taramaz, sadece ayaktaki cihazları ve MAC'leri bulur)
    komut = ["sudo", "nmap", "-sn", "-oX", xml_dosyasi, hedef_ag]
    
    try:
        subprocess.run(komut, check=True, stdout=subprocess.DEVNULL)
        print("\n[+] M4 Tamamlandı. Ağdaki Aktif Cihazlar:\n")
        print(f"{'IP ADRESİ':<18} | {'MAC ADRESİ':<20} | {'CİHAZ ÜRETİCİSİ'}")
        print("-" * 65)
        
        tree = ET.parse(xml_dosyasi)
        root = tree.getroot()
        cihazlar = []
        
        for host in root.findall('host'):
            # Sadece durumu "up" (açık) olan cihazları alıyoruz
            if host.find('status').get('state') == 'up':
                ip_addr = "Bilinmiyor"
                mac_addr = "Bilinmiyor"
                vendor = "Bilinmiyor Üretici"
                
                # IP, MAC ve Üretici bilgilerini çekiyoruz
                for address in host.findall('address'):
                    if address.get('addrtype') == 'ipv4':
                        ip_addr = address.get('addr')
                    elif address.get('addrtype') == 'mac':
                        mac_addr = address.get('addr')
                        vendor = address.get('vendor', 'Bilinmiyor Üretici')
                
                print(f"{ip_addr:<18} | {mac_addr:<20} | {vendor}")
                # AI API'sine göndermek için listeye ekliyoruz
                cihazlar.append({"ip": ip_addr, "mac": mac_addr, "uretici": vendor})
                
        if os.path.exists(xml_dosyasi): os.remove(xml_dosyasi)
        return cihazlar
    except Exception as hata:
        print(f"[-] M4  Hatası: {hata}")
        return None

# --- ANA ÇALIŞTIRMA BLOKU ---
if __name__ == "__main__":
    print("=" * 70)
    print("Yapay Zeka Destekli Ağ Güvenlik Tarayıcısı - Modül 1 & Modül 2")
    print("=" * 70)
    
    hedef_ip = input("\nLütfen Modül 1 için hedef IP adresini girin (Örn: 192.168.17.129): ")
    modul1_sonuclari = nmap_taramasi(hedef_ip)
    
    # Ağ adresi genellikle IP'nin sonunun 0/24 ile değiştirilmiş halidir
    hedef_ag = input("\nLütfen Modül 2 için ağ adresini girin (Örn: 192.168.17.0/24): ")
    modul2_sonuclari = aktif_cihaz_kesfi(hedef_ag)
    
    print("\n[*] Her iki modül de başarıyla çalıştı. Veriler AI analizi için hazırlandı!")
