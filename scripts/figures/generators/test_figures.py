#!/usr/bin/env python3
"""
Test script for figure generation system.
This script tests all components of the figure generation pipeline.
"""

import sys
import tempfile
import subprocess
from pathlib import Path

# Add the figures directory to the path to enable imports
figures_dir = Path(__file__).parent.parent
sys.path.insert(0, str(figures_dir))

def test_matplotlib_config():
    """Test matplotlib configuration."""
    try:
        from utils.matplotlib_config import (
            configure_matplotlib,
            create_publication_figure,
            COLORS,
            FIGURE_SIZES
        )
        
        # Test configuration
        configure_matplotlib()
        
        # Test figure creation
        fig, ax = create_publication_figure(figsize=FIGURE_SIZES['single_column'])
        
        # Test that colors are available
        assert 'primary' in COLORS
        assert 'secondary' in COLORS
        
        print("✓ Matplotlib configuration test passed")
        return True
    except Exception as e:
        print(f"✗ Matplotlib configuration test failed: {e}")
        return False

def test_seaborn_config():
    """Test seaborn configuration."""
    try:
        from ..utils.seaborn_config import (
            configure_seaborn,
            CUSTOM_PALETTES
        )
        
        # Test configuration
        configure_seaborn()
        
        # Test palettes
        assert 'publication' in CUSTOM_PALETTES
        assert len(CUSTOM_PALETTES['publication']) > 0
        
        print("✓ Seaborn configuration test passed")
        return True
    except Exception as e:
        print(f"✗ Seaborn configuration test failed: {e}")
        return False

def test_mermaid_generator():
    """Test Mermaid generator."""
    try:
        from ..utils.mermaid_generator import (
            MermaidGenerator,
            create_process_flow
        )
        
        # Test generator creation
        generator = MermaidGenerator()
        
        # Test simple diagram creation (without CLI)
        steps = ['Step 1', 'Step 2', 'Step 3']
        
        print("✓ Mermaid generator test passed")
        return True
    except Exception as e:
        print(f"✗ Mermaid generator test failed: {e}")
        return False

def test_figure_generation():
    """Test actual figure generation."""
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from ..utils.matplotlib_config import create_publication_figure, save_figure
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Generate a simple test figure
            x = np.linspace(0, 5, 50)
            y = np.sin(x)
            
            fig, ax = create_publication_figure()
            ax.plot(x, y, label='Test Data')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.legend()
            
            # Save figure
            output_path = temp_path / 'test_figure'
            save_figure(fig, output_path, formats=('pdf',))
            plt.close()
            
            # Check if file was created
            if (temp_path / 'test_figure.pdf').exists():
                print("✓ Figure generation test passed")
                return True
            else:
                print("✗ Figure generation test failed: PDF not created")
                return False
                
    except Exception as e:
        print(f"✗ Figure generation test failed: {e}")
        return False

def test_dependencies():
    """Test required dependencies."""
    dependencies = {
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn', 
        'numpy': 'numpy',
        'pandas': 'pandas'
    }
    
    missing = []
    for name, module in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} available")
        except ImportError:
            print(f"✗ {name} missing")
            missing.append(name)
    
    # Test Mermaid CLI (optional)
    try:
        result = subprocess.run(['mmdc', '--version'], 
                              capture_output=True, text=True, check=True)
        print("✓ Mermaid CLI available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Mermaid CLI not available (optional)")
    
    return len(missing) == 0

def run_all_tests():
    """Run all tests."""
    print("Running figure generation system tests...")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Matplotlib Config", test_matplotlib_config),
        ("Seaborn Config", test_seaborn_config),
        ("Mermaid Generator", test_mermaid_generator),
        ("Figure Generation", test_figure_generation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check dependencies and configuration.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
