from setuptools import setup

version = {}
with open("cv_plinko/version.py") as f:
    exec(f.read(), version)

setup(name='cv_plinko',
      version=version['__version__'],
      description='Turn images & videos into plinko boards.',
      author='Adam Spannbauer',
      author_email='spannbaueradam@gmail.com',
      url='https://github.com/AdamSpannbauer/cv_plinko',
      packages=['cv_plinko'],
      license='MIT',
      install_requires=[
          'numpy',
          'imutils',
      ],
      extras_require={
          'cv2': ['opencv-contrib-python >= 3.4.0']
      },
      keywords=['computer vision', 'image processing', 'opencv'],
      )
