import setuptools

def read(file):
    with open(file) as f:
        content = f.read()
    return content

setuptools.setup(
    name='MOITA',
    version='1.0.0',
    description='Matrícula Otimizada/Iteração de Todas as Alternativas',
    url='https://github.com/ranisalt/moita',
    author='Ranieri Althoff',
    author_email='ranisalt@gmail.com',
    license='GNU Affero General Public License v3 or later',
    install_requires=read('requirements.txt'),
    test_suite='tests'
)
