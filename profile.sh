MF=massif.out.fire_planes
EX=fire_planes

echo "###########################"
echo "Time usage by ${EX}:"
time ./${EX}
echo ""
echo "###########################"

echo "###########################"
echo "Memory profiling for ${EX}:"
valgrind --tool=massif --massif-out-file=./${MF} ./${EX}
echo ""
echo "###########################"

massif-visualizer ${MF}
