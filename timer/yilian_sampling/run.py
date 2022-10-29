# -*- coding: utf-8 -*-
import os
import csv
import commands
import time

'''Error Code'''
STATUS_OK       = 0
STATUS_TIMEOUT  = 1001

'''运行插桩程序进行采样'''
def case_run(np,nt):
    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave')
    # assert os.system('make') == 0, "complie GOMO failed"
    os.chdir('./bin')
    cmd="bsub -I -b -q q_share -share_size 7000 -host_stack 2048 -n " + str(np) + " -cgsp " + str(nt) +" -exclu ./GOMO | tee l"
    print('>>>'+cmd)
    os.system(cmd)

def check_run():
    timeout=0
    while 1:
        time.sleep(30)
        output=commands.getoutput("bjobs -J GOMO")
        if output=="No match record found!":
            break
        timeout+=30
        if(timeout>=60*30):
            os.system("bjobs -J GOMO")
            os.system("bkill -J GOMO")
            return STATUS_TIMEOUT
    return STATUS_OK

'''处理采样数据'''
def deal_sampling_data(nt,Np):
    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave/sampling/timer')
    for np in Np:
        command="rm -f result/"+str(nt)+"/"+str(np)+".csv"
        os.system(command)
        command="sh func_trace.sh ../../bin/GOMO ./out/"+str(np)+"_time.csv ./result/"+str(nt)+"/"+str(np)+".csv"
        os.system(command)

'''处理使得到待拟合数据'''
def get_fit_data(Nt,Np):
    fit_x=dict()
    fit_y=dict()
    flag=0

    os.chdir('/home/export/online1/mdt00/shisuan/swliuyao/oa/OA/GOMO.slave/sampling/timer/result')
    outx = open("../../trainX"+".csv",'w')
    outy = open("../../trainY"+".csv",'w')
    timefile = open("../../Toriginal.csv",'a')
    for nt in Nt:
        for np in Np:
            sampling_file = "./" +str(nt)+"/"+ str(np) + ".csv"
            orginal_data = csv.reader(open(sampling_file, 'r'))

            error_time=0
            out_time=0
            out_time2=0
            selftime=dict()

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
            
            for func in selftime:
                functime = selftime[func]
                fit_x.setdefault(func,[func])
                fit_x[func].append(nt)
                fit_x[func].append(np)
                fit_y.setdefault(func,[func])
                fit_y[func].append(functime)
                if functime > 0:
                    out_time+=functime
                else:
                    out_time2-=functime
            # timefile.write(str(nproc)+","
            #     +str(out_time/1000000)+","
            #     +str(int(1.0*out_time2/1000000))+","
            #     +str(int(1.0*error_time/1000))+"\n")

            timefile.write(str(nt)+","+str(np)+","+str(out_time/1000000)+"\n")
            print("nthread = %d, nproc = %d, alltime = %d ms, alltime2 = %d ms, error_time = %d ns"%(nt,np, out_time/1000000,1.0*out_time2/1000000,1.0*error_time/1000))
    # print(fit_x)
    for line in fit_x:    
        outx.write(",".join(str(i) for i in fit_x[line])+"\n")
    for line in fit_y:
        outy.write(",".join(str(i) for i in fit_y[line])+"\n")


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
    timefile.write(",".join(str(p) for p in Np)+"\n")
    timefile.close()
    # deal_sampling_data(64,Np)

    if CASERUN:
        for nt in Nt:
            command="export NT_NUMS="+str(nt)
            os.system(command)
            # for np in Np:
            #     case_run(np,nt)
            
            status=check_run()
            if(status == STATUS_OK):
                print("Succeed: nt=%d, status=%d!"%(nt,status))
                deal_sampling_data(nt,Np)
            else:
                print("ERROR: nt=%d, status=%d!"%(nt,status))


    get_fit_data(Nt,Np)
    
    # fit()
        

    print('Run PROFILING_RUN Successfully!')


if __name__ == '__main__':
    CASERUN=False
    
    # sampling_procs=[4,6,16,24,36,48,52,64,84,96]
    # sampling_procs=[4,8,16,32,64,128,256,512,1024,2048]
    # sampling_procs=[300,400,512,600,768,860,1024,1280,1560,2048]
    # sampling_procs=[300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1600,1700,1800,1900,2000,2100,2200]
    # sampling_procs=[600,684,720,800,860,900,1024,1280,1360,1420]
    # Np=[20,40,60,80,100]
    Np=[400,600,800,1000,1200]
    Nt=[16,32,48,64]
    main()