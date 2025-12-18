from setuptools import setup, find_packages

setup(
    name='eyegymnastics',
    version='1.0',
    py_modules=['example_05_pomodoro_timer'],
    packages=find_packages(),
    install_requires=[
        "colormath>=3.0.0",
        "numpy>=2.2.6",
        "pygame>=2.6.1",
        "PyOpenGL>=3.1.10",
        "opencv-python>=4.12.0.88"
    ],
    include_package_data=True,
    package_data={
        'eyegymnastics': ['data/*.json', 'examples/*.py'],
    },
    entry_points={
        'console_scripts': [
            'eyegymnastics=eyegymnastics.cli:main',
            'eyegym=eyegymnastics.cli:main',  # короткий алиас
        ],
    }
)

