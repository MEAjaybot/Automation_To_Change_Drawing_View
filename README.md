# Automation to Change Drawing View

A Python-based automation tool that converts existing CadQuery scripts from the **XY plane to XZ or YZ planes** by applying predefined code transformations.

The project automates changes to workplanes, extrusion directions, face and edge selectors, hole positions, groove geometry and other geometry-related operations. It also supports parallel processing of multiple Python files.

## Features

- **Multiple Drawing Views:** Convert models into XZ or YZ orientations.
- **Automated Code Transformation:** Uses Python regular expressions to modify CadQuery scripts.
- **Workplane Conversion:** Changes XY workplanes to the selected target plane.
- **Extrusion Direction:** Adjusts extrusion directions according to the selected view.
- **Geometry Adjustments:** Updates face selectors, edge selectors, groove operations, hole coordinates and drill-hole geometry.
- **Parallel Processing:** Uses `ProcessPoolExecutor` to process multiple Python files concurrently.
- **Output Organization:** Stores converted scripts in separate folders for each view.
- **3D Visualization:** Executes converted scripts and displays generated models using OCP CAD Viewer.

## Project Structure

```text
Automation_To_Change_Drawing_View/
│
├── input/
│   └── *.py                  # Original CadQuery scripts
│
├── outcome/
│   ├── XZ/                   # Converted XZ scripts
│   └── YZ/                   # Converted YZ scripts
│
├── main.py                   # Main execution and visualization
├── process.py                # Code transformation logic
├── requirements.txt          # Python dependencies
├── .env                      # Configuration
└── .gitignore
```

## Technologies Used

- Python
- CadQuery
- Regular Expressions (`re`)
- Multiprocessing (`ProcessPoolExecutor`)
- OCP CAD Viewer (`ocp_vscode`)
- pathlib and os

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MEAjaybot/Automation_To_Change_Drawing_View.git

cd Automation_To_Change_Drawing_View
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Add input files

Place the original CadQuery Python scripts inside the `input/` directory.

### 2. Select the drawing view

Set the `MODEL_VIEW` environment variable to select the target orientation.

**For XZ view:**

```env
MODEL_VIEW=XZ
```

**For YZ view:**

```env
MODEL_VIEW=YZ
```

The default view is XZ if no environment variable is provided.

### 3. Configure parallel workers

In `main.py`, configure the maximum number of worker processes:

```python
MAX_WORKERS = 5
```

Change this value depending on your available CPU resources.

### 4. Run the automation

```bash
python main.py
```

The program will:

1. Find Python files in the input directory.
2. Submit files to multiple worker processes.
3. Apply the required code transformations.
4. Save converted scripts in the selected output directory.
5. Execute the converted scripts.
6. Display the resulting 3D models using OCP CAD Viewer.

## Processing Workflow

```text
        Original CadQuery Scripts
                   |
                   v
             Input Directory
                   |
                   v
          Select Target View
              XZ / YZ
                   |
                   v
          Parallel Processing
          (ProcessPoolExecutor)
                   |
                   v
         Code Transformation
                   |
          +--------+--------+
          |                 |
          v                 v
       XZ Output         YZ Output
          |                 |
          +--------+--------+
                   |
                   v
          Execute Converted Code
                   |
                   v
             Generate 3D Model
                   |
                   v
             OCP CAD Viewer
```

## Parallel Processing

The project uses Python's `ProcessPoolExecutor` to distribute independent input files across multiple processes.

Each worker:
- Reads an input Python file.
- Applies the required regex-based transformations.
- Writes the converted script to the output directory.
- Returns the output file path.

Model execution and OCP CAD visualization are handled by the main process after the conversion tasks finish.

## Configuration

| Variable | Description |
|---|---|
| `MODEL_VIEW` | Target drawing orientation: XZ or YZ |
| `MAX_WORKERS` | Maximum number of parallel worker processes |
| `INPUT_DIR` | Directory containing original scripts |
| `OUTPUT_DIR` | Directory for converted scripts |

## Notes

- Input files should contain CadQuery scripts following the expected source-code patterns.
- The transformation rules are pattern-based and may require adjustments for scripts with different geometry definitions.
- The XZ and YZ configurations use different workplane and direction settings.
- Parallel processing applies to script conversion; model execution and visualization are performed sequentially.
- Existing output files may be skipped by the processing function.

## Future Improvements

- Support additional drawing orientations.
- Improve transformation handling for different CadQuery coding styles.
- Add validation to compare original and converted geometries.
- Improve error reporting for unsupported code patterns.
- Explore parallel model generation for larger datasets.

## Author

**Ajay B.K.**

GitHub: [@MEAjaybot](https://github.com/MEAjaybot)

## Repository

[Automation_To_Change_Drawing_View](https://github.com/MEAjaybot/Automation_To_Change_Drawing_View)
