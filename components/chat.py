# kick_chat_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchWindowException, 
    WebDriverException, 
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException
)
from collections import deque
import time
import os
from datetime import datetime
import logging

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://kick.com/hype")
    return driver

def find_username_element(entry):
    """Kullanıcı adı elementini bulmak için farklı selector'ları dener"""
    selectors = [
        # Kick.com'un yeni yapısı için spesifik selector'lar
        'div > div > button',
        'div[class*="betterhover"] > div > button',
        'div[class*="group-hover"] > div > button',
        'div[class*="bg-shade-lower"] > div > button',
        'div[class*="w-full"] > div > button',
        'div[class*="min-w-0"] > div > button',
        'div[class*="shrink-0"] > div > button',
        'div[class*="break-words"] > div > button',
        'div[class*="rounded-lg"] > div > button',
        'div[class*="px-2"] > div > button',
        'div[class*="py-1"] > div > button',
        # Genel selector'lar
        'button[title]',
        'span[title]',
        'a[title]',
        '.username',
        '[data-username]',
        'button[data-v-*][title]',
        'span[data-v-*][title]'
    ]
    
    for selector in selectors:
        try:
            element = entry.find_element(By.CSS_SELECTOR, selector)
            username = element.get_attribute("title")
            if not username:
                username = element.text.strip()
            if username:
                return username
        except NoSuchElementException:
            continue
        except Exception as e:
            logger.debug(f"Selector {selector} için hata: {e}")
            continue
    
    return None

def find_message_element(entry):
    """Mesaj elementini bulmak için farklı selector'ları dener"""
    selectors = [
        # Kick.com'un yeni yapısı için spesifik selector'lar
        'span[class*="font-normal"]',
        'span[class*="leading-"]',
        'div[class*="message"]',
        'p[class*="message"]',
        # XPath selector'ları
        './/span[contains(@class, "font-normal") and contains(@class, "leading-")]',
        './/span[contains(@class, "font-normal")]',
        './/span[contains(@class, "leading-")]',
        './/div[contains(@class, "message")]',
        './/p[contains(@class, "message")]',
        # Genel selector'lar
        '.message-content',
        '.chat-message',
        'span',
        'div',
        'p'
    ]
    
    for selector in selectors:
        try:
            if selector.startswith('.//'):
                element = entry.find_element(By.XPATH, selector)
            else:
                element = entry.find_element(By.CSS_SELECTOR, selector)
            
            message = element.text.strip()
            if message and len(message) > 0:
                return message
        except NoSuchElementException:
            continue
        except Exception as e:
            logger.debug(f"Selector {selector} için hata: {e}")
            continue
    
    # Son çare olarak tüm text'i al
    try:
        message = entry.text.strip()
        if message and len(message) > 0:
            return message
    except Exception as e:
        logger.debug(f"Text alma hatası: {e}")
    
    return None

def wait_for_chat_load(driver, timeout=30):
    """Chat'in yüklenmesini bekler"""
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.ID, "chatroom-messages")))
        logger.info("Chat başarıyla yüklendi")
        return True
    except TimeoutException:
        logger.error("Chat yüklenme timeout'u")
        return False

def main():
    driver = None
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            driver = start_driver()
            if wait_for_chat_load(driver):
                break
            else:
                retry_count += 1
                if driver:
                    driver.quit()
                logger.warning(f"Retry {retry_count}/{max_retries}")
                time.sleep(5)
        except Exception as e:
            logger.error(f"Driver başlatma hatası: {e}")
            retry_count += 1
            if driver:
                driver.quit()
            time.sleep(5)
    
    if retry_count >= max_retries:
        logger.error("Maximum retry sayısına ulaşıldı, program sonlandırılıyor")
        return

    printed_messages = deque(maxlen=100)
    last_refresh = time.time()
    error_count = 0
    max_errors = 10

    filepath = os.path.abspath("mustfyman_mesajlari.txt")
    logger.info(f"Kayıt dosyası: {filepath}")

    try:
        while True:
            # Sayfa yenileme kontrolü
            if time.time() - last_refresh > 3600:
                logger.info("Sayfa 60 dakika doldu, yenileniyor...")
                try:
                    driver.refresh()
                    if wait_for_chat_load(driver):
                        last_refresh = time.time()
                        error_count = 0
                    else:
                        raise Exception("Chat yüklenemedi")
                except Exception as e:
                    logger.error(f"Sayfa yenilenirken hata: {e}")
                    driver.quit()
                    driver = start_driver()
                    if wait_for_chat_load(driver):
                        last_refresh = time.time()
                        error_count = 0
                    else:
                        logger.error("Yeniden başlatma başarısız")
                        break

            try:
                # Chat mesajlarını al - daha spesifik XPath kullan
                chat_entries = driver.find_elements(
                    By.XPATH, '//*[@id="chatroom-messages"]/div/div'
                )
                
                # Alternatif selector'lar
                if not chat_entries:
                    chat_entries = driver.find_elements(
                        By.CSS_SELECTOR, '#chatroom-messages > div > div'
                    )
                
                if not chat_entries:
                    chat_entries = driver.find_elements(
                        By.XPATH, '//*[@id="chatroom-messages"]//div[contains(@class, "relative")]'
                    )
                
                if not chat_entries:
                    logger.debug("Chat mesajı bulunamadı")
                    time.sleep(2)
                    continue

            except Exception as e:
                logger.error(f"Chat elemanları alınırken hata: {e}")
                error_count += 1
                if error_count >= max_errors:
                    logger.error("Çok fazla hata, program sonlandırılıyor")
                    break
                time.sleep(2)
                continue

            processed_count = 0
            for entry in chat_entries:
                try:
                    # Debug için entry'nin HTML'ini logla (sadece ilk birkaç entry için)
                    if processed_count < 3:
                        logger.debug(f"Entry HTML: {entry.get_attribute('outerHTML')[:200]}...")
                    
                    # Kullanıcı adını bul
                    username = find_username_element(entry)
                    
                    if not username:
                        continue
                    
                    logger.debug(f"Bulunan kullanıcı: {username}")
                    
                    if username == 'mustfyman':
                        # Mesajı bul
                        message = find_message_element(entry)
                        
                        if not message:
                            logger.debug("Mesaj bulunamadı")
                            continue
                        
                        logger.debug(f"Bulunan mesaj: {message}")
                        
                        # Mesaj daha önce işlendi mi kontrol et
                        if message not in printed_messages:
                            printed_messages.append(message)
                            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                            formatted_message = f"{timestamp} - {username}: {message}"
                            
                            print(formatted_message)
                            logger.info(f"Yeni mesaj kaydedildi.")
                            
                            # Dosyaya yaz
                            try:
                                with open("mustfyman_mesajlari.txt", "a", encoding="utf-8") as f:
                                    f.write(formatted_message + "\n")
                            except Exception as e:
                                logger.error(f"Dosya yazma hatası: {e}")
                            
                            processed_count += 1
                            error_count = 0  # Başarılı işlemde hata sayacını sıfırla

                except StaleElementReferenceException:
                    logger.debug("Stale element reference, devam ediliyor...")
                    continue
                except Exception as e:
                    logger.debug(f"Mesaj işleme hatası: {e}")
                    continue

            if processed_count > 0:
                logger.debug(f"{processed_count} mesaj işlendi")

            time.sleep(2)

    except (NoSuchWindowException, WebDriverException) as e:
        logger.error(f"Tarayıcı hatası: {e}")
    except KeyboardInterrupt:
        logger.info("Program kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("Tarayıcı kapatıldı")
            except:
                pass

if __name__ == "__main__":
    main()