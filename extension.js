// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const path = require('path');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "foxyjumpscare" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('foxyjumpscare.helloWorld', function () {
		// The code you place here will be executed every time your command is executed
		const panel = vscode.window.createWebviewPanel(
            'videoPlayer', // Identifies the type of the webview. Used internally
            'Video Player', // Title of the panel displayed to the user
            vscode.ViewColumn.One, // Editor column to show the new webview panel in.
            {
                // 2. Enable scripts in the webview
                enableScripts: true,
                
                // 3. Important: Restrict the webview to only loading content from our extension's `media` directory.
                localResourceRoots: [vscode.Uri.file(path.join(context.extensionPath, 'media'))]
            }
        );
		const onDiskPath = vscode.Uri.file(
            path.join(context.extensionPath, 'media', 'fnaf-2-foxy-jumpscare-video.mp4')
        );
		const videoSrc = panel.webview.asWebviewUri(onDiskPath);

        // 6. Set the HTML content
        panel.webview.html = getWebviewContent(videoSrc);

		panel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'toggleFullscreen':

                        vscode.commands.executeCommand('workbench.action.toggleZenMode');
                        break;
                }
            },
            undefined,
            context.subscriptions
        );
	});

	context.subscriptions.push(disposable);
}

function getWebviewContent(videoSrc) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Player</title>
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; media-src ${videoSrc.scheme}: https:; script-src 'unsafe-inline';">
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: var(--vscode-editor-background); }
        video { max-width: 100%; max-height: 100%; outline: none; }
    </style>
</head>
<body>
    <video id="myVideo" controls width="1080">
        <source src="${videoSrc}" type="video/mp4">
    </video>

    <script>
        const video = document.getElementById('myVideo');
        
        // Try to play with sound first
        video.play().catch(error => {
            // If that fails (due to browser policy), mute and try again
            console.log("Autoplay with sound failed, muting and playing.");
            video.muted = true;
            video.play();
        });
    </script>
</body>
</html>`;
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
