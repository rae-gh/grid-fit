import platform
import psutil
import sys
import numpy as np
import scipy

def get_system_info():
    """Collect comprehensive system information for benchmark documentation"""
    
    info = {
        # CPU info
        'cpu_model': platform.processor(),
        'cpu_physical_cores': psutil.cpu_count(logical=False),
        'cpu_logical_cores': psutil.cpu_count(logical=True),
        'cpu_freq_mhz': psutil.cpu_freq().max if psutil.cpu_freq() else None,
        
        # Memory
        'ram_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        
        # OS
        'os': platform.system(),
        'os_version': platform.version(),
        'platform': platform.platform(),
        
        # Python environment
        'python_version': sys.version,
        'python_implementation': platform.python_implementation(),
        
        # Package versions
        'numpy_version': np.__version__,
        'scipy_version': scipy.__version__,
        # 'gridfit_version': gridfit.__version__,  # add your library
        
        # Hostname (useful for HPC vs laptop identification)
        'hostname': platform.node(),
    }
    
    return info

# Usage:
if __name__ == "__main__":
    import json
    system_info = get_system_info()
    print(json.dumps(system_info, indent=2))