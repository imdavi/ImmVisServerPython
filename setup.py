from setuptools import setup

setup(name='immvis-server',
      version='0.1',
      description='The server component from ImmVis',
      author='Felipe Pedroso',
      author_email='f.pedroso677@gmail.com',
      license='MIT',
      package='immvis',
      install_requires=[
          'pandas',
          'protobuf',
          'grpcio',
          'grpcio-tools',
          'numpy',
          'xlrd',
          'sklearn'
      ],
      zip_safe=False)