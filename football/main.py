CATEGORY='Category:English footballers'
REQUEST_LIMIT=50

import ceterach, getpass, re

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
            #changed=False
            """for team in teams:
                cat='[[Category:{} players]]'.format(team)
                if cat not in text and mw.page(cat).exists:
                    text=text+cat
                    changed=True"""
            infoboxteams=['[[Category:{} players]]'.format(team) for team in teams]
            catteams=re.findall(r'\[\[Category:[^]]+ players\]\]',text)
            if set(infoboxteams)!=set(catteams):
                try:
                    #mw.page(name).edit(text,summary='bot testing edit',bot=True)
                    #print('done editing')
                    print(name+': discrepancy')
                except ceterach.exceptions.EditConflictError:
                    pass
                    #print('edit conflict')
            else:
                print(name+': no discrepancy')
    result=mw.call(prop='revisions', rvprop='content', generator='categorymembers', gcmtitle=CATEGORY, gcmprop='title', gcmlimit=REQUEST_LIMIT)
    pages=result['query']['pages'].values()
    cont=result['continue']['gcmcontinue']
