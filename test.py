import json
import asyncio
import re
from playwright.async_api import async_playwright
import gspread
from google.oauth2.service_account import Credentials

COOKIE_FILE = "fbcookie.json"
SHEET_ID = "1aEYx3j2tVEtdTMjCsM9bWD6n7jzLTimZ-W_uIoy9YL8"

# ====== CLICK SEE MORE TRONG 1 BÀI ======
async def try_click_see_more(post):
    try:
        candidates = post.locator("div, span").filter(has_text=re.compile(r"See more|Xem thêm", re.I))
        count = await candidates.count()
        if count == 0:
            return  # Không có nút, bỏ qua luôn
        for i in range(count):
            btn = candidates.nth(i)
            try:
                await btn.scroll_into_view_if_needed()
                await asyncio.sleep(0.2)
                await btn.click()
                await asyncio.sleep(0.2)
                print("✅ Click See more thành công")
            except Exception:
                # Không click được thì bỏ qua, đừng đứng lại
                pass
    except Exception as e:
        print("⚠️ Không click được See more:", e)

# ====== CRAWL 1 PAGE ======
async def crawl_page(context, url):
    print(f"\n=== Đang vào page: {url} ===")
    page = await context.new_page()
    try:
        await page.goto(url, timeout=10000)
    except Exception as e:
        print("⚠️ Lỗi khi load page:", e)
        await page.close()
        return []

    posts_xpath = '//div[contains(@id,"_r_")]/div/div/span/div/div'

    print("⬇️ Cuộn trang và mở See more...")
    last_count = 0
    for step in range(15):  # scroll nhiều bước nhỏ hơn
        await page.mouse.wheel(0, 150)  # cuộn nhẹ
        await asyncio.sleep(0.3)       # delay ngắn

        posts = page.locator(posts_xpath)
        count = await posts.count()

        # Nếu có bài mới xuất hiện, thử click see more
        if count > last_count:
            for i in range(last_count, count):
                post = posts.nth(i)
                await try_click_see_more(post)
            last_count = count

    print(f"✔ Tổng số bài tìm thấy: {count}")

    max_posts = min(5, count)
    results = []
    for i in range(max_posts):
        post = posts.nth(i)
        try:
            text = await post.inner_text()
            print(f"--- Bài {i+1} ---\n{text[:200]}...\n")
            results.append({"text": text.strip()})
        except Exception as e:
            print(f"⚠️ Lỗi bài {i+1}: {e}")

    await page.close()
    return results
# ====== MAIN ======
async def main():
    # Load cookie FB
    try:
        cookies = json.load(open(COOKIE_FILE, "r", encoding="utf-8"))
    except:
        print("❌ Không tìm thấy fbcookie.json")
        return

    # Google Sheets
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("botfbcre.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet_config = client.open_by_key(SHEET_ID).worksheet("Config")
    sheet_output = client.open_by_key(SHEET_ID).worksheet("Crawdata")

    links = sheet_config.col_values(2)[1:]
    print("Danh sách link cần craw:")
    for l in links:
        print(" -", l)

    async with async_playwright() as p:
        for link in links:
            print(f"\n🚀 Bắt đầu crawl page: {link}")
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            await context.add_cookies(cookies)

            sheet_output.clear() if links.index(link) == 0 else None
            if links.index(link) == 0:
                sheet_output.append_row(["Page", "Index", "Content"])

            posts = await crawl_page(context, link)
            for i, content in enumerate(posts):
                sheet_output.append_row([link, i+1, content["text"]])

            await browser.close()  # tắt hẳn browser sau mỗi page

    print("\n🎉 DONE – Craw xong và lưu vào sheet Crawdata")

if __name__ == "__main__":
    asyncio.run(main())
