const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

const CHANCE_DENOMINATOR = 10000; 
const CHECK_INTERVAL_MS = 1000;

let intervalId;

function activate(context) {
    console.log('Five Nights...');

    const triggerJumpscare = () => {
        const scriptPath = path.join(context.extensionPath, '__init__.py');
        const videoPath = path.join(context.extensionPath, 'media', 'fnaf-2-foxy-jumpscare-video.mp4');
        
        // Spawn Python
        const pyProcess = spawn('python', [scriptPath, videoPath]);

        pyProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data}`);
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
    if (intervalId) clearInterval(intervalId);
}

module.exports = { activate, deactivate }