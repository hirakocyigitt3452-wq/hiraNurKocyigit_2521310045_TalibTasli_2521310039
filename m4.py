import subprocess
import xml.etree.ElementTree as ET
import os

def aktif_cihaz_kesfi(hedef_ag):
    print(f"\n[*] {hedef_ag} ağı için Aktif Cihaz Keşfi başlatılıyor...")
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
