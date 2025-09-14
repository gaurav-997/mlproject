from setuptools import find_packages,setup
from typing import List

hyphen_e_dot = "-e ."
def get_packages(file_path:str) -> List[str]:
    """ this function will return the list of requirments"""
    requirments = []
    with open(file_path,"r") as file:
        requirments = file.readlines()
        requirments = [i.replace("\n" ,"") for i in  requirments ]  # each line is adding a new line in readlines so replace it 
        
        if hyphen_e_dot in requirments:
            requirments.remove(hyphen_e_dot)
        
    return requirments
        

setup(
    name="mlproject",
    author= "Gaurav Chauhan",
    author_email="chauhan7gaurav@gmail.com",
    version='0.0.1',
    packages=find_packages(),
    install_requires = get_packages("requirments.txt")
)