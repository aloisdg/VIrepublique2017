import shutil


programmeFiles = [
    'header.md',
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
]


def generate_readme():
    with open('README.md', 'wb') as wfd:
        for f in programmeFiles:
            with open('programme/' + f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)


if __name__ == '__main__':
    generate_readme()
