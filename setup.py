from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='streamlit-permalink',
    version='0.5.2',
    description='Effortless permalinks in Streamlit apps.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Franciszek Piszcz',
    author_email='franciszek.piszcz@rtbhouse.com',
    url='https://github.com/franekp/streamlit-permalink',
    py_modules=['streamlit_permalink'],
    install_requires=[
        'streamlit >= 1.4.0',
        'packaging >= 15.0',
    ],
    extras_require={
        'test': [
            'pytest>=8.0.0',
            'pytest-cov>=4.1.0',  # For coverage reporting
            'pytest-xdist>=3.5.0',  # For parallel testing
        ],
    },
    python_requires='>=3.8',  # Match Streamlit's minimum Python version
)
