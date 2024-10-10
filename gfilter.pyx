# cython: language_level=2, boundscheck=False
import numpy as np
cimport numpy as np
cimport cython
import random
from libc.stdlib cimport rand,srand
from libc.time cimport time

cdef sumfilterc (np.uint8_t [:,:] images, np.uint16_t [:,:] output, int xsize, int ysize, int filtersize):
    cdef Py_ssize_t ii
    cdef Py_ssize_t jj
    cdef Py_ssize_t xx
    cdef Py_ssize_t yy
    cdef int fi
    cdef int fj
    cdef np.uint16_t a
    for ii in range(xsize):
        for jj in range(ysize):
            if images[ii][jj]==1:
                a = 0
                for xx in range(-filtersize, filtersize+1):
                    for yy in range(-filtersize, filtersize+1):
                        fi = xx+ii
                        fj = yy+jj
                        if fi>=0:
                            if fi<xsize:
                                if fj>=0:
                                    if fj<ysize:
                                        a = a+images[fi][fj]
                if a>0:
                    a = a-1
                output[ii][jj] = a
    return output

cdef heterofilterc (np.uint8_t [:,:] images, np.uint8_t [:,:] sumn, np.uint16_t [:,:] output, int xsize, int ysize, int filtersize):
    cdef Py_ssize_t ii
    cdef Py_ssize_t jj
    cdef Py_ssize_t xx
    cdef Py_ssize_t yy
    cdef int fi
    cdef int fj
    cdef np.uint16_t a
    for ii in range(xsize):
        for jj in range(ysize):
            if images[ii][jj]==1:
                a = 0
                for xx in range(-filtersize, filtersize+1):
                    for yy in range(-filtersize, filtersize+1):
                        fi = xx+ii
                        fj = yy+jj
                        if fi>=0:
                            if fi<xsize:
                                if fj>=0:
                                    if fj<ysize:
                                        a = a+sumn[fi][fj]
                output[ii][jj] = a

    return output

def heterofilter (np.uint8_t [:,:] images, np.uint8_t [:,:] sumn, np.uint16_t [:,:] output, int xsize, int ysize, int filtersize):
    return heterofilterc(images, sumn, output, xsize, ysize, filtersize)

def sumfilter (np.uint8_t [:,:] images, np.uint16_t [:,:] output, int xsize, int ysize, int filtersize):
    return sumfilterc(images, output, xsize, ysize, filtersize)
##cdef subspacecheckany(int cellid,int[:] subc):
##    cdef Py_ssize_t ii
##    cdef int x
##    x=subc.shape[0]
##    for ii in range(x):
##        if subc[ii]==cellid:
##            return True
##    return False

