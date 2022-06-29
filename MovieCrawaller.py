import requests as rq
import csv
import time
from bs4 import BeautifulSoup as bs
 
page_cnt = 100  # 크롤링할 페이지 개수
row_n = 10  # 한 페이지당 댓글 개수
count = 1  # 크롤링한 자료 개수

with open("samples.csv", "w", encoding="utf-8") as fd:    # 파일이 open
    writer = csv.writer(fd)
    writer.writerow(["movie", "sentence", "score"])
    i = 1  # 페이지 번호 변수
    start = time.time()
    while i <= page_cnt:  # 페이지 번호가 크롤링할 페이지의 최대 수랑 같아 질때 까지 루프 반복
        try:
            if int(time.time() - start) > 80:  # 네트워크 문제로 무한루프에 빠질 경우를 대비, 루프 시작 후 80초 후에는 종료
                break
            url = "https://movie.naver.com/movie/point/af/list.naver?&page=" + str(i)
            res = rq.get(url) # 각 페이지의 html 소스코드를 가져옴

        except rq.exceptions.ConnectionError as ec:  # 연결 오류 시 fail 메세지를 출력하고 1개의 추가 페이지를 크롤링
            print("Connection error: ", ec)
            page_cnt += 1
            i+=1
            time.sleep(0.5)
            continue

        except rq.exceptions.Timeout as et:  # 타임아웃 오류 시 fail 메세지를 출력하고 1개의 추가 페이지를 크롤링
            print("Timeout error: ", et)
            page_cnt += 1
            i+=1
            time.sleep(0.5)
            continue

        except rq.exceptions.HTTPError as eh:  # HTTP 오류 시 fail 메세지를 출력하고 1개의 추가 페이지를 크롤링
            print("HTTP error: ", eh)
            page_cnt += 1
            i+=1
            time.sleep(0.5)
            continue

        except rq.exceptions.RequestException as err:  # 기타 오류 시 fail 메세지를 출력하고 1개의 추가 페이지를 크롤링
            print("Unknown error: ", err)
            page_cnt += 1
            i+=1
            time.sleep(0.5)
            continue

        i+=1
        time.sleep(0.5) # 1개의 페이지를 가져오고 나서 0.5초 대기        
        soup = bs(res.text, "html.parser") # bs 객체선언
        flag = soup.find("tbody").find("tr") # tbody 블럭 안에 tr블럭들을 순차적으로 가져오기 위한 시작 지점

        for j in range(row_n):
            movie = flag.find("a", attrs={"class":"movie color_b"})
            score = flag.find("em")
            sentence = flag.find("br").next_element.get_text().strip()  # 작성하지 않은 부분에 대한 공백 처리 
            flag = flag.find_next_sibling("tr")  # 다음 tr블럭의 위치를 지정
            if sentence == "":  # 빈 리뷰인 경우 수집 하지 않음
                continue
            writer.writerow([movie.get_text(), sentence, score.get_text()])
            count += 1

        print("Success!! from: {}.... {}개 수집 완료....".format(url, count))  # 루프가 끝날 때 마다 크롤링한 자료 개수, 경과 시간 출력

print("Done!!")