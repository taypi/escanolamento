class Process(object):
    def __init__(self, pid, arrivingTime, nPeaks = 0, peaks = [], timeWaiting = 0, 
                 endTime = 0, processingTime = 0, timeInReady = 0, turnAround = 0, 
                 arrivedTime = 0, timeDoing = 0, done = False, peak = 0):
        super(Process, self).__init__()
        self.pid = pid
        self.arrivingTime = arrivingTime
        self.nPeaks = nPeaks
        self.peaks = peaks
        self.timeWaiting = timeWaiting
        self.endTime = endTime
        self.processingTime = processingTime
        self.timeInReady = timeInReady
        self.turnAround = turnAround
        self.arrivedTime = arrivedTime
        self.timeDoing = timeDoing
        self.done = done
        self.peak = peak
    
    def printP(self):
        print("no peaks - pid:",self.pid,"arrivingTime:",self.arrivingTime,"nPeaks:",self.nPeaks,
              'peaks:', self.peak , '/' , self.peaks, "processingTime:", self.processingTime,
              "timeInReady:", self.timeInReady)

def getKey(process):
    return process.peaks[0]

def importData():
    try:
        with open("especificacoes/processos.dat", "r") as openFile:
            processes = []
            for line in openFile:
                peaks = []
                line = line.split(" ")
                pid = int(line.pop(0))
                arrivingTime = int(line.pop(0))
                nPeaks = int(line.pop(0))
                line.pop() #excluindo '\n'
                for peak in line:
                    peaks.append(int(peak))
                processes.append(Process(pid, arrivingTime, nPeaks, peaks))
        return processes
    except IOError:
        print("INFO: importData() failed")

def exportData(algorithm, list1, list2, list3):
    mediumTime = [0, 0, 0]
    try:
        with open("resultados/log1" + str(algorithm) + ".dat","w") as log1:
            log1.write("%s \n" %algorithm)
            log1.write("ID Tempo_de_Chegada Tempo_de_finalizacao Tempo_de_Processamento Tempo_de_Espera Tempo_de_Turnaround \n")
            for process in list1:
                log1.write("%s %s %s %s %s %s \n" %(process.pid, process.arrivingTime, process.endTime, process.processingTime, process.timeInReady, process.turnAround))
                mediumTime[0] += process.processingTime
                mediumTime[1] += process.timeInReady
                mediumTime[2] += process.turnAround
            for i in range(len(mediumTime)):
                mediumTime[i] /= len(list1)
    except IOError:
        print("IOError: could not write log1")

    try:
        with open("resultados/log2" + str(algorithm) + ".dat","w") as log2:
            log2.write("%s \n" %algorithm)
            log2.write("Tempo Processos_Fila_Pronto Processos_Fila_Bloqueado Processos_Finalizados \n")
            for i in range(len(list2['count'])):
                log2.write("%s %s %s %s \n" %(list2['count'][i], list2['ready'][i], list2['waiting'][i], list2['finished'][i]))
    except IOError:
        print("IOError: could not write log2")

    try:
        with open("resultados/log3" + str(algorithm) + ".dat","w") as log3:
            log3.write("%s \n" %algorithm)
            log3.write("Valor_Atual_do_Ciclo Tempo_Medio_Processamento Tempo_Medio_Espera Tempo_Medio_Turnaround Tempo_CPU_Ocupada Taxa_Ocupacao Tempo_CPU_Ociosa Taxa_Ociosidade \n")
            log3.write("%s %s %s %s %s %s %s %s \n" %(list3['total'], mediumTime[0], mediumTime[1], mediumTime[2], list3['busy'], list3['busy']/list3['total'], list3['total']-list3['busy'], (list3['total']-list3['busy'])/list3['total']))
    except IOError:
        print("IOError: could not write log2")

