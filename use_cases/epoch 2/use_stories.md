User Stories for Epoch 2

1. I, as a user, would like to take my 13 coffee slurp sounds and randomly insert short clips of an audio into all of them at random times, 2~3 times per coffee slurp.
2. I, as a user, have added my 20 sound files into the sound directory and would like to see them in alphabetical order.
3. I, as a user, would like to be able to sort my sounds by date creation and date edited.
4. I, as a user, would like to hear what my sounds sound like when played backwards.
5. I, as a user, would like to flag my favorite sounds and would like to see them at the top of my directory because they’re my favorite.
6. I, as a user, would like to randomize the volume of my sound as it plays. For example, I want it to be able to get louder/quieter throughout its playing
7. I, as a user, would like to blend two audio files so one audio file plays into another audio file, with simultaneous overlap.
8. I, as a user, would like to bass boost an audio file.
9. I, as a user would like to normalize the volume of an audio file to a target amount of decibels.

Name: UC-#RandomInsert

Summary: For some audio files and a given audio clip, insert the audio clip into random points in the audio files, replacing the original sound, 2~3 times.

Rationale: It would be cool and fun. Remixing!

Users: all users

Preconditions: The audio clip being inserted is significantly shorter in length than the audio files it is inserting into. We’re given an audio clip and 1+ audio files.

Basic course of events:
1. User provides a list of audio files to be edited and an audio clip to insert.
2. For each audio file to be edited, the software determines whether the audio clip will be inserted 2 or 3 times (determined randomly; coin flip).
3. For each audio file to be edited, the software randomly determines locations in the audio file equal to the length of the audio clip to be replaced.
4. The software replaces the audio files with the audio clip.

Alternate Paths:
1. The user is unhappy with their remixed audio and would like their original sound files back.
2. The user is unhappy with their remixed audio and would like to try remixing them again.

Postconditions: All of the given audio files have had parts of their sound replaced with the given audio clip

Name: UC-#AlphabeticalOrder

Summary: the user would like to see their files sorted in alphabetical order

Rationale: basic organizational feature

Users: all users

Preconditions: there is more than one audio file in the directory and the directory is not sorted in alphabetical order (and users can add sounds)

Basic Course of Events:
1. User adds/looks at the current directory of sounds
2. User makes a request for the sounds to be sorted in alphabetical order
3. Software sorts the sounds in alphabetical order and presents them back to the user

Alternate Paths:
1. The user no longer wants to see their sounds sorted in alphabetical order and would like to unsort them (?)
Postconditions - the directory now presents the sounds in alphabetical order


Name: UC-#BassBoost

Summary: The audio of a file has its bass boosted.

Rationale: This would be funny.

Users: All users

Preconditions: A audio file is loaded.

Basic course of events:
1. Audio file loaded
2. User's flag would specify to boost the bass and the value by which to do it.
3. The audio track is played, with the new bass amount.

Alternate paths:
1. The user can exit playing, and since it is not permanent, it will revert to the precondition state.
Postconditions: This will not be permanent, to avoid changing the files themselves.


Name: UC-#NormalizeAudio

Summary: The audio levels will be normalized, meaning the volume will effect them all equally.

Rationale: This is a necessary quality of life addition.

Users: All users

Preconditions: A audio file is loaded.

Basic course of events:
1. Audio file loaded
2. The audio level would be set to a value pre-set into the python file or provided by the user.
3. The audio track is played
Alternate paths: 1. The user can exit playing, and since it is not permanent, it will revert to the precondition state.
Postconditions: This will not be permanent, to avoid changing the files themselves.

Name: Reverse

Summary: Plays a selected audio file in reverse when applied

Rationale: A listener would want to listen to an audio file in reverse for a new listening experience.

Users: All Users

Preconditions: A single, playable audio file has been loaded

Basic Course of Events:

1. The user selects their desired file
2. The user then selects the 'reverse' option before playing the file
3. When the user plays the file, the file is played in reverse

Alternative Paths: NA

Postconditions: File is no longer selected, and reverse is no longer applied to any files until selected again
