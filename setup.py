from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(filepath:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements=[]
    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements


setup(
    name="skin-cancer-detection",
    version="0.1",
    author="SBagh",
    author_email="sbaghusa@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirement.txt'),
    )