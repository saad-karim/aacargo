# for track in 87654321 41062372 41166414 43615434
# do 
#   time curl -v http://localhost:5000/track\?awbCode\=001\&awbNumber\=$track
# done

time curl -v http://localhost:5000/track\?awbCode\=001\&awbNumber\=87654321 &
time curl -v http://localhost:5000/track\?awbCode\=001\&awbNumber\=41166414 &
time curl -v http://localhost:5000/track\?awbCode\=001\&awbNumber\=43615434 &
time curl -v http://localhost:5000/track\?awbCode\=001\&awbNumber\=41062372 &