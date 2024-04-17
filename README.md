# Steganography Detection Tool

This tool is designed for detecting steganography in files, particularly images, using various methods commonly employed in cybersecurity and digital forensics.

## Introduction

Steganography is the practice of concealing a message, file, image, or video within another message, file, image, or video. This tool provides a collection of utilities to analyze files for potential hidden content, including strings and metadata extraction, steghide detection, binwalk analysis, and more.

## Requirements

- This tool is specifically designed for Linux systems.
- Python 3.x is required.
- Certain functionalities rely on external tools like `steghide`, `binwalk`, `exiftool`, etc. Ensure these tools are installed on your system.

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/LightYagamiRT/stego_detection_tool.git
   ```

2. Navigate into the project directory:

   ```bash
   cd stego-detection-tool
   ```

3. Run the main Python script:

   ```bash
   python stego_detection_tool.py
   ```

4. Follow the prompts to select the analysis options and provide the file path you want to analyze.

## Features

- **Strings and Grep:** Search for potential flags or hidden messages within files.
- **Exiftool:** Extract metadata from files, particularly images.
- **Steghide:** Detect hidden data within images using steghide.
- **Zsteg:** Analyze PNG and BMP images for hidden data using zsteg.
- **Binwalk:** Scan files for embedded files and executable code.
- **Foremost:** Recover embedded images from files.
- **Pngcheck:** Validate the integrity of PNG image files.
- **Stegseek:** Perform brute-force attacks to uncover hidden data within images.

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
