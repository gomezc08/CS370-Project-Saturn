<p align="right">Neel Troeger</p>
<p align="right">CS 370</p>
<p align="right">3/3/2024</p>

<p align="center">Exam 2 Take-Home</p>

**Use Case Name** | Change Audio File Display Order |
|---|---|
Summary | A user reorders the audio files in their audio archive project through the GUI, allowing for a more personalized and efficient organization of their audio files. |
Rationale | Users may want to change the order of audio files to suit their archival preferences, such as ordering by importance, frequency of use, or thematic relevance. This allows for a more efficient retrieval and usage of the audio files. |
Users | Any user of the audio archive project who has the need to customize the order of their audio files for better accessibility and organization. |
Preconditions | User has audio files in their audio archive and has launched the audio archive tool. |
Course of Events | 1. User launches the audio archive tool from their device. <br> 2. The program presents a list of the audio files in the archive in their current order. <br> 3. User selects and drags the desired audio file, then drops it at the preferred position in the list. The program provides immediate visual feedback through a smooth animation or a noticeable change in the appearance of the selected audio file, confirming the ongoing drag-and-drop action. <br> 4. After successfully updating the order, the GUI reflects the change in order instantly, and the backend is updated accordingly. |
Exceptions | If the user does not have any audio files in their audio archive, the program will not only prompt the user to add audio files but also provide a guide on how to add audio files. If the user attempts to move a file to an invalid position (e.g., outside the list boundaries), the program will display a detailed error message explaining the invalid action and guide the user on how to rectify the issue. In case of any system errors or unexpected issues during the reordering process, the program will handle the situation gracefully, maintaining the current order and informing the user about the issue. |
Alternative Paths | 1. User can access the built-in sorting function through a clearly labeled button or menu option in the GUI. <br> 2. The sorting function allows reordering of audio files based on file name, duration, bitrate, file size, or custom metadata. The user selects the desired sorting criteria, and the program intelligently adjusts the display, providing a clear visual representation of the new order. <br> 3. The program may intelligently suggest potential sorting criteria based on the user's historical preferences or usage patterns, enhancing user assistance and guidance. |
Postconditions | The order of audio files in the user's audio archive is updated both in the GUI and saved in the backend. The user can now access and use the audio files in the new order. |