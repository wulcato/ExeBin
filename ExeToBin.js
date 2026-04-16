#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const InputFile = args.find(arg => !arg.startsWith('-')) || process.argv.find(arg => arg.includes('.exe'));
const OutputFormat = args.includes('-Hex') ? 'Hex' : args.includes('-Both') ? 'Both' : 'Base64';
const OutputFile = args.includes('-OutputFile') ? args[args.indexOf('-OutputFile') + 1] : null;

const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    cyan: '\x1b[36m',
    gray: '\x1b[90m',
    reset: '\x1b[0m'
};

function colorLog(message, color) {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

if (!InputFile) {
    colorLog('[ERROR] Usage: node ExeToBin.js <inputfile.exe> [-Base64|-Hex|-Both] [-OutputFile <path>]', 'red');
    process.exit(1);
}

if (!fs.existsSync(InputFile)) {
    colorLog(`[ERROR] File not found: ${InputFile}`, 'red');
    process.exit(1);
}

const fileInfo = fs.statSync(InputFile);
const fileSizeKB = (fileInfo.size / 1024).toFixed(2);

colorLog(`[INFO] Processing: ${path.basename(InputFile)}`, 'cyan');
colorLog(`[INFO] File size: ${fileSizeKB} KB`, 'cyan');

const fileBytes = fs.readFileSync(InputFile);

switch (OutputFormat) {
    case 'Base64': {
        const encoded = fileBytes.toString('base64');
        colorLog('[SUCCESS] Base64 conversion complete', 'green');

        if (OutputFile) {
            fs.writeFileSync(OutputFile, encoded, 'utf8');
            colorLog(`[SAVED] Output: ${OutputFile}`, 'green');
        } else {
            colorLog('[OUTPUT] Base64 String:', 'cyan');
            colorLog('-'.repeat(60), 'gray');
            console.log(encoded);
            colorLog('-'.repeat(60), 'gray');
            colorLog(`[INFO] Total characters: ${encoded.length}`, 'cyan');
        }
        break;
    }

    case 'Hex': {
        const hexString = fileBytes.toString('hex').match(/.{1,2}/g).join(' ');
        colorLog('[SUCCESS] Hex conversion complete', 'green');

        if (OutputFile) {
            fs.writeFileSync(OutputFile, hexString, 'utf8');
            colorLog(`[SAVED] Output: ${OutputFile}`, 'green');
        } else {
            colorLog('[OUTPUT] Hex String:', 'cyan');
            colorLog('-'.repeat(60), 'gray');
            console.log(hexString);
            colorLog('-'.repeat(60), 'gray');
            colorLog(`[INFO] Total characters: ${hexString.length}`, 'cyan');
        }
        break;
    }

    case 'Both': {
        const base64 = fileBytes.toString('base64');
        const hexString = fileBytes.toString('hex').match(/.{1,2}/g).join(' ');
        colorLog('[SUCCESS] Both conversions complete', 'green');

        colorLog('[OUTPUT] Base64 String:', 'cyan');
        colorLog('-'.repeat(60), 'gray');
        console.log(base64);
        colorLog('-'.repeat(60), 'gray');

        console.log();
        colorLog('[OUTPUT] Hex String:', 'cyan');
        colorLog('-'.repeat(60), 'gray');
        console.log(hexString);
        colorLog('-'.repeat(60), 'gray');

        if (OutputFile) {
            const combined = `=== BASE64 OUTPUT ===\n${base64}\n\n=== HEX OUTPUT ===\n${hexString}`;
            fs.writeFileSync(OutputFile, combined, 'utf8');
            colorLog(`[SAVED] Output: ${OutputFile}`, 'green');
        }
        break;
    }
}

colorLog('\n[COMPLETE] Conversion finished successfully!', 'green');
