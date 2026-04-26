import yfinance as yf
import requests
import os

# GitHub Secretsから住所(URL)を読み込む
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
# テスト用に1000円に設定（1410.5円なら確実に通知が来る）
TARGET_PRICE = 1000 

def check_stock():
    # 第一生命ホールディングス(8750.T)
    stock = yf.Ticker("8750.T")
    # 土日でもデータが取れるように直近5日分を取得
    df = stock.history(period="5d")
    
    if df.empty:
        print("株価データの取得に失敗しました。")
        return

    current_price = round(df['Close'].iloc[-1], 2)
    print(f"現在値: {current_price}円 / 目標: {TARGET_PRICE}円")

    # 目標価格(1000円)を超えていたら通知
    if current_price >= TARGET_PRICE:
        payload = {
            "username": "第一生命 株価監視くん",
            "content": f"🎯 **目標価格到達！**\n第一生命（8750）が目標の {TARGET_PRICE}円 を超えました。\n現在の株価：**{current_price}円**"
        }
        requests.post(WEBHOOK_URL, json=payload)
        print("通知を送信しました。")

if __name__ == "__main__":
    check_stock()
