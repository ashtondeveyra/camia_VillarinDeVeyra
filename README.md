Project Title:
# Class Monitor Attendance Tracker

- Project Description: 

The Class Monitor Attendance tracker is a school project in PSHS - EVCL Campus dedicated to Track, Display, and monitor attendance in Section Homerooms. We saw that our school makes the use of a school monitor to be in track of attendance, so we made use of the certain problem.
 
The Class Monitor Attendance Tracker is comprised of four parts: the QR Generator, the QR Scanner, the Display Monitor, and the Admin Panel. The QR Generator makes the QR code for students who don't have or have no access to a QR code. The QR Scanner scans the QR code and captures a snapshot for visual verification before pasting the information into the monitor. The Display Monitor is in charge of monitoring and displaying the name given from the QR code, as well as the time and time status. Lastly, the Admin Panel allows the Person-in-Authority to securely log in using a password to modify or delete attendance records and manage system settings.
__________________________________________________________________________________________________________________________________________________________________
- Features:
1. In the user interface, there are 2 buttons for the user to pick:

      A. The Generate QR Code Button (For those with no QR Code)

       - When pressed it will ask for your Full name
       - Last Name, First Name, M.I. is the format used for your name.
       - Once information is filled, it will generate a qr code for you

     B. The Scan QR Code Button

         - It will ask to open the Device's camera
         - Once opened, it will scan the QR code
         - Once scanned, the camera captures a snapshot for visual proof, and the user's  attendance is recorded.


 

2. The program displays people's names in numerical order

3. Program displays your time status based on what time you registered:
	
        A. Early - Before 7:30
      	B. On Time - Exactly 7 : 30
      	C. Late, No admission slip - 7:30 - 7:39
      	D. Late, Admission slip for tardiness - 7:40 onwards.

4. With the use of python, time tracker is applied for easier way to make the program
5. Names, as well as the time status, and time is displayed on the main page for easier monitoring and visibility
6. Upon exiting the program, the program's attendance display is converted into an excel sheet and text file that are saved and organized in the same file location as the .py file
7. The camera snapshots are also saved in the same file location as the .py file, and are labeled based on the data of the scanned QR code (the student's name)
8. You can only Scan your QR Code once, if you scan it again, the program will say:
 "Attendance Already Recorded for {name}"

9. In the user interface, there are also buttons for the admin/person-in-charge, which are as follows:

	 A. Admin Login - the person-in-charge must first enter their password to log in and be recognized as the admin

   		 - Upon logging in, the person-in-charge can do the following:
    			a. Update an attendace record - allows them to modify aspects of an attendance record like the name, time of arrival, and time status
   				b. Delete an attendance record - allows them to delete a specific attendance record
   				c. Log out
		 

	 B. Change Password - allows the person-in-charge to change their password by entering their original password first
__________________________________________________________________________________________________________________________________________________________________
- Exceptions:

	The scanner only scans the QR codes made in the program. Other QR Codes wont be accepted by the QR scanner.     
	The program resets every day at 12:00 AM, in order to prevent any bugs on the time status
__________________________________________________________________________________________________________________________________________________________________

- How to Run the Program:
1. Have Python installed on your device
2. Download the file Attendance_Tracker.py
3. Open your computer's terminal (or Command Prompt)
4. Navigate to the folder where you saved Attendance_Tracker.py using the cd command (e.g., cd MainDirectory/Folder_Where_File_IsSaved).
5. Type 'python Attendance_Tracker.py'
6. Follow the on-screen instruction.

- DISCLAIMER (only for the person-in-authority or admin):

		-To access the Admin Panel, please enter the default password: admin123
  		-This password can be changed using the change password feature
__________________________________________________________________________________________________________________________________________________________________






Example Output:
	
    (Once Everyone has secured attendance, please save and close this program)
	  |GENERATE QR|		|SCAN QR|
    *Presses Scan QR*
    "Please Open The Device's Camera, Press Q to Cancel"
    *Opens Camera*
    *Scans QR Code
    On the Display Monitor: 1. De Veyra, Ashton Zac (Early at 7:05)
__________________________________________________________________________________________________________________________________________________________________

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
