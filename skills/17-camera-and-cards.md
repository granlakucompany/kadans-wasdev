# Skill: camera moves and cut-out cards

On image/video scenes: `camera:{from:{zoom,x,y}, to:{zoom,x,y}, ease:inout|out|punch|linear}` for a real
zoom/pan; `cards:[{crop:[x,y,w,h], at:[x,y], width, from:left|right|up|down, rotate, enter, pill?, icon?}]`
for cut-out cards that fly in. `layout:"window"` puts a rounded 9:16 window over a blurred backdrop.
