CATEGORY='Category:Scottish footballers'
REQUEST_LIMIT=50

import ceterach, getpass, re

def getteam(text,param):
    val=text.split('| '+param)[1].split('|')[0]
    val=val.split('[')[-1].split(']')[0] if '[' in val else val.strip(' =\n')
    val=val.strip()
    return val
def getteams(text):
    teams=[]
    for i in range(1,41):
        try:
            teams.append(getteam(text,'clubs'+str(i)))
        except IndexError:
            break
    try:
        teams.append(getteam(text,'currentclub'))
    except IndexError: pass
    return [i for i in teams if i]
mw=ceterach.api.MediaWiki(api_url='https://en.wikipedia.org/w/api.php')
print('Username: ',end='')
username=input()
password=getpass.getpass()
mw.login(username,password)
ignore=set([i[1:] for i in ceterach.page.Page(mw,'Wikipedia:WikiProject_Football/Missing_categories/Null').content.split('\n') if i and i[0]=='*'])
result=mw.call(prop='revisions', rvprop='content', generator='categorymembers', gcmtitle=CATEGORY, gcmprop='title', gcmlimit=REQUEST_LIMIT)
pages=result['query']['pages'].values()
cont=result['continue']['gcmcontinue']
count=0
discrepancies=0
names=[]
while True:
    for page in pages:
        count+=1
        if count%500==0:
            print(str(discrepancies)+' out of '+str(count)+' articles have discrepancies so far.')
        text=page['revisions'][0]['*']
        name=page['title']
        infoboxteams=set([[i for i in j if i][0] for j in re.findall(r'\|\s*clubs\d+\s*=\s*(?:([a-zA-Z0-9().,][a-zA-Z0-9()., ]+[a-zA-Z0-9().,])|(?:\[\[([^]|]+)\|[^]]+\]\]))',text)])-ignore
        catteams=set(re.findall(r'\[\[Category:([^]]+?) (?:wartime guest )?(?:players|footballers)\]\]',text))-ignore
        if infoboxteams-catteams:
            discrepancies+=1
            names.append('[['+name+']]: '+', '.join(infoboxteams-catteams))
    result=mw.call(gcmcontinue=cont,prop='revisions', rvprop='content', generator='categorymembers', gcmtitle=CATEGORY, gcmprop='title', gcmlimit=REQUEST_LIMIT)
    pages=result['query']['pages'].values()
    try:
        cont=result['continue']['gcmcontinue']
    except:
        break
print("total discrepancies:")
print(str(discrepancies)+'/'+str(count))
text="\n\n".join(names)
page=ceterach.page.Page(mw,"User:KSFT bot/Football/"+CATEGORY)
try:
    page.edit(text,"[[User:KSFT bot|Bot task 1]]: Update list.")
except ceterach.exceptions.NonexistentPageError:
    page.create(text,"[[User:KSFT bot|Bot task 1]]: Update list.")
