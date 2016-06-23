CATEGORY='Category:English footballers'
REQUEST_LIMIT=50

import ceterach, getpass

def getteam(text,param):
    param=text.split('| '+param)[1].split('\n')[0].strip(' =[]')
    return param.split('|')[0] if '|' in param else param
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
mw=ceterach.api.MediaWiki(api_url='http://en.wikipedia.org/w/api.php')
print('Username: ',end='')
username=input()
password=getpass.getpass()
mw.login(username,password)
result=mw.call(prop='revisions', rvprop='content', generator='categorymembers', gcmtitle=CATEGORY, gcmprop='title', gcmlimit=REQUEST_LIMIT)
pages=result['query']['pages'].values()
cont=result['continue']['gcmcontinue']
while cont:
    for page in pages:
        if any([i in page['revisions'][0]['*'].upper() for i in ("{{BOTS","{{NOBOTS","TEMPLATE:BOTS","TEMPLATE:NOBOTS")]):
            continue
        while True:
            text=page['revisions'][0]['*']
            name=page['title']
            teams=getteams(text)
            print(name)
            ischange=False
            for team in teams:
                if '[[Category:{} players]]'.format(team) not in text:
                    text=text+'[[Category:{} players]]'.format(team)
                    ischange=True
            if ischange:
                try:
                    mw.page(name).edit(text,summary='bot testing edit',bot=True)
                    print('done editing')
                    break
                except ceterach.exceptions.EditConflictError:
                    print('edit conflict')
            else:
                print('no teams to add')
    result=mw.call(prop='revisions', rvprop='content', generator='categorymembers', gcmtitle=CATEGORY, gcmprop='title', gcmlimit=REQUEST_LIMIT)
    pages=result['query']['pages'].values()
    cont=result['continue']['gcmcontinue']
