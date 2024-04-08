Use Case Name
Random Sound Insert
Summary
This feature would allow the user to select a short sound clip (1~3 seconds) and randomly insert it 2~3 times into another audio clip of their selection
Rationale
This feature does not really have a practical application. Its purpose is to provide an absurd form of enjoyment to the user.
Users
All Users (that dare employ this feature)
Preconditions
The user specifies two audio clips existing within the existing audio library. The first audio clip is a short audio file (around 1~3 seconds) and the second is a longer audio file (long enough for the user’s first audio clip to be inserted 3 times). Both audio files should be in the same audio format.
Course of Events
1. The user uses the command line interface to call the Sound Insert Command, specifying an audio file to be inserted and an audio file to be inserted into (-S)
2. The system randomly decides to insert the audio two or three times
3. The system randomly picks two or three timestamps within the second audio file
4. At the selected timestamps, the system replaces the original audio with the first audio clip, for the duration of the audio file (unless original audio has finished playing)
5. The system plays the new edited audio file
6. The system saves the newly constructed audio as an audio file of the same format
Exceptions
1. If the first audio file provided exceeds 3 seconds, an error is raised indicating that the first audio file is too long
2. If the second audio file provided is less than 10 seconds long, an error is raised indicating that the second audio file is too short
3. If the first and second audio files are in different audio formats, an error is raised indicating file incompatibility
Alternate Paths
1. In step 6, the user can choose to replay the newly constructed audio so they can listen to it again
2. In step 6, the user can choose to immediately remix the audio again if they are unhappy with the result, by going back to step 1
3. In step 6, the user can forego this step completely and be satisfied with the listening to their randomized audio
Postconditions
The program properly plays a new audio sound with the specified changes above
If asked by the user, the program creates a new audio file in the sound library with the newly remixed audio sound. The new audio file format should be the same as the remixed audios

