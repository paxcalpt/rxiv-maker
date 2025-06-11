#!/usr/bin/env python3
"""
Generate Enhanced Mermaid diagrams for Article-Forge methodology and workflows.
This script creates comprehensive diagrams showing the template system.
"""

from pathlib import Path
import sys

# Add the figures directory to the path to enable imports
figures_dir = Path(__file__).parent.parent
sys.path.insert(0, str(figures_dir))

# Import after path setup for local modules
from utils.mermaid_generator import MermaidGenerator  # noqa: E402

def create_article_forge_workflow(output_dir: Path) -> None:
    """Create a comprehensive workflow diagram for Article-Forge."""
    
    workflow_mermaid = """
flowchart TD
    A[Author Creates Content] --> B[LaTeX Source Files]
    B --> C{Build System}
    C --> D[Figure Generation]
    C --> E[Bibliography Processing]
    C --> F[Style Application]
    
    D --> D1[Data Mining]
    D --> D2[Matplotlib Plots]
    D --> D3[Seaborn Analysis]
    D --> D4[Mermaid Diagrams]
    
    D1 --> D1a[Preprint Data Collection]
    D1 --> D1b[Statistical Analysis]
    D2 --> D2a[Growth Visualizations]
    D2 --> D2b[Repository Comparisons]
    D3 --> D3a[Correlation Analysis]
    D3 --> D3b[Distribution Plots]
    D4 --> D4a[Workflow Diagrams]
    D4 --> D4b[System Architecture]
    
    E --> E1[Reference Collection]
    E --> E2[Citation Processing]
    F --> F1[HenriquesLab Style]
    F --> F2[Typography & Layout]
    
    D1b --> G[Combined Figures]
    D2b --> G
    D3b --> G
    D4b --> G
    E2 --> H[Bibliography]
    F2 --> I[Styled Document]
    
    G --> J[LaTeX Compilation]
    H --> J
    I --> J
    
    J --> K[PDF Output]
    K --> L[Publication Ready]
    
    style A fill:#e1f5fe
    style K fill:#c8e6c9
    style L fill:#4caf50
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#f3e5f5
    """
    
    # Create the workflow diagram using MermaidGenerator
    generator = MermaidGenerator()
    output_path = output_dir / 'methodology_workflow.pdf'
    generator.generate_diagram(workflow_mermaid, output_path, format='pdf')

def create_figure_generation_process(output_dir: Path) -> None:
    """Create a detailed figure generation process diagram."""
    
    figure_process = """
flowchart LR
    subgraph "Data Sources"
        DS1[CrossRef API]
        DS2[arXiv Statistics]
        DS3[Repository Data]
        DS4[Growth Metrics]
    end
    
    subgraph "Data Processing"
        DP1[Data Mining Script]
        DP2[Statistical Analysis]
        DP3[Trend Calculation]
        DP4[Period Classification]
    end
    
    subgraph "Figure Generation"
        FG1[Matplotlib Config]
        FG2[Seaborn Setup]
        FG3[Mermaid Templates]
        FG4[Publication Styling]
    end
    
    subgraph "Output Types"
        OT1[Growth Analysis]
        OT2[Statistical Plots]
        OT3[Correlation Maps]
        OT4[Workflow Diagrams]
    end
    
    subgraph "Final Output"
        FO1[PDF Figures]
        FO2[PNG Figures]
        FO3[SVG Diagrams]
        FO4[LaTeX Integration]
    end
    
    DS1 --> DP1
    DS2 --> DP1
    DS3 --> DP2
    DS4 --> DP3
    
    DP1 --> DP4
    DP2 --> DP4
    DP3 --> DP4
    
    DP4 --> FG1
    DP4 --> FG2
    FG3 --> FG4
    
    FG1 --> OT1
    FG2 --> OT2
    FG2 --> OT3
    FG4 --> OT4
    
    OT1 --> FO1
    OT2 --> FO1
    OT3 --> FO2
    OT4 --> FO3
    
    FO1 --> FO4
    FO2 --> FO4
    FO3 --> FO4
    
    style DS1 fill:#e8f5e8
    style DS2 fill:#e8f5e8
    style DS3 fill:#e8f5e8
    style DS4 fill:#e8f5e8
    style FO4 fill:#fff2cc
    """
    
    generator = MermaidGenerator()
    output_path = output_dir / 'figure_generation_process.pdf'
    generator.generate_diagram(figure_process, output_path, format='pdf')

