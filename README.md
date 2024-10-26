
FROM MEMORY MAP:
https://www.smwcentral.net/?p=memorymap&game=smw
$7E0019 	1 byte 	Player 	Current player powerup status. 0-3, small, big, cape, fire
$7E0076 	1 byte 	Player 	Player direction. #$00 = Left; #$01 = Right.
$7E007B 	1 byte 	Player 	Player X speed (8-bit, signed), in 1/16s of a pixel per frame. Positive speeds (01-7F) are rightwards while negative speeds (80-FF) are leftwards.
$7E007D 	1 byte 	Player 	Player Y speed (8-bit, signed), in 1/16s of a pixel per frame. Positive speeds (01-7F) are downwards while negative speeds (80-FF) are upwards.
$7E00D1 	2 bytes Player 	Player X position (16-bit) within the level, current frame (as opposed to $7E:0094).
$7E00D3 	2 bytes Player 	Player Y position (16-bit) within the level, current frame (as opposed to $7E:0096).
$7E0DBE 	1 byte 	Player 	Current player lives, minus one (#$04 here means that the player has 5 lives).
$7E0DBF 	1 byte 	Player 	Current player coin count. -> "snes9x-x64.exe" + A330D3

$7E0071 	1 byte 	Player 	Player animation trigger states. When nonzero, the player character is performing an action and cannot be controlled by the player. Often used for cutscenes.
00	None: the player is able to move freely.
01	Flashing as if the player is hurt by an enemy.
02	Get Mushroom animation.
03	Get Feather animation. (Note: to make it work, write to $1496 also.)
04	Get Fire Flower animation. (Note: to make it work, write to $149B also.)
05	Enter a horizontal Warp Pipe.
06	Enter a vertical Warp Pipe.
07	Shoot from a slanted pipe.
08	Shoot up into the sky. (Yoshi Wings)
09	End level without activating overworld events. (Dying)
0A	Castle entrance moves.
0B	Freeze player (used during the bowser defeated cutscene, and also disables HDMA).
0C	Castle destruction moves.
0D	Enter a door.

$7E0079 	1 byte 	Empty 	Empty. Cleared on reset, titlescreen load, overworld load and level load. <- Could write a 1 here, then check for when it is reset
$7E0DD5 	1 byte 	Misc. 	Used to indicate how a level has been exited, and hence what events to activate on the overworld.
00	No event; do nothing
01	Normal exit
02	Secret exit 1
03	Secret exit 2
04	Secret exit 3
05	Corresponds to the first "do not use" overworld action for secondary exits
06	Corresponds to the second "do not use" overworld action for secondary exits
80	No event; level exited with start+select or dying (or "switch players" secondary exit action)
E0	No event, but show save prompt anyway (used if the level was beaten a second time and its tile corresponds to one of the tiles at $04E5E6)


$7E0019 	1 byte 	read_memory_bytes(0xA3232D, 1)
$7E0071 	1 byte  read_memory_bytes(0xA32385, 1)
$7E0076 	1 byte 	read_memory_bytes(0xA3238A, 1)
$7E0079     1 byte  write_memory_bytes(0xA3238D, 1)
$7E007B 	1 byte 	read_memory_bytes(0xA3238F, 1)
$7E007D 	1 byte 	read_memory_bytes(0xA32391, 1)
$7E00D1 	2 bytes read_memory_bytes(0xA323E5, 2)
$7E00D3 	2 bytes read_memory_bytes(0xA323E7, 2)
$7E0DBE 	1 byte 	read_memory_bytes(0xA330D2, 1)
$7E0DBF 	1 byte 	read_memory_bytes(0xA330D3, 1)
$7E0DD5 	1 byte  read_memory_bytes(0xA330E9, 1)
$7E0F31 	3 bytes write_memory_bytes(0xA33245, 1)

$7E0F34 	6 bytes 	Counter 	24-bit scores for each player.
$0F34 = Mario's score.
$0F37 = Luigi's score.

Note: This value is in hexadecimal and not decimal, so it needs to be converted before it can be displayed in-game. Additionally, this value is actually the score seen in the status bar divided by 10, as the "ones digit" SMW displays is actually just a static 0 tile.

$7E0F31 	3 bytes 	Counter 	Timer.
$7E:0F31 = Hundreds.
$7E:0F32 = Tens.
$7E:0F33 = Ones.