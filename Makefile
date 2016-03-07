PYTHON := python
MD5 := md5sum -c

kuro10_FLAGS  := -DKURO
aka10_FLAGS   := -DAKA
shiro10_FLAGS := -DSHIRO

.SUFFIXES: 
.PHONY: all clean compare
.SECONDEXPANSION:

debichiru_obj := \
	main.o

roms := kuro10.gbc

all: $(roms)

clean:
	rm -f $(debichiru_obj)
	rm -f $(roms:.gbc=.map)
	rm -f $(roms:.gbc=.sym)
	rm -f $(roms)

compare: $(roms)
	@$(MD5) roms.md5

%.asm: ;

%.gbc : $(debichiru_obj)
	rgblink -n $(basename $@).sym -m $(basename $@).map -p 0x00 -o $@ $^

$(debichiru_obj): %.o : %.asm
	rgbasm -h $($(basename $(notdir $@))_FLAGS) -o $@ $<
