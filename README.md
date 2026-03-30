Project Title:
# Class Monitor Attendance Tracker

- Project Description: 

The Class Monitor Attendance tracker is a school project in PSHS - EVCL Campus dedicated to Track, Display, and monitor attendance in Section Homerooms. We saw that our school makes the use of a school monitor to be in track of attendance, so we made use of the certain problem.
 
The Class Monitor Attendance Tracker is comprised of 3 parts, the QR Generator, QR Scanner, and the Display screen. The QR Generator makes the QR code for students who don't have or have no access to the QR code. The QR scanner, on the other hand, scans the QR code and pastes information into the Display monitor. Lastly, the Display Monitor is in charge of monitoring and displaying The name given from the QR code. The Display monitor also gets and displays the time and time status.

- Features:
1. In the user interface, there are 2 buttons for you to pick:

      A. The Generate QR Code Button (For those with no QR Code)

       - When pressed it will ask for your Full name
       - Last Name, First Name, M.I. is the format used for your name.
       - Once information is filled, it will generate a qr code for you

     B. The Scan QR Code Button

         - It will ask to open the Device's camera
         - Once opened, it will scan the QR code
         - Once scanned, Your attendance will be recorded
 

2. The program displays people's names in numerical order
3. Program displays your time status based on what time you registered:
	
        A. Early - Before 7:30
      	B. On Time - Exactly 7 : 30
      	C. Late, No admission slip - 7:30 - 7:39
      	D. Late, Admission slip for tardiness - 7:40 onwards.

4. With the use of python, time tracker is applied for easier way to make the program
5. Names, as well as the time status, and time is displayed on the main page for easier monitoring and visibility
6. The program's attendance display can be converted into an excel sheet and text file once saved for easier sharing of the registration.
7. You can only Scan your QR Code once, if you scan it again, the program will say:
 "Attendance Already Recorded for {name}"

The scanner only scans the QR codes made in the program. Other QR Codes wont be accepted by the QR scanner.
The program resets every day at 12:00 AM, in order to prevent any bugs on the time status

- How to Run the Program:
1. Have Python installed on your device
2. Download the file Attendance_Tracker
3. Open the file downloaded.
4. Make sure the student follows the on-screen instruction.






Example Output:
	
    (Once Everyone has secured attendance, please save and close this program)
	  |GENERATE QR|		|SCAN QR|
    *Presses Scan QR*
    "Please Open The Device's Camera, Press Q to Cancel"
    *Opens Camera*
    *Scans QR Code
    On the Display Monitor: 1. De Veyra, Ashton Zac (Early at 7:05)


Contributors: 
Villarin, Sean Lester C. -
 helped in making the project title, its objectives,planned features, and helping in the design of the flowchart.
 Revised the project.
Updated the README and the Progress reports
Gave ideas on what to change and the structure of the code

 De Veyra, Ashton Zac G. 
 helped in making the project description, features, and overall outline logic plan (flowchart) of the program
Made the program and added gui
Made progress reports.
Uploads all documentation into the GitHub account
