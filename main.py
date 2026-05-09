import datetime
import os
from dotenv import load_dotenv
from google import genai

# Diğer dosyalardaki fonksiyonları projemize dahil ediyoruz
import m1
import m4

def yapay_zeka_analizi(modul1_veri, modul2_veri):
    print("\n[*] Yapay Zeka (Google Gemini) analizi başlatılıyor, lütfen bekleyin...")
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("[-] HATA: .env dosyasında API_KEY bulunamadı!")
        return "Yapay zeka analizi yapılamadı (API Key eksik)."
        
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        Sen kıdemli bir Siber Güvenlik Uzmanısın. Aşağıda Nmap ile yapılmış bir ağ taraması sonuçları var.
        Bu bulguları inceleyerek profesyonel ve Türkçe bir risk analizi raporu oluştur. Müşteriye sunulacak HTML raporu içine gömüleceği için formatı düzgün tut.
        M1 (Açık Portlar): {modul1_veri}
        M4 (Ağdaki Cihazlar): {modul2_veri}
        """
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        print("[+] Yapay Zeka analizi başarıyla tamamlandı.")
        return response.text
    except Exception as e:
        print(f"[-] Yapay zeka bağlantısında bir hata oluştu: {e}")
        return f"Yapay zeka analizi sırasında hata: {e}"

def html_rapor_olustur(m1_veri, m2_veri, ai_rapor):
    print("[*] Profesyonel HTML raporu hazırlanıyor...")
    zaman = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Raporun genel HTML ve tam CSS iskeleti
    html_icerik = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Siber Güvenlik Tarama Raporu</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f8f9fa; color: #212529; line-height: 1.6; }}
            h1 {{ color: #dc3545; text-align: center; border-bottom: 2px solid #dc3545; padding-bottom: 10px; }}
            h2 {{ color: #0d6efd; margin-top: 30px; }}
            .zaman-etiketi {{ text-align: center; font-weight: bold; color: #6c757d; margin-bottom: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; background-color: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            th, td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
            th {{ background-color: #343a40; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .ai-kutu {{ background-color: #e2e3e5; border-left: 6px solid #ffc107; padding: 20px; white-space: pre-wrap; font-family: monospace; font-size: 14px; overflow-x: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <h1>Ağ Güvenlik Tarama Raporu</h1>
        <div class="zaman-etiketi">Oluşturulma Tarihi: {zaman}</div>

        <h2>Modül 1: Açık Portlar ve Servisler</h2>
        <table>
            <tr><th>Port / Protokol</th><th>Servis Adı</th><th>Versiyon Bilgisi</th></tr>
    """
    
    # M1 verilerini tabloya ekle
    if m1_veri:
        for item in m1_veri:
            html_icerik += f"<tr><td>{item['port']}/{item['protokol']}</td><td>{item['servis']}</td><td>{item['versiyon']}</td></tr>\n"
    else:
        html_icerik += "<tr><td colspan='3'>Hedefte açık port bulunamadı veya taranmadı.</td></tr>\n"
        
    html_icerik += """
        </table>

        <h2>M4: Aktif Cihaz Keşfi</h2>
        <table>
            <tr><th>IP Adresi</th><th>MAC Adresi</th><th>Cihaz Üreticisi</th></tr>
    """
    
    # M4 verilerini tabloya ekle
    if m2_veri:
        for item in m2_veri:
            html_icerik += f"<tr><td>{item['ip']}</td><td>{item['mac']}</td><td>{item['uretici']}</td></tr>\n"
    else:
        html_icerik += "<tr><td colspan='3'>Ağda cihaz bulunamadı veya taranmadı.</td></tr>\n"
        
    html_icerik += f"""
        </table>

        <h2>Yapay Zeka Risk Analizi (Google Gemini)</h2>
        <div class="ai-kutu">{ai_rapor if ai_rapor else "AI Raporu Bulunamadı."}</div>

    </body>
    </html>
    """
    
    with open("guvenlik_raporu.html", "w", encoding="utf-8") as dosya:
        dosya.write(html_icerik)
        
    print("\n[+] GÖREV TAMAMLANDI! Sonuçlar 'guvenlik_raporu.html' adlı dosyaya kaydedildi.")

if __name__ == "__main__":
    hedef_ip = input("M1 için hedef IP adresini girin (Örn: 192.168.17.129): ")
    hedef_ag = input("M4 için ağ adresini girin (Örn: 192.168.17.0/24): ")
    
    # Modüllerden fonksiyonları çağırıyoruz
    m1_sonuc = m1.nmap_taramasi(hedef_ip)
    m2_sonuc = m4.aktif_cihaz_kesfi(hedef_ag)
    
    ai_rapor_metni = None
    if m1_sonuc and m2_sonuc:
        ai_rapor_metni = yapay_zeka_analizi(m1_sonuc, m2_sonuc)
        
    html_rapor_olustur(m1_sonuc, m2_sonuc, ai_rapor_metni)
