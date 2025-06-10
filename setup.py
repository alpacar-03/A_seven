from setuptools import setup, find_packages

setup(
    name="rjb",
    version="0.1",
    packages=find_packages(),
    package_data={},
    install_requires=[
        'PyQt5',
        'dashscope',
        'requests',
    ],
    author="A_seven",
    description="基于开源AI大模型的教学实训智能体平台",
    python_requires=">=3.6",
) 