# cdef class agent:
#     cdef int x
#     cdef int y
#     cdef int xsize
#     cdef int ysize
#     cdef int oldx
#     cdef int oldy
#     cdef int generation
#     cdef public int cellid
#     cdef public int celltype
#     cdef int freetime
#     cdef int divtime
#     cdef public int cluster
#     cdef public int border
#     cdef public int proximatedisabled
#     cdef public list closest
#     cdef public list sensed
#     cdef public list sensedark
#     cdef list avg
#     cdef public list grad
#     cdef public np.int32_t[:] pixx
#     cdef public np.int32_t[:] pixy
#     cdef np.int32_t[:] oldpixx
#     cdef np.int32_t[:] oldpixy
#     cdef public (int,int,int) color
#     cdef int static
#     srand(time(NULL))
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     cpdef ini(self,int ex,int ey,int cellid, dom, int purpose, int gen=0, int exsize=2, int eysize=2):
#
#         self.x=ex
#         self.y=ey
#         self.xsize=exsize
#         self.ysize=eysize
#         self.static=0
#         self.cellid=cellid
#         self.celltype=purpose
#         self.freetime=0
#         self.generation=gen
#         self.divtime=0
#         self.proximatedisabled=0
#         self.cluster=-1
#         self.border=0
#         self.closest=list()
#
# ##        self.sensed=list()
# ##        self.sensedark=list()
#         self.avg=list()
#         self.avg.append(0)
#         self.grad=list()
#
#         if purpose==1:
#             self.pixx=np.asarray([ex+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             self.pixy=np.asarray([ey+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             dom.update(self.pixx,self.pixy,self.cellid)
#             self.color=(255,255,255)
#         if purpose==2:
#             self.static=0
#             self.pixx=np.asarray([ex+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             self.pixy=np.asarray([ey+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             dom.update(self.pixx,self.pixy,self.cellid)
#             self.color=(0,255,255)
#         if purpose==3:
#             self.pixx=np.asarray([ex+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             self.pixy=np.asarray([ey+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             dom.update(self.pixx,self.pixy,self.cellid)
#             self.color=(255,0,0)
#
#         ## for v4.1
#         if purpose==4:
#             #self.pixx=np.asarray([ex+2,ex+2,ex+2,ex+2,ex+2,ex+1,ex+1,ex+1,ex+1,ex+1,ex,ex,ex,ex,ex,ex-1,ex-1,ex-1,ex-1,ex-1,ex-2,ex-2,ex-2,ex-2,ex-2])
#             #self.pixy=np.asarray([ey+2,ey+1,ey,ey-1,ey-2,ey+2,ey+1,ey,ey-1,ey-2,ey+2,ey+1,ey,ey-1,ey-2,ey+2,ey+1,ey,ey-1,ey-2,ey+2,ey+1,ey,ey-1,ey-2])
#             self.pixx=np.asarray([ex+i for i in range (-2,3) for j in range (-2,3)],dtype=np.intc)
#             self.pixy=np.asarray([ey+j for i in range (-2,3) for j in range (-2,3)],dtype=np.intc)
#             #dom.update(self.pixx,self.pixy,self.cellid)
#             self.color=(0,0,255)
#
#     cpdef motile(self,np.uint8_t [:,:] images,imagesint,dom,double sense):
#         cdef int xrand,yrand,lenimx,lenimy
#         #cdef int[:] subspace
#         if self.static==0 and self.celltype==1:
#             self.freetime+=1
#             xrand=rand()%6-3
#             yrand=0
#             lenimx=images.shape[0]
#             lenimy=images.shape[1]
#             self.oldx=self.x
#             self.oldy=self.y
#             self.x=self.x+xrand
#             self.y=self.y+yrand
#             if not (self.x > self.xsize and self.x<lenimx-self.xsize-1 and self.y>self.ysize and self.y<(lenimy-self.ysize-1)):
#
#                 self.x=self.oldx
#                 self.y=self.oldy
#             dom.purge(self.pixx,self.pixy)
#             self.oldpixx=self.pixx
#             self.oldpixy=self.pixy
#             self.pixx=np.asarray([self.x+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             self.pixy=np.asarray([self.y+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             subspace=dom.subspace(self.pixx,self.pixy)
#             if subspacecheckall(0,self.cellid,subspace): #or subspacecheckall(self.cellid,subspace):#np.logical_or(subspace==0,subspace==self.cellid).all():
#                 dom.update(self.pixx,self.pixy,self.cellid)
#             else:
#                 dom.update(self.oldpixx,self.oldpixy,self.cellid)
#                 self.pixx=self.oldpixx
#                 self.pixy=self.oldpixy
#
#         if self.static==0 and self.celltype==3:
#             xrand=rand()%7-3
#             yrand=rand()%7-3
#             lenimx=images.shape[0]
#             lenimy=images.shape[1]
#             self.oldx=self.x
#             self.oldy=self.y
#             self.x=self.x+xrand
#             self.y=self.y+yrand
#             if not (self.x > self.xsize and self.x<lenimx-self.xsize-1 and self.y>self.ysize and self.y<(lenimy-self.ysize-1)):
#                 self.x=self.oldx
#                 self.y=self.oldy
#             dom.purge(self.pixx,self.pixy)
#             self.oldpixx=self.pixx
#             self.oldpixy=self.pixy
#             self.pixx=np.asarray([self.x+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             self.pixy=np.asarray([self.y+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             subspace=dom.subspace(self.pixx,self.pixy)
#
#             if subspacecheckall(0,self.cellid,subspace):# or subspacecheckall(self.cellid,subspace):#np.logical_or(subspace==0,subspace==self.cellid).all():
#                 dom.update(self.pixx,self.pixy,self.cellid)
#
#             else:
#                 dom.update(self.oldpixx,self.oldpixy,self.cellid)
#                 self.pixx=self.oldpixx
#                 self.pixy=self.oldpixy
#             self.visits(imagesint, self.pixx,self.pixy,self.x,self.y,dom)
#         if self.static==0 and self.celltype==4:
#             xrand=random.randint(-1,1)
#             yrand=0#random.randint(-1,1)
#             self.freetime+=1
#             self.oldx=self.x
#             self.oldy=self.y
#             self.x=self.x+xrand
#             self.y=self.y+yrand
#             if not (self.x > 5 and self.x<len(images)-6 and self.y>5 and self.y<(len((images)[0])-6)):
#                 self.x=self.oldx
#                 self.y=self.oldy
#             #dom.purge(self.pixx,self.pixy)
#             self.oldpixx=self.pixx
#             self.oldpixy=self.pixy
#             self.pixx=np.asarray([self.x+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             self.pixy=np.asarray([self.y+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             #subspace=dom.space[self.pixx,self.pixy]
#
#             #dom.update(self.pixx,self.pixy,self.cellid)
#
# ##            else:
# ##                dom.update(self.oldpixx,self.oldpixy,self.cellid)
# ##                self.pixx=self.oldpixx
# ##                self.pixy=self.oldpixy
#             self.storing_grads(images.base)
#             self.quorum(dom,images.base,sense)
#     ##def lightleak(self,
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     def mito(self,dom,dots,norm_im,loww,seeders=0):
#         cdef Py_ssize_t i,indrand
#         cdef int maxchild,parenttype,xoryrand,posrand
#         cdef int[:] dist
#         if self.static==0:
#             self.static=1
#             self.freetime=0
#
#             singlearr=np.asarray([-self.xsize*2+1,self.xsize*2+1],dtype=np.intc)
#             dist=singlearr
#             parenttype= self.celltype
#             if self.celltype==1:
#                 maxchild=5
#             else:
#                 maxchild=16
#             for i in range(maxchild):
#                 if i==0:
#                     childtype=1
#                 if i==1:
#                     childtype=2
#                 if i>1:
#                     childtype=2
#                 xoryrand=rand()%2
#                 #random.randint(0,1)
#                 if xoryrand==0:
#                     indrand=rand()%2#random.randint(0,1)
#                     xrand=self.x+dist[indrand]
#                     posrand=rand()%11-self.xsize*2+1
#
#                     yrand=self.y+posrand#random.randint(-5,5)
#                 if xoryrand==1:
#                     indrand=rand()%2#random.randint(0,1)
#                     yrand=self.y+dist[indrand]
#                     posrand=rand()%11-self.xsize*2+1
#                     xrand=self.x+posrand#random.randint(-5,5)
#
#                 dots=self.child(xrand,yrand,dom,dots,childtype,norm_im,parenttype,loww,seeders)
#
#         return dots
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     def visits(self,int [:,:] imagesint,int[:] pixx,int[:] pixy, int selfx, int selfy, dom):
#         cdef double varall,darkall,whiteall
#         varall=dom.subtoutarr[selfx,selfy]#subtout(imagesint,pixx,pixy,selfx,selfy,dom.subtoutarr[selfx,selfy])
#         darkall,whiteall=dom.avgarr[selfx,selfy],255-dom.avgarr[selfx,selfy]#avgpixint(imagesint,pixx,pixy,dom.avgarr[selfx,selfy])
#         #a=np.int32(images.base[self.pixx,self.pixy])
# ##        self.sensed.extend([varall])
# ##        self.sensedark.extend([darkall])
#         #self.sensed.extend([np.abs(np.subtract.outer(a,a)[np.tril_indices(a.shape[0],k=-1)]).var()])
#         #print(varall,self.sensed[len(self.sensed)-1])
#         self.grad.extend([1])#np.abs(ss.skew(a))])
#
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     def storing_grads(self,images):
#         a=images[self.pixx,self.pixy]
#         self.avg.extend([np.mean(a)])
#         self.grad.extend([self.avg[len(self.avg)-1]-self.avg[len(self.avg)-2]])
#
#
#
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     cdef child(self,int ex,int ey,dom,dots,int purpose,np.uint8_t [:,:] norm_im,int parent,double loww,seeders):
#         cdef int lendot,lendotx,lendoty,genx,exsize,eysize,genz
#         cdef double avg1,avg2
#         cdef int[:] subspace
#         cdef double newloww
#         lendotx=len(dom.space)
#         lendoty=len(dom.space[0])
#         if purpose==1:
#             if  (ex > self.xsize and ex<lendotx-self.xsize-1 and ey>self.ysize and ey<(lendoty-self.ysize-1)):
#                 pixx=np.asarray([ex+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#                 pixy=np.asarray([ey+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#                 subspace=dom.subspace(pixx,pixy)
#                 #print subspace
# ##                stat=pytime.time()
#                 if subspacecheckall(0,0,subspace):#not (subspace>0).any():
#                     dots.append(agent())
#                     lendot=len(dots)-1
#                     dots[lendot].ini(ex,ey,lendot,dom,purpose)
# ##                    last=pytime.time()
# ##                    if last-stat>0.0001:
# ##                       print (last-stat," time for child")
#             return dots
#         if purpose==2:
#             pixx=np.asarray([ex+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             pixy=np.asarray([ey+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#             if rand()%2==1:
#                 exsize = 1
#                 eysize = 1
#                 genz = 2
#             else:
#                 exsize = 2
#                 eysize = 2
#                 genz = 6
#             if  (ex > self.xsize and ex<lendotx-self.xsize-1 and ey>self.ysize and ey<(lendoty-self.ysize-1)):
#                 #print (self.type2values(pixx,pixy,norm_im))
#                 qspace=dom.qsubspace(pixx,pixy)
# ##                stat=pytime.time()
#                 avg1=self.type2values(pixx,pixy,norm_im,dom)
#                 avg2=self.type2values(pixx,pixy,norm_im,dom)
#                 newloww = loww+loww*0.05*self.generation*(self.generation<genz)
#                 #print (self.generation,newloww)
#                 if avg1<=newloww or not subspacecheckall(0,0,qspace):#(qspace>0).any():
#
#                     subspace=dom.subspace(pixx,pixy)
#                     #print subspace
#                     if subspacecheckall(0,0,subspace):#not (subspace>0).any():
#                         dots.append(agent())
#                         lendot=len(dots)-1
#
#                         if avg1<loww:
#                             genx = 1
#                         else:
#                             genx = self.generation+1
#                         dots[lendot].ini(ex,ey,lendot,dom,purpose, genx,exsize,eysize)
#
#                         if parent==1:
#
#                             seeders.update(lendot)
# ##                        last=pytime.time()
# ##                        if last-stat>0.00005:
# ##                           print (last-stat," time for child")
#                 return dots
#         if purpose==4:
#             if  (ex > 5 and ex<lendotx-6 and ey>5 and ey<(lendoty-6)):
#                 self.pixx=np.asarray([ex+i for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#                 self.pixy=np.asarray([ey+j for i in range (-self.xsize,self.xsize+1) for j in range (-self.ysize,self.ysize+1)],dtype=np.intc)
#                 subspace=dom.subspace(pixx,pixy)
#                 #if not (subspace>0).any():
#                 lendot=len(dots)-1
#                 dots.append(agent())
#                 dots[lendot].ini(ex,ey,lendot,dom,purpose)
#             return dots
#         return dots
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     def values(self,np.uint8_t [:,:] norm_im,int[:,:] imagesint,dom,dots,int maxupp,int upp,int loww,int minloww,int purpose, seeders):
#
#         if purpose==1:
#
#             variasloc=dom.subtoutarr[self.x,self.y]#subtout(imagesint,self.pixx,self.pixy,self.x,self.y,dom.subtoutarr[self.x,self.y])
#             #a=np.int32(norm_im[self.pixx,self.pixy])
#             #variasloc=np.abs(np.subtract.outer(a,a)[np.tril_indices(a.shape[0],k=-1)]).var()
#
#             if  variasloc > upp and variasloc < maxupp:
#                 self.mito(dom,dots,norm_im,loww,seeders)
#         if purpose==2:
#             self.divtime+=1
#
#             if self.divtime<3:
#                 self.mito(dom,dots,norm_im,loww)
#
#         return dots
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     def type2values(self,int[:] pixx,int[:] pixy,np.uint8_t [:,:] norm_im,dom):
#         #avgpi=norm_im.base[pixx.base,pixy.base].mean()
#
#         avgpixx,avgpixx2=dom.avgarr[self.x,self.y],255-dom.avgarr[self.x,self.y]#avgpix(norm_im,pixx,pixy,dom.avgarr[self.x,self.y])#change log v4.1
#         #print (avgpixx,avgpi)
# ##        a=np.int32(norm_im[self.pixx,self.pixy])
# ##        avgpixx=np.abs(ss.skew(a))
#         return avgpixx
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     def kill(self,dots,dom):
#         if self.celltype==1 and self.freetime>200:
#             dots[self.cellid]=0
#             dom.update(self.pixx,self.pixy,0)
#         if self.celltype==4 and self.freetime>10:
#             dots[self.cellid]=0
#             #dom.update(self.pixx,self.pixy,0)
#     @cython.boundscheck(False)
#     @cython.wraparound(False)
#     def neighbours(self,dots,dom):
#
#         neighboursites=[(self.x+i,self.y+j) for i in range (-self.xsize-1,self.xsize+1) for j in range (-self.xsize-1,self.xsize+1) if self.x+i > 0 and self.x+i < len(dom.space)-1 and self.y+j >0 and self.y+j < len(dom.space[0])-1]
#         neighboursitesx,neighboursitesy=np.asarray(neighboursites).T
#         neighboursitesx=neighboursitesx.astype(np.int32)
#         neighboursitesy=neighboursitesy.astype(np.int32)
#         allneighbours=dom.subspace(neighboursitesx,neighboursitesy)
#         allneighbours=allneighbours.base
#         allneighbours=allneighbours[allneighbours>0]
#         allneighbours=allneighbours[allneighbours!=self.cellid]
#         allneighbours=(np.unique(allneighbours)).tolist()
#         for i in allneighbours:
#             if dots[i].celltype==2:
#                 self.proximatedisabled=1
#
#         self.closest.append(allneighbours)
#
#     def quorum(self,dom,images,sense):
#         diff=(np.max(images[self.pixx,self.pixy])-np.min(images[self.pixx,self.pixy]))
#         meanu=np.mean(images[self.pixx,self.pixy])
#
#         if ((diff<50) and meanu<sense):
#             dom.quorum_update(self.pixx,self.pixy)
