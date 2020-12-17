for track in 87654321 41062372
do 
  time curl -v http://localhost:5000/track\?awbCode\=001\&awbNumber\=$track
done