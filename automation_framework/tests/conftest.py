import os
import pytest

@pytest.fixture(autouse=True)
def setup_environment():
    """Set up environment variables for tests"""
    os.environ['OPENWEATHER_API_KEY'] = 'f88d54cd8eddb5d1f23ff82a80b95fec'
    yield
    # Clean up after tests if needed
    if 'OPENWEATHER_API_KEY' in os.environ:
        del os.environ['OPENWEATHER_API_KEY'] 