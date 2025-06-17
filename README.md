# TypeRiser

## Overview
TypeRiser is a versatile desktop application designed to automate text input into any application with precise, customizable typing speeds. Built with Python, Tkinter, and PyAutoGUI, it offers a modern, intuitive interface for users to type text at controlled rates, ranging from 30 to 2000 characters per minute (CPM). Whether you're automating workflows, creating demos, or enhancing accessibility, TypeRiser provides a reliable and flexible solution.

## Features
- **Customizable Typing Speed**: Set your typing speed from 1 to 2000 CPM to match your needs.
- **Flexible Target Selection**:
  - Type at the current cursor position.
  - Click to select a specific target area (with a 5-second window).
  - Type at the center of the screen.
- **Debug Mode**: Enable console output for detailed debugging and monitoring.
- **Failsafe Mechanism**: Move the mouse to the top-left corner to instantly stop typing.
- **Test Mode**: Verify functionality by typing "Hello" with a single click.
- **Sample Text**: Load pre-written text for quick testing.
- **Modern UI**: Sleek, dark-themed interface with clear status updates and intuitive controls.
- **Customizable Delay**: Set a countdown delay (0-60 seconds) before typing begins.

## Requirements
- **Python 3.x** (Tkinter comes built-in with Python on Windows)
- **PyAutoGUI**: Install via `pip install pyautogui`
- A compatible operating system (Windows, macOS, or Linux)

## Installation
1. Clone or download the repository:
   ```bash
   git clone https://github.com/your-username/TypeRiser.git
   ```
2. Navigate to the project directory:
   ```bash
   cd TypeRiser
   ```
3. Install the required dependency:
   ```bash
   pip install pyautogui
   ```
4. Run the application:
   ```bash
   python typeriser.py
   ```

## Usage
1. **Launch the Application**: Run the script to open the TypeRiser window.
2. **Test PyAutoGUI**: Click "Test PyAutoGUI" to ensure typing works (types "Hello" after a 3-second countdown).
3. **Enter Text**: Input your desired text in the text area or click "Load Sample Text" for a quick start.
4. **Set Parameters**:
   - Choose a typing speed (CPM) or select a preset (Very Slow, Slow, Medium, Normal, Fast).
   - Set a delay (seconds) for the countdown before typing begins.
   - Select a target method (current position, click to choose, or screen center).
5. **Start Typing**: Click "Start Typing" to begin. Use "Stop Typing" to halt the process.
6. **Failsafe**: Move your mouse to the top-left corner of the screen to immediately stop typing.

## Debugging
- Enable "Debug Mode" in the UI to view detailed console output, including:
  - PyAutoGUI version and screen information.
  - Typing progress and character-by-character logs.
  - Error messages and status updates.

## Notes
- Ensure the target application is ready to receive input before starting.
- Minimize the TypeRiser window if it overlaps with your target typing area.
- Avoid moving the mouse during typing to prevent unintended cursor shifts.
- The application runs in a separate thread to keep the UI responsive.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [PyAutoGUI](https://pyautogui.readthedocs.io/) for cross-platform automation.
- Powered by [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI.
- Inspired by the need for precise, automated text input across applications.

---
Happy Typing with TypeRiser! 🚀
