# ExeToBin.ps1 - Convert EXE to Base64/Hex
# Usage: .\ExeToBin.ps1 -InputFile "path\to\file.exe" [-OutputFormat Base64|Hex]

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("Base64", "Hex", "Both")]
    [string]$OutputFormat = "Base64",
    
    [Parameter(Mandatory=$false)]
    [string]$OutputFile
)

# Colors
$SuccessColor = "Green"
$ErrorColor = "Red"
$InfoColor = "Cyan"

function Write-ColorOutput {
    param([string]$Message, [string]$Color)
    Write-Host $Message -ForegroundColor $Color
}

# Check if file exists
if (-not (Test-Path $InputFile)) {
    Write-ColorOutput "[ERROR] File not found: $InputFile" $ErrorColor
    exit 1
}

# Get file info
$fileInfo = Get-Item $InputFile
$fileSize = $fileInfo.Length

Write-ColorOutput "[INFO] Processing: $($fileInfo.Name)" $InfoColor
Write-ColorOutput "[INFO] File size: $([math]::Round($fileSize / 1KB, 2)) KB" $InfoColor

# Read file as bytes
$fileBytes = [System.IO.File]::ReadAllBytes($InputFile)

switch ($OutputFormat) {
    "Base64" {
        $encoded = [Convert]::ToBase64String($fileBytes)
        $extension = ".b64"
        
        Write-ColorOutput "[SUCCESS] Base64 conversion complete" $SuccessColor
        
        if ($OutputFile) {
            $encoded | Out-File -FilePath $OutputFile -Encoding UTF8
            Write-ColorOutput "[SAVED] Output: $OutputFile" $SuccessColor
        } else {
            Write-ColorOutput "[OUTPUT] Base64 String:" $InfoColor
            Write-ColorOutput ("-" * 60) Gray
            $encoded
            Write-ColorOutput ("-" * 60) Gray
            Write-ColorOutput "[INFO] Total characters: $($encoded.Length)" $InfoColor
        }
    }
    
    "Hex" {
        $hexString = [BitConverter]::ToString($fileBytes) -replace '-', ' '
        $extension = ".hex"
        
        Write-ColorOutput "[SUCCESS] Hex conversion complete" $SuccessColor
        
        if ($OutputFile) {
            $hexString | Out-File -FilePath $OutputFile -Encoding UTF8
            Write-ColorOutput "[SAVED] Output: $OutputFile" $SuccessColor
        } else {
            Write-ColorOutput "[OUTPUT] Hex String:" $InfoColor
            Write-ColorOutput ("-" * 60) Gray
            $hexString
            Write-ColorOutput ("-" * 60) Gray
            Write-ColorOutput "[INFO] Total characters: $($hexString.Length)" $InfoColor
        }
    }
    
    "Both" {
        $base64 = [Convert]::ToBase64String($fileBytes)
        $hexString = [BitConverter]::ToString($fileBytes) -replace '-', ' '
        
        Write-ColorOutput "[SUCCESS] Both conversions complete" $SuccessColor
        
        Write-ColorOutput "[OUTPUT] Base64 String:" $InfoColor
        Write-ColorOutput ("-" * 60) Gray
        $base64
        Write-ColorOutput ("-" * 60) Gray
        
        Write-ColorOutput "`n[OUTPUT] Hex String:" $InfoColor
        Write-ColorOutput ("-" * 60) Gray
        $hexString
        Write-ColorOutput ("-" * 60) Gray
        
        if ($OutputFile) {
            $combined = @"
=== BASE64 OUTPUT ===
$base64

=== HEX OUTPUT ===
$hexString
"@
            $combined | Out-File -FilePath $OutputFile -Encoding UTF8
            Write-ColorOutput "[SAVED] Output: $OutputFile" $SuccessColor
        }
    }
}

Write-ColorOutput "`n[COMPLETE] Conversion finished successfully!" $SuccessColor
