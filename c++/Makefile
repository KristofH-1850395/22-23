all: bachelor bachelor-finite contact contact-finite

contact: bin
	g++ -fopenmp -lpthread -o bin/contact.o src/main/cpMain.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

contact-finite: bin
	g++ -fopenmp -lpthread -o bin/contact-finite.o src/main/cpMainFinite.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

bachelor: bin
	g++ -fopenmp -lpthread -o bin/bachelor.o src/main/bpMain.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

bachelor-finite: bin
	g++ -fopenmp -lpthread -o bin/bachelor-finite.o src/main/bpMainFinite.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

bin:
	mkdir bin 2> /dev/null || true

clean:
	rm bin/* 2> /dev/null || true
	rmdir bin 2> /dev/null || true 