def fcfsOld():
    processes = importData()
    # for process in processes:
        # print("pid:",process.pid,"arrivingTime:",process.arrivingTime,"nPeaks:",process.nPeaks, "peaks:", process.peaks, "processingTime:", process.processingTime, "timeInReady:", process.timeInReady)
    # print("================================================================")
    algorithm = "FCFS"
    count = 0
    busy = 0
    READYSIZE = 10
    log2 = {'count':[], 'ready':[], 'waiting':[], 'finished':[]}
    ready = []
    waiting = []
    doing = []
    finished = []
    while processes or ready or waiting or doing:
        while len(ready)+len(waiting)+len(doing) < READYSIZE and processes and processes[0].arrivingTime <= count:
            processes[0].arrivedTime = count
            ready.append(processes.pop(0))
        if ready and not doing:
            doing.append(ready.pop(0))
            # if not doing[0].done:
            #     doing[0].timeInReady = count - doing[0].arrivedTime
            #     doing[0].done = True
        if doing:
            # print(doing[0].pid, " ", doing[0].processingTime)
            busy += 1
            if doing[0].peaks[0] == 0:
                doing[0].peaks.pop(0)
                if not doing[0].peaks:
                    doing[0].endTime = count
                    # print("no peaks - pid:",doing[0].pid,"arrivingTime:",doing[0].arrivingTime,"nPeaks:",doing[0].nPeaks, 
                    #       "peaks:", doing[0].peaks, "processingTime:", doing[0].processingTime, "count:", count, "timeInReady:", process.timeInReady)
                    doing[0].turnAround = count - doing[0].arrivedTime
                    finished.append(doing.pop(0))
                else:
                    doing[0].timeWaiting = 10
                    # print("no peaks - pid:",doing[0].pid,"arrivingTime:",doing[0].arrivingTime,"nPeaks:",doing[0].nPeaks, 
                    #       "peaks:", doing[0].peaks, "processingTime:", doing[0].processingTime, "count:", count, "timeInReady:", process.timeInReady)
                    waiting.append(doing.pop(0))
            else:
                doing[0].peaks[0] -= 1
                doing[0].processingTime += 1
                # print("decremented peak: ", doing[0].pid, " ", doing[0].processingTime)
        if waiting:
            for next in waiting:
                next.processingTime += 1
            if waiting[0].timeWaiting == 0:
                ready.append(waiting[0])
                waiting.remove(waiting[0])
            if waiting:
                waiting[0].timeWaiting -= 1

        if count % 200 == 0:
            log2['count'].append(count)
            log2['ready'].append(len(ready))
            log2['waiting'].append(len(waiting))
            log2['finished'].append(len(finished))

        if ready:
            for next in ready:
                next.timeInReady += 1

        count += 1

            # print(ready[0].pid)
            # ready.pop(0)
        # process = processes.pop()
        # print("pid:",process.pid,"arrivingTime:",process.arrivingTime,"nPeaks:",process.nPeaks)
    # for f in finished:
    #     print(f.pid, " ", f.processingTime)

    # for process in finished:
    #     print("pid:",process.pid,"arrivingTime:",process.arrivingTime,"nPeaks:",process.nPeaks, "peaks:", process.peaks, "processingTime:", process.processingTime, "timeInReady:", process.timeInReady)

    # print("count:", count)

    log3 = {'total' : count, 'busy' : busy}

    exportData(algorithm, finished, log2, log3)


def fcfs():
    IO_TIME = 10
    processes = importData()
    algorithm = "FCFS"
    count = 0
    busy = 0
    READYSIZE = 10
    log2 = {'count':[], 'ready':[], 'waiting':[], 'finished':[]}
    ready = []
    waiting = []
    doing = []
    finished = []
    while processes or ready or waiting or doing:

        while len(ready)+len(waiting)+len(doing) < READYSIZE and processes and processes[0].arrivingTime <= count:
            processes[0].arrivedTime = count
            ready.append(processes.pop(0))

        count += 1

        if ready:
            if not doing:
                doing.append(ready.pop(0))
            for next in ready:
                next.timeInReady += 1

        if doing:
            busy += 1
            doing[0].processingTime += 1
            doing[0].peak += 1

            if not doing[0].peak < doing[0].peaks[0]:
                # doing[0].printP()

                doing[0].peaks.pop(0)
                doing[0].peak = 0
                if not doing[0].peaks:
                    doing[0].endTime = count
                    doing[0].turnAround = count - doing[0].arrivedTime
                    finished.append(doing.pop(0))
                else:
                    doing[0].timeWaiting = -1
                    waiting.append(doing.pop(0))

        if waiting:
            for next in waiting:
                if not next.timeWaiting < 0:
                    next.processingTime += 1
            waiting[0].timeWaiting += 1
            if not waiting[0].timeWaiting < IO_TIME:
                ready.append(waiting.pop(0))

        if count % 200 == 0:
            log2['count'].append(count)
            log2['ready'].append(len(ready))
            log2['waiting'].append(len(waiting))
            log2['finished'].append(len(finished))


    log3 = {'total' : count, 'busy' : busy}

    exportData(algorithm, finished, log2, log3)

