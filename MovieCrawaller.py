import requests as rq

res = rq.get("https://movie.naver.com/movie/point/af/list.naver?&page=1")
res.raise_for_status()

print(len(res.text))

with open("res_crawl.html", "w", encoding="utf8") as f:
    f.write(res.text)