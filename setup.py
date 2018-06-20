from pathlib import Path

from setuptools import find_packages, setup

requirements = Path(__file__).parent / 'requirements/core.txt'

with requirements.open(mode='rt', encoding='utf-8') as fp:
    install_requires = [line.strip() for line in fp]

readme = Path(__file__).parent / 'README.rst'

with readme.open(mode='rt', encoding='utf-8') as fp:
    readme_text = fp.read()

setup(
    name='multi_rake',
    version='0.0.1',
    description='Multilingual Rapid Keyword Extraction (RAKE)',
    long_description=readme_text,
    keywords=['nlp', 'keywords', 'rake'],
    license='MIT',
    author='Vitaliy Grabovets',
    author_email='v.grabovets@gmail.com',
    url='https://github.com/vgrabovets/multi_rake',
    packages=find_packages(include=['multi_rake']),
    python_requires='>=3.5.0',
    install_requires=install_requires,
    include_package_data=True,
)
