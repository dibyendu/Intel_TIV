(define (domain arm_domain)
  (:types data - object)
(:predicates (idle_dram_addr ?x)
             (cExpire_dram_addr ?x)
             (cke)
             (d_cache_avail)
             (valid_addr ?x)
             (busIdle)
	     (DMA_descriptor)
	     (DMA_En)
	     (Device_En)
             (refresh_addr ?x)
             (writeReq ?x)
             (blockBus)
             (d_cache_full)
             (readMiss ?x)
             (replace ?x)
             (dirty ?x)
	     (inWriteBack ?x)
	     (BusRQ)
	     (readReq ?x)
	     (DMA_active_sig)
	     (Out_data ?x)
	     (readReqAck ?x)	     
)



(:action TimeOut
:parameters (?x - data)
:precondition (not (cExpire_dram_addr ?x)) 
                   
:effect (cExpire_dram_addr ?x))



(:action Self_refresh
:parameters(?x - data)
:precondition(and (idle_dram_addr ?x) (cExpire_dram_addr ?x))
:effect(refresh_addr ?x)
)


(:action cke_high
:parameters(?x - data)
:precondition(and (not (cke)) (refresh_addr ?x) (writeReq ?x))
:effect(cke)
)


(:action Load_D_Cache
:parameters()
:precondition(d_cache_avail)
:effect(d_cache_full)
)


(:action LRU_selection
:parameters(?x ?y - data)
:precondition(and (d_cache_full) (readMiss ?y))
:effect(and (replace ?x)(not (valid_addr ?x)))
)


(:action WriteBackEntry
:parameters(?x - data)
:precondition(and (replace ?x) (dirty ?x))
:effect(inWriteBack ?x)
)


(:action ReadMiss
:parameters(?x - data)
:precondition( and (not (valid_addr ?x)) (readReq ?x))
:effect(readMiss ?x)
)


(:action Modify
:parameters(?x - data)
:precondition(valid_addr ?x)
:effect(dirty ?x)
)


(:action Channel_block
:parameters()
:precondition(and (BusRQ) (busIdle))
:effect(blockBus)
)

(:action Write_R
:parameters(?x - data)
:precondition(inWriteBack ?x)
:effect(and (writeReq ?x)(BusRQ))
)

(:action Read_N
:parameters(?x - data)

:effect(readReq ?x)
)

(:action DMA_active
:parameters()
:precondition(and (DMA_descriptor)(DMA_En))
:effect(DMA_active_sig)
)

(:action Device_active
:parameters(?x - data)
:precondition(Device_En)
:effect(Out_data ?x)
)

(:action Write_D
:parameters(?x - data)
:precondition(and (DMA_active_sig)(Out_data ?x))
:effect(and (writeReq ?x)(BusRQ))
) 

(:action ReadReqServe
:parameters(?x - data)
:precondition(readMiss ?x)
:effect(readReqAck ?x)
)  )
