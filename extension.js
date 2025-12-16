const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

// CONFIGURATION
const CHANCE_DENOMINATOR = 10000; // 1 in 10000 chance
const CHECK_INTERVAL_MS = 1000; // Check every 1 second

let intervalId;

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Five Nights...');

    const triggerJumpscare = () => {
        const scriptPath = path.join(context.extensionPath, '__init__.py');
        
        const pyProcess = spawn('python', [scriptPath], {
            cwd: path.join(context.extensionPath, 'media') 
        });

        pyProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data}`);
        });

        pyProcess.on('error', (err) => {
             console.error(`Spawn Error: ${err}`);
             vscode.window.showErrorMessage("Failed to launch Jumpscare. Is Python installed?");
        });
    };

    // THE TIMER
    intervalId = setInterval(() => {
        const roll = Math.floor(Math.random() * CHANCE_DENOMINATOR) + 1;
        if (roll === 1) {
            triggerJumpscare();
        }
    }, CHECK_INTERVAL_MS);
}

function deactivate() {
    if (intervalId) {
        clearInterval(intervalId);
    }
}

module.exports = {
    activate,
    deactivate
}