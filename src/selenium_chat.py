# selenium_chat.py

import asyncio
import websockets
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from collections import deque

clients = set()
printed_messages = deque(maxlen=100)

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

async def ws_handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

async def start_ws_server():
    async with websockets.serve(ws_handler, "localhost", 6789):
        await asyncio.Future()  # sonsuz bekleme

def run_ws_server():
    asyncio.run(start_ws_server())

def send_to_clients(message):
    to_remove = set()
    for ws in clients:
        try:
            asyncio.run_coroutine_threadsafe(ws.send(message), asyncio.get_event_loop())
        except:
            to_remove.add(ws)
    clients.difference_update(to_remove)

def chat_scraper():
    driver = start_driver()
    time.sleep(3)
    last_refresh = time.time()

    while True:
        if time.time() - last_refresh > 3600:
            driver.refresh()
            time.sleep(5)
            last_refresh = time.time()

        try:
            chat_entries = driver.find_elements(
                By.XPATH, '//*[@id="chatroom-messages"]//div[contains(@class, "relative")]'
            )
        except:
            time.sleep(2)
            continue

        for entry in chat_entries:
            try:
                try:
                    username_element = entry.find_element(By.CSS_SELECTOR, 'button[title]')
                except:
                    username_element = entry.find_element(By.CSS_SELECTOR, 'span[title]')
                username = username_element.get_attribute("title")

                if username == 'mustfyman':
                    message_element = entry.find_element(
                        By.XPATH, './/span[contains(@class, "font-normal") and contains(@class, "leading-")]'
                    )
                    message = message_element.text.strip()

                    if message and message not in printed_messages:
                        printed_messages.append(message)
                        print(f"{username}: {message}")
                        asyncio.run_coroutine_threadsafe(
                            broadcast_message(f"{username}: {message}"),
                            asyncio.get_event_loop()
                        )
            except StaleElementReferenceException:
                continue
            except Exception as e:
                print(f"Hata: {e}")

        time.sleep(2)

async def broadcast_message(msg):
    to_remove = set()
    for ws in clients:
        try:
            await ws.send(msg)
        except:
            to_remove.add(ws)
    clients.difference_update(to_remove)

def main():
    threading.Thread(target=run_ws_server, daemon=True).start()
    time.sleep(1)
    chat_scraper()

if __name__ == "__main__":
    main()
