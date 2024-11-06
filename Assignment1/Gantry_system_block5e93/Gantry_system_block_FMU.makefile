# FIXME: before you push into master...
RUNTIMEDIR=/usr/bin/../include/omc/c/
#COPY_RUNTIMEFILES=$(FMI_ME_OBJS:%= && (OMCFILE=% && cp $(RUNTIMEDIR)/$$OMCFILE.c $$OMCFILE.c))

fmu:
	rm -f Gantry_system_block.fmutmp/sources/Gantry_system_block_init.xml
	cp -a "/usr/bin/../share/omc/runtime/c/fmi/buildproject/"* Gantry_system_block.fmutmp/sources
	cp -a Gantry_system_block_FMU.libs Gantry_system_block.fmutmp/sources/

