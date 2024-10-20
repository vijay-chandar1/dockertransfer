import subprocess
import os
import zipfile
import tempfile
import shutil
import stat

# Path to the zip file containing the dependencies
ZIP_PATH = '/workspaces/dockertransfer/dependencies.zip'

def setup_dependencies():
    # Create a temporary directory to extract the dependencies
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Debug: Print the directory structure for verification
    for root, dirs, files in os.walk(temp_dir):
        print("Directory:", root)
        print("Subdirectories:", dirs)
        print("Files:", files)

    return temp_dir

def set_executable_permissions(bin_dir):
    try:
        # Use chmod to recursively set execute permissions for all files in the directory
        subprocess.run(['chmod', '-R', 'a+x', bin_dir], check=True)
        print(f"Set execute permissions for all files in: {bin_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error setting permissions: {e}")

def run_ocr(input_pdf, output_pdf, temp_dir):
    # Construct paths to the dependencies
    dependency_path = os.path.join(temp_dir, 'package')

    # Paths to bin and non-Python dependencies
    bin_dir = os.path.join(dependency_path, 'bin')
    lib_dir = os.path.join(dependency_path, 'lib')

    # Update LD_LIBRARY_PATH to include the extracted lib directory
    os.environ['LD_LIBRARY_PATH'] = f"{lib_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"

    # Ensure that the binaries/scripts have execute permission
    set_executable_permissions(bin_dir)

    # Run the OCRmyPDF command using the Python interpreter from the virtual environment
    python_executable = '/workspaces/dockertransfer/myenv/bin/python'  # Update this to the correct path to your venv's Python interpreter

    try:
        subprocess.run(
            [python_executable, '-m', 'ocrmypdf', input_pdf, output_pdf],  # Use virtual environment's Python
            check=True,
            env=os.environ
        )
        print(f"OCR successfully completed: {output_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"Error during OCR: {e}")
    except FileNotFoundError:
        print("The 'ocrmypdf' command was not found. Please check the extracted dependencies or your Python environment.")

def cleanup_dependencies(temp_dir):
    # Remove the temporary directory
    shutil.rmtree(temp_dir)
    print("Cleaned up temporary dependencies.")

if __name__ == '__main__':  
    # Define the input and output PDFs
    input_pdf = '/workspaces/dockertransfer/input.pdf'  # Replace with your input PDF
    output_pdf = '/workspaces/dockertransfer/output.pdf'  # Define your desired output PDF name

    # Extract dependencies, run OCR, and clean up
    temp_dir = setup_dependencies()
    try:
        run_ocr(input_pdf, output_pdf, temp_dir)
    finally:
        cleanup_dependencies(temp_dir)
