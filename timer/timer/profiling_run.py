# -*- coding: utf-8 -*-
import os
import csv

'''运行插桩程序进行采样'''
def case_run(nproc):
    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave')
    # assert os.system('make') == 0, "complie GOMO failed"
    os.chdir('./bin')
    command="bsub -b -I -q q_share -share_size 7000 -host_stack 2048 -n " + str(nproc) + " -cgsp 32 -exclu ./GOMO | tee l"
    os.system(command)

'''处理采样数据'''
def deal_sampling_data(nproc):
    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave/sampling/timer')
    command="rm -f result/"+str(nproc)+".csv"
    os.system(command)
    command="sh func_trace.sh ../../bin/GOMO ./out/0_time.out ./result/"+str(nproc)+".csv"
    os.system(command)

'''处理使得到待拟合数据'''
def get_fit_data():
    fit_data=[]
    flag=0

    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave/sampling/timer/result')
    outfile = open("../../fit_data"+".csv",'w')
    timefile = open("../../Toriginal.csv",'a')
    outfile.write("id,funcname,")
    outfile.write(",".join(str(i) for i in sampling_procs)+'\n')
    # outfile.write("id,func_name,self_time1,self_time2,self_time3,self_time4\n")
    for nproc in sampling_procs:
        sampling_file = "./" + str(nproc) + ".csv"
        orginal_data = csv.reader(open(sampling_file, 'r'))
        selftime=dict()
        error_time=0
        out_time=0
        out_time2=0

        for line in orginal_data:
            son=line[0]
            fa=line[1]
            acctime=line[3]
            wholetime=line[4]
            selftime.setdefault(son,0)
            selftime.setdefault(fa,0)
            selftime[son]=selftime[son]+int(acctime)
            selftime[fa]=selftime[fa]-int(wholetime)
            error_time+=int(wholetime)-int(acctime)
        
        if flag==0:
            flag=1
            idx=0
            for func in selftime:
                fit_data.append([idx,func])
                idx+=1
#note:此时保证所有计时输出的函数顺序及数量一致
        idx=0
        for func in selftime:
            functime = selftime[func]
            fit_data[idx].append(functime)
            idx+=1
            if functime > 0:
                out_time+=functime
            else:
                out_time2-=functime
        # timefile.write(str(nproc)+","
        #     +str(out_time/1000000)+","
        #     +str(int(1.0*out_time2/1000000))+","
        #     +str(int(1.0*error_time/1000))+"\n")
        timefile.write(str(out_time/1000000)+"\n")
        print("nproc = %d, alltime = %d ms, alltime2 = %d ms, error_time = %d ns"%(nproc, out_time/1000000,1.0*out_time2/1000000,1.0*error_time/1000))
    for line in fit_data:    
        outfile.write(",".join(str(i) for i in line)+"\n")


'''拟合'''
def fit():
    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave/sampling/')
    command = "swpython fit.py >/dev/null 2>&1"
    os.system(command)
    print('fit')

'''主程序'''
def main():
    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave/sampling/')
    timefile = open("./Toriginal.csv",'a')
    timefile.write(",".join(str(p) for p in sampling_procs)+"\n")
    timefile.close()
    if CASERUN:
        for nproc in sampling_procs:
            print('case run in ' + str(nproc) + ' nprocs')
            case_run(nproc)
            deal_sampling_data(nproc)

    get_fit_data()
    
    # fit()
        

    print('Run PROFILING_RUN Successfully!')


if __name__ == '__main__':
    CASERUN=False
    
    # sampling_procs=[4,6,16,24,36,48,52,64,84,96]
    # sampling_procs=[4,8,16,32,64,128,256,512,1024,2048]
    # sampling_procs=[300,400,512,600,768,860,1024,1280,1560,2048]
    # sampling_procs=[300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1600,1700,1800,1900,2000,2100,2200]
    # sampling_procs=[600,684,720,800,860,900,1024,1280,1360,1420]
    sampling_procs=[300,500]

    main()