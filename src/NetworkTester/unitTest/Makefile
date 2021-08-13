python= python2
tests=	testSource\
	testTime\
	dante\
	acn\
	dante\
	lake\
	ptp

test : $(tests:=.result)

%.result: %.py
	$(python) $<

