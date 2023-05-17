from playwright.sync_api import Playwright, sync_playwright
import time

# 동행복권 아이디와 패스워드를 설정
USER_ID = 'qkrqja9706'
USER_PW = '@p24749706'

# 구매 개수를 설정
COUNT = 1

def run(playwright: Playwright) -> None:
    # chrome 브라우저를 실행
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://dhlottery.co.kr/user.do?method=login
    page.goto("https://dhlottery.co.kr/user.do?method=login")

    # Click [placeholder="아이디"]
    page.click("[placeholder=\"아이디\"]")

    # Fill [placeholder="아이디"]
    page.fill("[placeholder=\"아이디\"]", USER_ID)

    # Press Tab
    page.press("[placeholder=\"아이디\"]", "Tab")

    # Fill [placeholder="비밀번호"]
    page.fill("[placeholder=\"비밀번호\"]", USER_PW)

    # Press Tab
    page.press("[placeholder=\"비밀번호\"]", "Tab")

    # Press Enter
    # with page.expect_navigation(url="https://ol.dhlottery.co.kr/olotto/game/game645.do"):
    with page.expect_navigation():
        page.press("form[name=\"jform\"] >> text=로그인", "Enter")

    time.sleep(5)

    page.goto(url="https://ol.dhlottery.co.kr/olotto/game/game645.do")
    # "비정상적인 방법으로 접속하였습니다. 정상적인 PC 환경에서 접속하여 주시기 바랍니다." 우회하기
    page.locator("#popupLayerAlert").get_by_role("button", name="확인").click()
    print(page.content())

    # Click text=자동번호발급
    page.click("text=자동번호발급")
    # page.click('#num2 >> text=자동번호발급')

    # 구매할 개수를 선택
    # Select 1
    page.select_option("select", str(COUNT))

    # Click text=확인
    page.click("text=확인")

    # Click input:has-text("구매하기")
    page.click("input:has-text(\"구매하기\")")

    time.sleep(2)
    # Click text=확인 취소 >> input[type="button"]
    page.click("text=확인 취소 >> input[type=\"button\"]")

    # Click input[name="closeLayer"]
    page.click("input[name=\"closeLayer\"]")
    # assert page.url == "https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40"

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)