search_text = "hello world"
print("SELECT * FROM events where name like '%%%s%%' order by date, time;" % search_text)