import shutil

programmeFiles = [
    'armee.md',
    'energie.md'
];

with open('README.md','wb') as wfd:
    with open('header.md','rb') as fd:
        shutil.copyfileobj(fd, wfd);
    for f in programmeFiles:
        with open('programme/' + f,'rb') as fd:
            shutil.copyfileobj(fd, wfd);
