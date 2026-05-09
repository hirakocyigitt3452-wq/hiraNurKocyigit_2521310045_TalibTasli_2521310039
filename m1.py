import subprocess
import xml.etree.ElementTree as ET
import os

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
                        service_version = service.get('version', 'Bulunamadı') if service is not None else "Bulunamadı"
                        
                        bulgular.append({"port": port_id, "protokol": protocol, "servis": service_name, "versiyon": service_version})
        
        if os.path.exists(xml_dosyasi): os.remove(xml_dosyasi)
        print(f"[+] M1 Tamamlandı. ({len(bulgular)} açık port bulundu)")
        return bulgular
    except Exception as hata:
        print(f"[-] M1 Hatası: {hata}")
        return None
