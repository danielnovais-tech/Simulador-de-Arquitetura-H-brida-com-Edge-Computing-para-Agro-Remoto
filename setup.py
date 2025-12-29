from setuptools import setup, find_packages

setup(
    name="hybrid-edge-agro",
    version="1.0.0",
    description="Hybrid Edge Computing Architecture for Remote Agriculture",
    author="Daniel Novais",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "paho-mqtt>=1.6.1",
        "prometheus-client>=0.17.1",
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
        "kubernetes>=27.2.0",
        "chaostoolkit>=1.14.0",
        "pytest>=7.4.0",
        "asyncio>=3.4.3",
        "aiohttp>=3.8.5",
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "loguru>=0.7.0",
        "python-dotenv>=1.0.0",
        "netifaces>=0.11.0",
        "psutil>=5.9.5",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.1",
            "pytest-timeout>=2.1.0",
        ]
    },
)
