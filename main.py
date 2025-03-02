import asyncio
from fastapi import FastAPI
from pyppeteer import launch

app = FastAPI()

async def get_tracking_info(tracking_url):
    """Hàm lấy thông tin vận đơn từ trang SPX"""

    # Sử dụng Chromium được cài đặt sẵn trên Linux
    browser = await launch(
        executablePath="/usr/bin/chromium-browser",  # Đường dẫn Chromium trên Render
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

    page = await browser.newPage()
    await page.goto(tracking_url)

    # Chờ dữ liệu xuất hiện
    await page.waitForSelector(".order-process-detail-list")

    # Lấy thông tin chi tiết về vận đơn
    elements = await page.querySelectorAll(".order-process-detail-list .detail-list-item")
    tracking_details = []

    for element in elements:
        text = await page.evaluate('(el) => el.innerText', element)
        tracking_details.append(text)

    await browser.close()

    return {"tracking_details": tracking_details}

@app.get("/track/{tracking_id}")
async def track_shipment(tracking_id: str):
    """API để lấy thông tin vận đơn theo mã"""
    tracking_url = f"https://spx.vn/track?{tracking_id}"
    data = await get_tracking_info(tracking_url)
    return data

# Chạy ứng dụng nếu file được chạy trực tiếp
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
