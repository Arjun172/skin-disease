#create python env 
python3 -m venv skinprediction

# Activate the virtual environment
. .\skinprediction\Scripts\Activate

# Function to check if a library is installed
function Is-LibraryInstalled($library) {
    $result = Get-Command $library -ErrorAction SilentlyContinue
    return $result -ne $null
}

# Check and install each library
$libraries = @("pandas", "numpy", "keras-preprocessing", "fpdf", "flask", "tensorflow", "opencv-python", "matplotlib")

foreach ($lib in $libraries) {
    if (-not (Is-LibraryInstalled $lib)) {
        Write-Host "$lib is not installed. Installing $lib..."
        pip install $lib
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to install $lib. Please try installing it manually and run the script again."
            exit
        }
    }
}

# Display a message indicating that all dependencies are installed
Write-Host "All dependencies are installed."

# Run final.py
python .\final.py
