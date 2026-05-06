import subprocess
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv
from google import genai # YENİ GOOGLE KÜTÜPHANESİ

# --- MODÜL 1: PORT VE VERSİYON TARAMASI ---
def nmap_taramasi(hedef_ip):
    print(f"\n[*] {hedef_ip} adresi için Port/Versiyon Taraması başlatılıyor...")
    xml_dosyasi = "nmap_cikti.xml"
    komut = ["sudo", "nmap", "-sS", "-sV", "-F", "-oX", xml_dosyasi, hedef_ip]
    
    try:
        subprocess.run(komut, check=True, stdout=subprocess.DEVNULL)
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
                        service_version = service.get('version', '') if service is not None else ""
                        tam_versiyon = f"{service_name} {service_version}".strip()
                        
                        bulgular.append({"port": port_id, "protokol": protocol, "versiyon": tam_versiyon})
        
        if os.path.exists(xml_dosyasi): os.remove(xml_dosyasi)
        print(f"[+] Modül 1 Tamamlandı. ({len(bulgular)} açık port bulundu)")
        return bulgular
    except Exception as hata:
        print(f"[-] Modül 1 Hatası: {hata}")
        return None

# --- M4 : AKTİF CİHAZ KEŞFİ ---
def aktif_cihaz_kesfi(hedef_ag):
    print(f"[*] {hedef_ag} ağı için Aktif Cihaz Keşfi başlatılıyor...")
    xml_dosyasi = "cihaz_kesfi.xml"
    komut = ["sudo", "nmap", "-sn", "-oX", xml_dosyasi, hedef_ag]
    
    try:
        subprocess.run(komut, check=True, stdout=subprocess.DEVNULL)
        tree = ET.parse(xml_dosyasi)
        root = tree.getroot()
        cihazlar = []
        
        for host in root.findall('host'):
            if host.find('status').get('state') == 'up':
                ip_addr, mac_addr, vendor = "Bilinmiyor", "Bilinmiyor", "Bilinmiyor Üretici"
                for address in host.findall('address'):
                    if address.get('addrtype') == 'ipv4': ip_addr = address.get('addr')
                    elif address.get('addrtype') == 'mac':
                        mac_addr = address.get('addr')
                        vendor = address.get('vendor', 'Bilinmiyor Üretici')
                cihazlar.append({"ip": ip_addr, "mac": mac_addr, "uretici": vendor})
                
        if os.path.exists(xml_dosyasi): os.remove(xml_dosyasi)
        print(f"[+] M4 Tamamlandı. ({len(cihazlar)} cihaz bulundu)")
        return cihazlar
    except Exception as hata:
        print(f"[-] M4 Hatası: {hata}")
        return None

# --- YAPAY ZEKA ENTEGRASYONU ---
def yapay_zeka_analizi(modul1_veri, modul2_veri):
    print("\n[*] Yapay Zeka (Google Gemini) analizi başlatılıyor, lütfen bekleyin...\n")
    
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("[-] HATA: .env dosyasında _API_KEY bulunamadı!")
        return
        
    try:
        # Yeni Google kütüphanesinin çalışma mantığı
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Sen kıdemli bir Siber Güvenlik Uzmanısın. Aşağıda Nmap ile yapılmış bir ağ taraması sonuçları var.
        Bu bulguları inceleyerek profesyonel ve Türkçe bir risk analizi raporu oluştur.
        Özellikle kritik zafiyet barındıran servisler varsa (örneğin vsftpd 2.3.4) bunları vurgula ve çözüm öner.
        
        Modül 1 (Açık Portlar ve Versiyonlar): {modul1_veri}
        M4  (Ağdaki Cihazlar): {modul2_veri}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        print("=" * 70)
        print("🤖 YAPAY ZEKA GÜVENLİK ANALİZ RAPORU")
        print("=" * 70)
        print(response.text)
        print("=" * 70)
        
    except Exception as e:
        print(f"[-] Yapay zeka bağlantısında bir hata oluştu: {e}")

# --- ANA ÇALIŞTIRMA BLOKU ---
if __name__ == "__main__":
    hedef_ip = input("Modül 1 için hedef IP adresini girin (Örn: 192.168.17.129): ")
    hedef_ag = input("Modül 2 için ağ adresini girin (Örn: 192.168.17.0/24): ")
    
    m1_sonuc = nmap_taramasi(hedef_ip)
    m2_sonuc = aktif_cihaz_kesfi(hedef_ag)
    
    # Hata yakalama eklendi: Eğer liste boş dönerse uyarı ver
    if not m1_sonuc:
        print("\n[-] UYARI: Hedef IP'de hiçbir açık port bulunamadı! IP'yi doğru yazdığınızdan emin olun.")
        
    if m1_sonuc is not None and m2_sonuc is not None:
        yapay_zeka_analizi(m1_sonuc, m2_sonuc)
