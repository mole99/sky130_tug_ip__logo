all: gds/sky130_tug_ip__logo.gds

gds/sky130_tug_ip__logo.gds: img/TU_Graz.png
	python3 python/make_gds.py img/TU_Graz.png gds/sky130_tug_ip__logo.gds --cellname sky130_tug_ip__logo --scale 0.4 --threshold 128 --invert --merge
.PHONY: gds/sky130_tug_ip__logo.gds

clean:
	rm -f gds/sky130_tug_ip__logo.gds
.PHONY: clean
