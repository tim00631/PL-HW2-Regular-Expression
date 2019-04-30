import urllib.request
import re
import matplotlib.pyplot as plt
import numpy as np

author = str()

def get_pages():
    '''
    This function is aim to get all the result from arxiv website, and return html_str (a html format string) to the caller.
    '''
    global author # input 
    author = input("Input Author:")
    print("Input Author:[" + author + ']')
    args = str(author).replace(" ", "+").strip() # 處理字串,符合url的格式
    # print(args)
    start = 0
    url = "https://arxiv.org/search/?query=" + args + "&searchtype=author&size=50&abstracts=show&start=" + str(start)
    # size = 50 每頁50筆資料
    # start : 每頁開頭要從第幾筆資料開始列出
    content = urllib.request.urlopen(url)
    html_str = content.read().decode('utf-8') # 轉成utf-8 格式
    start = start + 50
    # 以下開始loop尋找下一頁, 並加入到html_str裡, 直到無下一頁為止
    nexturl = "https://arxiv.org/search/?query=" + args + "&searchtype=author&size=50&abstracts=show&start=" + str(start)
    content = urllib.request.urlopen(nexturl)
    next_html_str = content.read().decode('utf-8')
    pattern = 'is-size-4 has-text-warning' # 停止的條件
    result = re.findall(pattern, next_html_str)
    
    while (not result): # result 不為空
        html_str = html_str + next_html_str # 加入html_str
        start = start + 50 # 重複剛剛動作
        nexturl = "https://arxiv.org/search/?query=" + args + "&searchtype=author&size=50&abstracts=show&start=" + str(start)
        content = urllib.request.urlopen(nexturl)
        next_html_str = content.read().decode('utf-8')
        result = re.findall(pattern, next_html_str)
    return html_str
def year_stat():
    print("Now, in Problem 1, input an author, I will draw the bar graph of the number of papers been published each year of an author.")
    html_str = get_pages()
    pattern = 'originally announced</span>[\s\S]*?</p>' # 發表年份的 pattern
    year_list = re.findall(pattern, html_str)
    year = list()
    for y in year_list:
        element = y.split('originally announced</span>')[1].split("</p>")[0].split()[1].split(".")[0] # 字串處理 切頭切尾留中間
        year.append(element)
    No_duplicate_year = list(set(year)) # 不重複的 year list, 用來做 counting
    No_duplicate_year.sort()
    # print(No_duplicate_year)
    year_count = list()
    for i in No_duplicate_year:
        year_count.append(year.count(i)) # Counting...
    # print(year)
    # print(year_count)
    plt.bar(No_duplicate_year, year_count)  # matplotlib bar function
    if(year_count):
        plt.yticks(np.arange(0, max(year_count) + 1, 1))  # 調整y軸刻度
        plt.show()
    else:
        print('the author is not exist...')
    
def co_author_finder():
    print("\nNow, in Problem 2, input an author, I will count the number of papers written together of each co-author.")
    html_str = get_pages()
    pattern = 'Authors:</span>[\s\S]*?</p>' # Author pattern
    author_list = re.findall(pattern, html_str)
    co_author_list = list()
    for a in author_list:
        pattern = '\">[\s\S]*?</a>' 
        co_author_name_list_per_paper = re.findall(pattern, str(a)) # 將每篇 paper 的所有 author 先存到 co_author_name_list_per_paper
        for i in co_author_name_list_per_paper:
            name = i.split("\">")[1].split('</a>')[0].strip() # 再將每個 author 存到 co_author_list
            if name != author: # 扣除本人
                co_author_list.append(name)
    No_duplicate_author = list(set(co_author_list)) # 不重複的author list, 用來做counting
    No_duplicate_author.sort()
    for j in No_duplicate_author:
        print('[' + j + ']:' + str(co_author_list.count(j)) + " times") # Counting...

# def find_title(): # Debug 用
#     html_str = get_pages()
#     pattern = 'title is-5 mathjax[\s\S]*?</p>'
#     title_list = re.findall(pattern, html_str)
#     for t in title_list:
#         title = t.split("title is-5 mathjax\">")[1].split("</p>")[0].strip()
#         print(title)

if __name__ == '__main__':
    year_stat() # Problem 1.
    co_author_finder() # Problem 2.
    # find_title() # Debug 用
