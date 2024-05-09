Use case name: Change pitch

Summary: Alter pitch of a specified audio file 

Rationale: Pitch manipulation plays a pivotal role in audio production and can be used to enhance visuals. The pitch changing feature allows users to adjust the pitch of their audio as follows: increase or decrease pitch and can specify amount of change in Pitch. The user using this feature will need to specify the audio file, choose value for change in pitch. 

Users: All users

Preconditions: User has chosen and uploaded audio file to be edited.

Course of events:
User indicates (through CLI) that the software will perform a change in Pitch of specified audio file. 
Software response by requesting for an increase or decrease in pitch.
 software then requests for a number change in pitch.
Software plays back audio
 software provides user the option to save new audio file or not 

Expectations: invalid pitch change request: no we still don't know if we will have user select low, medium, high or dictate a percentage. but if we use percentage, we would want software to handle nonsensical pitch change

Alternative paths: if at the end of the audio edit, the user should have a option to continue editing

Post conditions: a new version of audio file with pitch adjustments 