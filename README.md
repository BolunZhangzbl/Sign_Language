# IC_AML_Lab_Chappie

## DATA STRUCTURE
- Data structure: [time_segment, EMG1, EMG2, EMG3, EMG4, ANGX, ANGY, ANGZ, LINX, LINY, LINZ] <br />
- Start flag: [-200] * 11 <br />
- End flag: [-100] * 11 <br />
- If start with a row of [-1] * 11, ignore it! <br />

## SOFTWARE
### Arduino Installation
1. Install Arduino from https://www.arduino.cc/en/software.
2. After installation, open Arduino. Click **Sketch** → **Include Library** → **Manage Libraries...**, search **Adafruit_BNO055** library and choose **install all**.
3. Back to Arduino, click **Tools** → **Boards:...** → **Boards Manager...**, search **Arduino SAM Boards (32-bits ARM Cortex-M3)** and install.

### Upload Code to Arduino Board
1. Select **Tools** → **Boards:...** → **Boards Manager...** → **Arduino ARM (32-bits) Boards** → **Arduino Due (Native USB Port)**.
2. In **Tools** → **Port**, select the one that's connected to Arduino board.
3. Upload.

### Python Installation
1. `pip install pyserial`
2. `pip install matplotlib`
3. `pip install numpy`

## TO RECORD DATA
Upload arduino code into arduino board, then run python code to receive data transmitted by arduino board.