def create_system_architecture(output_dir: Path) -> None:
    """Create a system architecture diagram."""
    
    architecture = """
graph TB
    subgraph "User Interface"
        UI1[Author Workspace]
        UI2[Development Environment]
        UI3[VS Code Integration]
    end
    
    subgraph "Build System"
        BS1[Makefile]
        BS2[Shell Scripts]
        BS3[Python Scripts]
        BS4[Docker Container]
    end
    
    subgraph "Content Processing"
        CP1[LaTeX Engine]
        CP2[Bibliography Engine]
        CP3[Figure Engine]
        CP4[Style Engine]
    end
    
    subgraph "Data Sources"
        DS1[External APIs]
        DS2[Local Data]
        DS3[Template Files]
        DS4[Configuration]
    end
    
    subgraph "Output Generation"
        OG1[PDF Compilation]
        OG2[Figure Creation]
        OG3[Asset Management]
        OG4[Quality Control]
    end
    
    subgraph "Distribution"
        DT1[Local Build]
        DT2[GitHub Actions]
        DT3[Docker Registry]
        DT4[Release Management]
    end
    
    UI1 --> BS1
    UI2 --> BS2
    UI3 --> BS3
    
    BS1 --> CP1
    BS2 --> CP2
    BS3 --> CP3
    BS4 --> CP4
    
    DS1 --> CP3
    DS2 --> CP3
    DS3 --> CP4
    DS4 --> CP1
    
    CP1 --> OG1
    CP2 --> OG1
    CP3 --> OG2
    CP4 --> OG3
    
    OG1 --> DT1
    OG2 --> DT2
    OG3 --> DT3
    OG4 --> DT4
    
    style UI1 fill:#e3f2fd
    style UI2 fill:#e3f2fd
    style UI3 fill:#e3f2fd
    style DT4 fill:#e8f5e8
    """
    
    generator = MermaidGenerator()
    output_path = output_dir / 'system_architecture.pdf'
    generator.generate_diagram(architecture, output_path, format='pdf')

def create_collaboration_workflow(output_dir: Path) -> None:
    """Create a sequence diagram for collaboration workflow."""
    
    collaboration = """
sequenceDiagram
    participant A as Author
    participant G as Git Repository
    participant CI as GitHub Actions
    participant D as Docker
    participant S as System
    
    A->>G: Commit changes
    G->>CI: Trigger build
    CI->>D: Pull container
    D->>S: Execute build
    
    S->>S: Generate figures
    S->>S: Process bibliography
    S->>S: Compile LaTeX
    S->>S: Quality checks
    
    S->>CI: Build results
    CI->>G: Store artifacts
    G->>A: Notification
    
    Note over A,S: Automated publication pipeline
    
    A->>G: Create release tag
    G->>CI: Release workflow
    CI->>S: Production build
    S->>CI: Final PDF
    CI->>G: Create release
    
    Note over A,G: Publication ready
    """
    
    generator = MermaidGenerator()
    output_path = output_dir / 'collaboration_workflow.pdf'
    generator.generate_diagram(collaboration, output_path, format='pdf')

def create_data_flow_diagram(output_dir: Path) -> None:
    """Create a data flow diagram for the system."""
    
    data_flow = """
flowchart TD
    subgraph "Input Data"
        ID1[Raw LaTeX Files]
        ID2[Bibliography Data]
        ID3[Figure Specifications]
        ID4[Configuration Files]
    end
    
    subgraph "Processing Pipeline"
        PP1[Content Parser]
        PP2[Data Processor]
        PP3[Figure Generator]
        PP4[Style Processor]
    end
    
    subgraph "Quality Assurance"
        QA1[Syntax Validation]
        QA2[Figure Verification]
        QA3[Reference Checking]
        QA4[Format Compliance]
    end
    
    subgraph "Output Generation"
        OG1[Compiled PDF]
        OG2[Generated Figures]
        OG3[Processed Bibliography]
        OG4[Build Artifacts]
    end
    
    ID1 --> PP1
    ID2 --> PP2
    ID3 --> PP3
    ID4 --> PP4
    
    PP1 --> QA1
    PP2 --> QA3
    PP3 --> QA2
    PP4 --> QA4
    
    QA1 --> OG1
    QA2 --> OG2
    QA3 --> OG3
    QA4 --> OG4
    
    OG1 --> OG4
    OG2 --> OG4
    OG3 --> OG4
    
    style ID1 fill:#fff3e0
    style ID2 fill:#fff3e0
    style ID3 fill:#fff3e0
    style ID4 fill:#fff3e0
    style OG4 fill:#e8f5e8
    """
    
    generator = MermaidGenerator()
    output_path = output_dir / 'data_flow_diagram.pdf'
    generator.generate_diagram(data_flow, output_path, format='pdf')

if __name__ == '__main__':
    # Determine output directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'build' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating Enhanced Article-Forge methodology diagrams...")
    
    try:
        create_article_forge_workflow(output_dir)
        print("✓ Main workflow diagram created")
        
        create_figure_generation_process(output_dir)
        print("✓ Figure generation process created")
        
        create_system_architecture(output_dir)
        print("✓ System architecture diagram created")
        
        create_collaboration_workflow(output_dir)
        print("✓ Collaboration workflow created")
        
        create_data_flow_diagram(output_dir)
        print("✓ Data flow diagram created")
        
        print("All enhanced Mermaid diagrams generated successfully!")
        
    except Exception as e:
        print(f"Error generating Mermaid diagrams: {e}")
        sys.exit(1)
