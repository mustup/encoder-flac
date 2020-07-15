import setuptools


packages = setuptools.find_namespace_packages(
)

setuptools.setup(
    install_requires=[
        'mustup_core == 0.1',
    ],
    name='mustup_encoder_flac',
    packages=packages,
    python_requires='>= 3.8',
    version='0.1',
    zip_safe=False, # due to namespace package
)
