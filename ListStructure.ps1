# Usage: .\ListStructure.ps1 -Path "C:\Project1"
# Usage: PowerShell.exe -ExecutionPolicy Bypass -File "C:\Tools\ListStructure.ps1" -Path "C:\GitHub\learn-reactjs-in-2023\taskmanager" -ExcludedFolders ".next", "node_modules"
# Usage: PowerShell.exe -ExecutionPolicy Bypass -File "D:\TSA\travels-flask-azoai-api\scripts\ListStructure.ps1" -Path "D:\TSA\travels-flask-azoai-api"
param (
    [string]$Path = (Get-Location),
    [string[]]$ExcludedFolders = @("node_modules", ".next", "bin", "obj", "__pycache__", ".venv", "appenv", "venv", "backend_env", "env", ".env", "notes" )
)

function List-DirectoryStructure {
    param (
        [string]$Path,
        [string]$Indent = ''
    )
    
    $items = Get-ChildItem $Path

    foreach ($item in $items) {
        # Check if the current item should be excluded
        if ($item.Name -in $ExcludedFolders) {
            continue  # Skip this folder
        }

        Write-Host "$Indent- $($item.Name)"

        if ($item.PSIsContainer) {
            List-DirectoryStructure -Path $item.FullName -Indent "$Indent  "
        }
    }
}

Write-Host $Path
List-DirectoryStructure -Path $Path
