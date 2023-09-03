##PBS -N patterns-7
##PBS -q front
##PBS -l nodes=1:ppn=8
##PBS -l walltime=99:59:00
###PBS -r n
##PBS -j oe
###PBS -S /bin/csh -V

#SBATCH -J patterns
#SBATCH -p normal
#SBATCH -t 99:59:00
#SBATCH -N 1
##SBATCH --ntasks-per-node=20
#SBATCH --ntasks-per-node=60
##SBATCH -o log.%j
##SBATCH -e log.%j
#SBATCH --exclusive


cd /data/wujx01/EARthLab_UQ/TaskOptimize_FunLayer/layout_balancing/patterns
source activate uq

python generate_patterns.py 3