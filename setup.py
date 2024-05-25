from setuptools import setup, find_packages

setup(
    name="celes_ibio",
    version="0.1.0",  
    description="Prueba tecnica para ingresar a celes",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    author="Ibio Antonio Escobar Gomez",  
    author_email="ibiotec30@gmail.com",  
    url="https://github.com/ibioEsco/Celes", 
    packages=find_packages(), 
    include_package_data=False,  
    install_requires=[ 
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-jose",
        "passlib[bcrypt]",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.9',  
)
