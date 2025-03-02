import asyncio
from fastapi import FastAPI
from pyppeteer import launch

app = FastAPI()

async def get_tracking_info(tracking_url):
    """Hàm lấy thông tin vận đơn từ trang SPX"""
    
    # Đường dẫn Chrome có sẵn trên máy (Cập nhật đúng với máy bạn)
   # browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    browser = await launch(
    executablePath="/usr/bin/google-chrome",
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

