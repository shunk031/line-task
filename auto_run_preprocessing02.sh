#!/bin/bash

user_list=(wasara
	   myozurin
	   C1the
	   rokiegle
	   yuuraku
	   ui_nyan
	   Lasei_
	   ralachi5019
	   d_v_osorezan
	   groovy223
	   To_aru_ritsu
	   funiimouto
	   2nd_error403
	   error403
	   suzukosuke
	   taka_nashi
	   877uszm
	   kaiten_keiku
	   chisell3
	   Satomii_Opera
	   yappyJP
	   tsuda)

for user in ${user_list[@]}; do
    python preprocessing02.py $user
done

