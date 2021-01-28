from setuptools import setup

setup(name='celebritysoulm8',
      version='0.1',
      description='Twitter bot which compares twitter uses based on language usage and sentiment analysis',
      url='https://github.com/doogyb/celebritysoulm8',
      author='Samuel Doogan',
      author_email='samueldoogan@gmail.com',
      packages=['celebritysoulm8'],
      entry_points={
            "console_scripts": [
                  "celebritysoulm8=celebritysoulm8.main:main",
            ],
      },
      zip_safe=False)
