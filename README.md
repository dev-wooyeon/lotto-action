## lotto-action
> **Note**  
> python + github action을 활용해 자동으로 로또를 구매합니다.  
> 하기 원문 링크의 계정 정보 암호화하는 기능을 추가한 프로젝트입니다.

**[원문 링크](https://velog.io/@king/githubactions-lotto)**

### 준비물
  - [예치금 사전 충전](https://dhlottery.co.kr/payment.do?method=payment)

### 구축하기
GitHub 저장소 생성.  

소스코드 작성
2개의 파일이 필요합니다.  
`action.yml`  
`main.py`

✅ .github/workflows/ 하위 경로에 action.yml 있어야만 GitHub Actions 이 동작합니다!
``` 
$ root@master:github-action# tree -al -I '.git'  
.  
├── .github
│   └── workflows
│       └── action.yml
├── README.md
└── main.py
action.yml  
```

name: Lotto Action. 
`Note` 
원인이 무엇인지 모르겠지만.  
cron 표현식을 이용해 스케줄링을 하여도 예상 시간보다 5분 ~ 10분 이후에 동작합니다. (이 점을 유의해서 시간 설정을 해야합니다.)

``` bash
#on: [push]
on:
  schedule:
    - cron: '30 23 * * 5' # UST 기준의 크론. UST 23:30 는 KST 08:30 (+ 09:00)

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7]

    steps:
    - uses: actions/checkout@v2
    - name: Set up python ${{ matrix.python-version }}
      uses: actions/setup-python@v1
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install python package
      run: |        
        pip install selenium
        pip install requests        
        pip install twython
        pip install pillow    
        pip install gspread        
        pip install --upgrade google-api-python-client oauth2client
        pip install playwright
        python -m playwright install ${{ matrix.browser-channel }} --with-deps
    
    - name: Install ubuntu package
      run: |        
        sudo apt-get install fonts-unfonts-core
        sudo apt-get install fonts-unfonts-extra
        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add        
        sudo apt-get install google-chrome-stable    
        wget https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip
        unzip ./chromedriver_linux64.zip           
      
    - name: Run!      
      run: |        
        python main.py ${{scerets.MEMBER_ID}} ${{scerets.MEMBER_PW}}
```
`Note` : 아래 main.py의 수정1과 수정2를 본인의 동행복권 아이디와 패스워드로 변경해주세요.

`main.py`. 
```
from playwright.sync_api import Playwright, sync_playwright
import time

# 동행복권 아이디와 패스워드를 설정
USER_ID = '<아이디>'   # 수정1  
USER_PW = '<비밀번호>' # 수정2

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
    #page.click('#num2 >> text=자동번호발급')

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
```
### 동작 확인하기
lotto-action 저장소에 위에 작성한 action.yml와 buy_lotto.py 2개의 파일을 업로드 합니다.  
금요일 오전 08:30분에 동작합니다. (실행 시간은 약 2분 소요, Action 시간이 느려서 정확한 시간대에 실행은 조금 어렵습니다.)  
Actions 탭에서 실행 결과를, 로또 마이페이지에서 구매 결과를 확인할 수 있습니다.  
