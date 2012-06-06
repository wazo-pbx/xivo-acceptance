import psutil, sys

def print_mem(n, name, title):

    arguments = sys.argv

    if sys.platform == 'win32':
        import os, msvcrt
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    if len(arguments) > 1:
        if arguments[1] == 'config':
            print 'graph_order xc_mem_rss xc_mem_vms'
            print 'graph_title ' + title
            print 'graph_args --vertical-label MBytes'
            print 'graph_category xivo'
            print 'graph_info This graph the memory consumption of xivoclient'
            print 'xc_mem_rss.label Xivoclient Resident memory'
            print 'xc_mem_rss.draw AREA'
            print 'xc_mem_vms.label Xivoclient Virtual memory'
            print 'xc_mem_vms.draw LINE2'
            if sys.platform == 'win32':
                print '.'
                exit()
        elif arguments[1] == 'name':
            print name
            exit()

    if sys.platform == 'win32':
        PROCNAME = "xivoclient.exe"
    else:
        PROCNAME = 'xivoclient'

    xc_pid = []
    for proc in psutil.process_iter():
        if proc.name == PROCNAME:
            xc_pid.append(proc.pid)

    if len(xc_pid) < n + 1:
        print 'xc_mem_rss.value 0'
        print 'xc_mem_vms.value 0'
        if sys.platform == 'win32':
            print '.'
        exit()

    handler = psutil.Process(xc_pid[n])
    if sys.platform == 'win32':
        xc_mem_stats = handler.get_memory_info()
        xc_mem_rss = xc_mem_stats.rss
        xc_mem_vms = xc_mem_stats.vms
    else:
        xc_mem_rss, xc_mem_vms = handler.get_memory_info()

    print 'xc_mem_rss.value ' + str(xc_mem_rss/1024/1024)
    print 'xc_mem_vms.value ' + str(xc_mem_vms/1024/1024)
    if sys.platform == 'win32':
        print '.'

