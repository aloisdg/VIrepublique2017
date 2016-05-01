import shutil

programmeFiles = [
	'alimentaire.md',
    'armee.md',
	'culture.md',
	'ecologie.md',
	'economie.md',
	'education.md',
    'energie.md',
	'finance.md',
	'politique.md',
	'recherche.md',
	'sante.md',
	'securite.md',
	'technologie.md',
	'transport.md',
	'viepublique.md'
];

with open('README.md','wb') as wfd:
    with open('header.md','rb') as fd:
        shutil.copyfileobj(fd, wfd);
    for f in programmeFiles:
        with open('programme/' + f,'rb') as fd:
            shutil.copyfileobj(fd, wfd);
