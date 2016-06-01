import shutil
import pypandoc


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
]


def generate_readme(for_pdf):
    with open('README.md', 'wb') as wfd:
        if for_pdf:
            with open('programme/header.md') as head:
                head_txt = head.read()
                head_txt = head_txt.partition('<p align="center"><img src="/annexes/photo.jpg" alt="Vincent Lamotte" title="Photo de Vincent Lamotte" width="300"></p>')
                wfd.write(bytes(head_txt[0], encoding='utf-8'))
                wfd.write(bytes('![Vincent Lamotte](annexes/photo.jpg){#id '
                                '.class '
                          'width=280 text-align=center}', encoding='utf-8'))
                wfd.write(bytes(head_txt[2], encoding='utf-8'))
        else:
            programmeFiles.insert(0, 'header.md')
        for f in programmeFiles:
            with open('programme/' + f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd)


if __name__ == '__main__':
    generate_readme(for_pdf=True)
    pypandoc.convert('README.md',
                     'pdf',
                     outputfile="ProgrammeVincentLamotte2017.pdf",
                     extra_args=['-V',
                                 'geometry:margin=2.5cm'])
    generate_readme(for_pdf=False)
