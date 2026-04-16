# ExeBin

Convert any executable (.exe) file to Base64, Hex, or Raw byte format.

## Features

- **Multiple Output Formats**: Convert to Base64, Hexadecimal, or Raw bytes
- **Cross-Platform Scripts**: Python GUI and PowerShell CLI versions
- **Lightweight**: No dependencies required for PowerShell version
- **Clipboard Support**: One-click copy to clipboard
- **File Export**: Save output to any text file

## Installation

### PowerShell (Recommended - No Dependencies)

```powershell
# Clone the repository
git clone https://github.com/wulcato/ExeBin.git
cd ExeBin

# Run directly
.\ExeToBin.ps1 -InputFile "path\to\your.exe"
```

### Python Version

```bash
# Requires Python 3.x
python exe2bin.py
```

## Usage

### PowerShell CLI

```powershell
# Convert to Base64
.\ExeToBin.ps1 -InputFile "notepad.exe" -OutputFormat Base64

# Convert to Hex
.\ExeToBin.ps1 -InputFile "notepad.exe" -OutputFormat Hex

# Convert to both formats
.\ExeToBin.ps1 -InputFile "notepad.exe" -OutputFormat Both

# Save output to file
.\ExeToBin.ps1 -InputFile "notepad.exe" -OutputFormat Base64 -OutputFile "output.txt"
```

### Python GUI

1. Click **Browse** to select an .exe file
2. Choose output format (Base64 / Hex / Raw Bytes)
3. Copy to clipboard or save as file

## Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **Base64** | ASCII-safe encoding | Embedding in scripts, web, documents |
| **Hex** | Hexadecimal bytes | Debugging, memory analysis |
| **Raw** | Spaced hex bytes | Compact representation |

## Requirements

### PowerShell Version
- Windows PowerShell 5.0+ or PowerShell Core
- No external dependencies

### Python Version
- Python 3.6+
- tkinter (built-in)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

---

*Convert executables to portable byte formats*