def sjf():
    IO_TIME = 10
    processes = importData()
    algorithm = "SJF"
    count = 0
    busy = 0
    READYSIZE = 10
    log2 = {'count':[], 'ready':[], 'waiting':[], 'finished':[]}
    ready = []
    waiting = []
    doing = []
    finished = []
    while processes or ready or waiting or doing:

        while len(ready)+len(waiting)+len(doing) < READYSIZE and processes and processes[0].arrivingTime <= count:
            processes[0].arrivedTime = count
            ready.append(processes.pop(0))

        count += 1

        if ready:
            ready = sorted(ready, key=getKey)
            if not doing:
                doing.append(ready.pop(0))
            for next in ready:
                next.timeInReady += 1

        if doing:
            busy += 1
            doing[0].processingTime += 1
            doing[0].peak += 1

            if not doing[0].peak < doing[0].peaks[0]:
                # doing[0].printP()

                doing[0].peaks.pop(0)
                doing[0].peak = 0
                if not doing[0].peaks:
                    doing[0].endTime = count
                    doing[0].turnAround = count - doing[0].arrivedTime
                    finished.append(doing.pop(0))
                else:
                    doing[0].timeWaiting = -1
                    waiting.append(doing.pop(0))

        if waiting:
            for next in waiting:
                if not next.timeWaiting < 0:
                    next.processingTime += 1
            waiting[0].timeWaiting += 1
            if not waiting[0].timeWaiting < IO_TIME:
                ready.append(waiting.pop(0))

        if count % 200 == 0:
            log2['count'].append(count)
            log2['ready'].append(len(ready))
            log2['waiting'].append(len(waiting))
            log2['finished'].append(len(finished))


    log3 = {'total' : count, 'busy' : busy}

    exportData(algorithm, finished, log2, log3)

def roundRobin():
    IO_TIME = 10
    ROUND_TIME = 20
    processes = importData()
    algorithm = "RR"
    count = 0
    busy = 0
    READYSIZE = 10
    log2 = {'count':[], 'ready':[], 'waiting':[], 'finished':[]}
    ready = []
    waiting = []
    doing = []
    finished = []
    while processes or ready or waiting or doing:

        while len(ready)+len(waiting)+len(doing) < READYSIZE and processes and processes[0].arrivingTime <= count:
            processes[0].arrivedTime = count
            ready.append(processes.pop(0))

        count += 1

        if ready:
            if not doing:
                doing.append(ready.pop(0))
            for next in ready:
                next.timeInReady += 1

        if doing:
            busy += 1
            doing[0].processingTime += 1
            doing[0].peak += 1
            doing[0].timeDoing += 1

            if not doing[0].peak < doing[0].peaks[0]:
                # doing[0].printP()

                doing[0].peaks.pop(0)
                doing[0].peak = 0
                if not doing[0].peaks:
                    doing[0].endTime = count
                    doing[0].turnAround = count - doing[0].arrivedTime
                    finished.append(doing.pop(0))
                else:
                    doing[0].timeWaiting = -1
                    waiting.append(doing.pop(0))
            else:
                if not doing[0].timeDoing < ROUND_TIME:
                    # doing[0].printP()

                    doing[0].timeDoing = 0
                    ready.append(doing.pop(0))

        if waiting:
            for next in waiting:
                if not next.timeWaiting < 0:
                    next.processingTime += 1
            waiting[0].timeWaiting += 1
            if not waiting[0].timeWaiting < IO_TIME:
                ready.append(waiting.pop(0))

        if count % 200 == 0:
            log2['count'].append(count)
            log2['ready'].append(len(ready))
            log2['waiting'].append(len(waiting))
            log2['finished'].append(len(finished))

    log3 = {'total' : count, 'busy' : busy}

    exportData(algorithm, finished, log2, log3)

if __name__ == '__main__':
    fcfs()
    sjf()
    roundRobin()
