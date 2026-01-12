"""
analytics module initialization
"""

from .data_processing import DataProcessor
from .dashboard import dashboard_bp

__all__ = ['DataProcessor', 'dashboard_bp']
__version__ = '1.0.0'