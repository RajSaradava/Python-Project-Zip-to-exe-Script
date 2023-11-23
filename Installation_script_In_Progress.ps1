# PowerShell script for DNA Cloud installation

# Define the form
Add-Type -AssemblyName System.Windows.Forms
$form = New-Object System.Windows.Forms.Form
$form.Text = "DNA Cloud Installation"
$form.Size = New-Object System.Drawing.Size(600, 400)

# Create labels and textboxes
$labelVersion = New-Object System.Windows.Forms.Label
$labelVersion.Text = "Enter version name:"
$labelVersion.Location = New-Object System.Drawing.Point(20, 20)
$labelVersion.AutoSize = $true
$form.Controls.Add($labelVersion)

$textboxVersion = New-Object System.Windows.Forms.TextBox
$textboxVersion.Location = New-Object System.Drawing.Point(200, 20)
$textboxVersion.Size = New-Object System.Drawing.Size(250, 20)
$form.Controls.Add($textboxVersion)

$labelLicense = New-Object System.Windows.Forms.Label
$labelLicense.Text = "Select license text file:"
$labelLicense.Location = New-Object System.Drawing.Point(20, 60)
$labelLicense.AutoSize = $true
$form.Controls.Add($labelLicense)

$textboxLicense = New-Object System.Windows.Forms.TextBox
$textboxLicense.Multiline = $true
$textboxLicense.ScrollBars = 'Vertical'
$textboxLicense.Location = New-Object System.Drawing.Point(200, 60)
$textboxLicense.Size = New-Object System.Drawing.Size(250, 80)
$form.Controls.Add($textboxLicense)

$buttonBrowseLicense = New-Object System.Windows.Forms.Button
$buttonBrowseLicense.Text = "Browse"
$buttonBrowseLicense.Location = New-Object System.Drawing.Point(460, 60)
$buttonBrowseLicense.Add_Click({
    $licenseFileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $licenseFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
    
    if ($licenseFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $textboxLicense.Text = Get-Content $licenseFileDialog.FileName -Raw
    }
})
$form.Controls.Add($buttonBrowseLicense)

$labelExeFile = New-Object System.Windows.Forms.Label
$labelExeFile.Text = "Select DNA Cloud executable file:"
$labelExeFile.Location = New-Object System.Drawing.Point(20, 150)
$labelExeFile.AutoSize = $true
$form.Controls.Add($labelExeFile)

$textboxExeFile = New-Object System.Windows.Forms.TextBox
$textboxExeFile.Location = New-Object System.Drawing.Point(200, 150)
$textboxExeFile.Size = New-Object System.Drawing.Size(250, 20)
$form.Controls.Add($textboxExeFile)

$buttonBrowseExeFile = New-Object System.Windows.Forms.Button
$buttonBrowseExeFile.Text = "Browse"
$buttonBrowseExeFile.Location = New-Object System.Drawing.Point(460, 150)
$buttonBrowseExeFile.Add_Click({
    $exeFileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $exeFileDialog.Filter = "Executable files (*.exe)|*.exe|All files (*.*)|*.*"
    
    if ($exeFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $textboxExeFile.Text = $exeFileDialog.FileName
    }
})
$form.Controls.Add($buttonBrowseExeFile)

$checkboxCreateDesktopShortcut = New-Object System.Windows.Forms.CheckBox
$checkboxCreateDesktopShortcut.Text = "Create Desktop Shortcut"
$checkboxCreateDesktopShortcut.Location = New-Object System.Drawing.Point(20, 200)
$form.Controls.Add($checkboxCreateDesktopShortcut)

# Create buttons for Next and Back
$buttonNext = New-Object System.Windows.Forms.Button
$buttonNext.Text = "Next"
$buttonNext.Location = New-Object System.Drawing.Point(20, 240)
$form.Controls.Add($buttonNext)

$buttonBack = New-Object System.Windows.Forms.Button
$buttonBack.Text = "Back"
$buttonBack.Location = New-Object System.Drawing.Point(100, 240)
$buttonBack.Enabled = $false  # Back button is disabled initially
$form.Controls.Add($buttonBack)

# Event handler for Next button
$buttonNext.Add_Click({
    if ($buttonNext.Text -eq "Next") {
        # Move to the next step
        $buttonBack.Enabled = $true
        $buttonNext.Text = "Install"
        # Your logic for handling version and license information goes here
    } else {
        # Perform the installation
        $versionName = $textboxVersion.Text
        $licenseText = $textboxLicense.Text
        $exeFilePath = $textboxExeFile.Text
        $createDesktopShortcut = $checkboxCreateDesktopShortcut.Checked

        # Validate that the DNA Cloud executable file exists
        if (-not (Test-Path $exeFilePath -PathType Leaf)) {
            [System.Windows.Forms.MessageBox]::Show("Please select a valid DNA Cloud executable file.", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
            return
        }

        # Set paths
        $destinationPath = "C:\Program Files\DNA Cloud"

        # Optionally, create destination directory if it doesn't exist
        if (-not (Test-Path $destinationPath)) {
            New-Item -ItemType Directory -Path $destinationPath | Out-Null
        }

        # Copy the DNA Cloud executable file
        Copy-Item -Path $exeFilePath -Destination $destinationPath -Force

        # Optionally, create desktop shortcut
        if ($createDesktopShortcut) {
            $desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"), "DNA Cloud.lnk")
            $shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($desktopPath)
            $shortcut.TargetPath = [System.IO.Path]::Combine($destinationPath, (Get-Item $exeFilePath).Name)
            $shortcut.Save()
        }

        # Optionally, perform any additional actions or cleanup here

        # Close the form
        $form.Close()
    }
})

# Event handler for Back button
$buttonBack.Add_Click({
    # Move back to the previous step
    $buttonBack.Enabled = $false
    $buttonNext.Text = "Next"
    # Your logic for handling going back to the previous step goes here
})

# Show the form
$form.ShowDialog()
